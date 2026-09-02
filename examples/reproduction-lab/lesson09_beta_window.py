#!/usr/bin/env python3
"""Reproduction Lab · Lesson 09 · beta needs a stable critical window.

Paper2-oriented validation checkpoint.

Authority / scope
-----------------
Ferrero et al. (2013) emphasize that the velocity is an order parameter near
T=0 depinning, but also that mesoscopic corrections-to-scaling can bias simple
power-law fits. This lesson therefore does NOT accept one good-looking log-log
line as evidence for a universal beta.

Protocol
--------
1. Regression gold test on du/dt=f-sin(u), whose asymptotic beta is 1/2.
2. Eight independent quenched disorder realizations. Each realization gets its
   own finite-sample fc bracket before any velocity is measured.
3. Steady velocity uses the Lesson08 estimator: dt=.025, discard one full
   u-period, measure the next three periods.
4. Fit the arithmetic disorder mean v(Delta f), then shrink the registered
   upper edge of the fit window without post-hoc point selection.
5. Bootstrap only the independent disorder realizations. Delta-f points are
   repeated measurements within a realization, not independent n.
"""
from pathlib import Path
import math
import numpy as np
from numba import njit

SEEDS=np.arange(20260902,20260910,dtype=np.int64)
L,M,DU,RF=32,256,0.25,1.0
DT_THRESHOLD=0.05
DT_VELOCITY=0.025
DFS=np.array([0.015,0.025,0.040,0.065,0.105,0.170])
WINDOW_MAX=np.array([0.170,0.105,0.065,0.040])
WINDOW_DRIFT_GATE=0.030
BOOTSTRAPS=10000

@njit
def _interp_force(u, table, du):
    L,M=table.shape
    out=np.empty(L)
    for x in range(L):
        p=(u[x]/du)%M
        i=int(math.floor(p)); a=p-i; j=i+1
        if j==M: j=0
        out[x]=(1.0-a)*table[x,i]+a*table[x,j]
    return out

@njit
def _relax(f,table,du,dt,u0,tol=2e-7,max_steps=500000,periods=2.0):
    L,M=table.shape
    u=u0.copy(); c0=0.0
    for i in range(L): c0+=u[i]
    c0/=L; stable=0
    for _ in range(max_steps):
        pin=_interp_force(u,table,du)
        vel=np.empty(L); maxr=0.0
        for i in range(L):
            im=i-1 if i>0 else L-1; ip=i+1 if i<L-1 else 0
            v=(u[ip]+u[im]-2.0*u[i])+pin[i]+f
            vel[i]=v
            if abs(v)>maxr: maxr=abs(v)
        if maxr<tol:
            stable+=1
            if stable>=10: return 0,u
        else:
            stable=0
        com=0.0
        for i in range(L):
            u[i]+=dt*vel[i]; com+=u[i]
        com/=L
        if com-c0>periods*M*du: return 1,u
    return 2,u

@njit
def _threshold(table,du,dt=0.05,lo=0.4,hi=1.0,n=12):
    u=np.zeros(table.shape[0])
    state,u=_relax(lo,table,du,dt,u)
    if state!=0: return -1.0,-1.0,u
    state,_=_relax(hi,table,du,dt,u)
    if state!=1: return -2.0,-2.0,u
    for _ in range(n):
        mid=0.5*(lo+hi)
        state,um=_relax(mid,table,du,dt,u)
        if state==0:
            lo=mid; u=um
        elif state==1:
            hi=mid
        else:
            return -3.0,-3.0,u
    return lo,hi,u

@njit
def _line_velocity(f,table,du,u0,dt=0.025,warm=1,measure=3):
    L,M=table.shape; P=M*du
    u=u0.copy(); c0=0.0
    for i in range(L): c0+=u[i]
    c0/=L; prev_c=c0; t=0.0; prev_t=0.0
    nt=warm+measure
    targets=np.empty(nt); crossings=np.empty(nt)
    for k in range(nt): targets[k]=c0+P*(k+1)
    k=0
    for _ in range(2000000):
        pin=_interp_force(u,table,du); c=0.0
        for i in range(L):
            im=i-1 if i>0 else L-1; ip=i+1 if i<L-1 else 0
            v=(u[ip]+u[im]-2.0*u[i])+pin[i]+f
            u[i]+=dt*v; c+=u[i]
        c/=L; t+=dt
        while k<nt and c>=targets[k]:
            a=(targets[k]-prev_c)/(c-prev_c)
            crossings[k]=prev_t+a*(t-prev_t); k+=1
        if k==nt: break
        prev_c=c; prev_t=t
    if k<nt: return -1.0
    prev=0.0; total=0.0; count=0
    for j in range(nt):
        vv=P/(crossings[j]-prev); prev=crossings[j]
        if j>=warm: total+=vv; count+=1
    return total/count

def disorder(seed):
    rng=np.random.default_rng(int(seed))
    raw=rng.standard_normal((L,M))
    q=2*np.pi*np.fft.fftfreq(M,d=DU)
    filt=np.exp(-0.5*(q*RF)**2)
    force=np.fft.ifft((-1j*q)[None,:]*np.fft.fft(raw,axis=1)*filt[None,:],axis=1).real
    return force/force.std()

def particle_velocity(f,dt=0.01,warm=2,measure=5):
    P=2*np.pi; u=0.0; t=0.0; pu=0.0; pt=0.0
    targets=[P*k for k in range(1,warm+measure+1)]
    cross=[]; k=0
    for _ in range(4000000):
        u+=dt*(f-math.sin(u)); t+=dt
        while k<len(targets) and u>=targets[k]:
            a=(targets[k]-pu)/(u-pu)
            cross.append(pt+a*(t-pt)); k+=1
        if k==len(targets): break
        pu,pt=u,t
    if k<len(targets): raise RuntimeError('particle traversal incomplete')
    vv=P/np.diff(np.r_[0.0,cross])
    return float(vv[warm:].mean())

def fit_beta(x,y):
    return float(np.polyfit(np.log(x),np.log(y),1)[0])

particle_df=np.array([0.003,0.006,0.012,0.024,0.048])
particle_v=np.array([particle_velocity(1.0+d) for d in particle_df])
particle_beta=[]
for mx in (0.048,0.024,0.012):
    m=particle_df<=mx+1e-15
    particle_beta.append(fit_beta(particle_df[m],particle_v[m]))
particle_beta=np.array(particle_beta)
particle_beta_err=float(np.max(np.abs(particle_beta-0.5)))
assert particle_beta_err<0.005

vel=np.empty((len(SEEDS),len(DFS)))
fc_lo=np.empty(len(SEEDS)); fc_hi=np.empty(len(SEEDS))
for si,seed in enumerate(SEEDS):
    table=disorder(seed)
    lo,hi,u0=_threshold(table,DU,DT_THRESHOLD)
    if lo<0: raise RuntimeError(f'threshold failed for seed {seed}: {lo}')
    fc_lo[si],fc_hi[si]=lo,hi
    fc=0.5*(lo+hi)
    for j,df in enumerate(DFS):
        v=_line_velocity(fc+df,table,DU,u0,DT_VELOCITY)
        if v<=0: raise RuntimeError(f'velocity failed for seed {seed}, df={df}')
        vel[si,j]=v

bracket_width=fc_hi-fc_lo
assert np.max(bracket_width)<2e-4
mean_v=vel.mean(axis=0)

window_beta=[]
for mx in WINDOW_MAX:
    m=DFS<=mx+1e-15
    window_beta.append(fit_beta(DFS[m],mean_v[m]))
window_beta=np.array(window_beta)
window_drift=float(window_beta.max()-window_beta.min())
window_pass=window_drift<WINDOW_DRIFT_GATE

rng=np.random.default_rng(20260902)
boot=np.empty(BOOTSTRAPS)
for b in range(BOOTSTRAPS):
    idx=rng.integers(0,len(SEEDS),len(SEEDS))
    boot[b]=fit_beta(DFS,vel[idx].mean(axis=0))
ci=np.quantile(boot,[0.025,0.5,0.975])

half=float(np.mean(bracket_width)/2)
beta_if_lo=fit_beta(DFS+half,mean_v)
beta_if_hi=fit_beta(DFS-half,mean_v)
threshold_edge_span=abs(beta_if_lo-beta_if_hi)
assert threshold_edge_span<0.005

receipt=[
    'Lesson 09 beta-window validation',
    'scope                        = Paper2-oriented; small-QEW checkpoint',
    f'independent disorder n       = {len(SEEDS)}',
    'statistical unit             = disorder realization (not df points)',
    f'seeds                        = {SEEDS[0]}..{SEEDS[-1]}',
    f'line L, M, du, rf            = {L}, {M}, {DU:.3f}, {RF:.3f}',
    f'threshold dt                 = {DT_THRESHOLD:.4f}',
    f'velocity dt                  = {DT_VELOCITY:.4f}',
    'steady protocol              = discard 1 u-period; measure next 3 periods',
    'delta-f ladder                = 0.015, 0.025, 0.040, 0.065, 0.105, 0.170',
    f'particle beta windows         = {particle_beta[0]:.6f}, {particle_beta[1]:.6f}, {particle_beta[2]:.6f}',
    f'particle max |beta-0.5|       = {particle_beta_err:.6f}',
    f'max threshold bracket width  = {np.max(bracket_width):.9f}',
]
for seed,lo,hi in zip(SEEDS,fc_lo,fc_hi):
    receipt.append(f'seed={seed} fc bracket          = [{lo:.9f}, {hi:.9f}]')
for df,mv in zip(DFS,mean_v):
    receipt.append(f'df={df:.3f} disorder-mean v     = {mv:.9f}')
for mx,b in zip(WINDOW_MAX,window_beta):
    receipt.append(f'max df={mx:.3f} beta             = {b:.6f}')
receipt += [
    f'window beta drift            = {window_drift:.6f}',
    f'window drift gate            = < {WINDOW_DRIFT_GATE:.3f}',
    f'all-six beta                 = {window_beta[0]:.6f}',
    f'sample bootstrap 95% CI      = [{ci[0]:.6f}, {ci[2]:.6f}]',
    f'bootstrap median             = {ci[1]:.6f}',
    f'threshold-edge beta span     = {threshold_edge_span:.6f}',
    'UNIVERSAL BETA CLAIM          = NOT AUTHORIZED',
    'WINDOW-STABILITY GATE         = ' + ('PASS' if window_pass else 'NOT PASSED'),
]
print('\n'.join(receipt))

out=Path(__file__).resolve().parents[2]/'assets'/'reproduction-lab'
out.mkdir(parents=True,exist_ok=True)
header=['seed','fc_lo','fc_hi']+[f'v_df_{d:.3f}' for d in DFS]
rows=[]
for i,seed in enumerate(SEEDS):
    rows.append([str(int(seed)),f'{fc_lo[i]:.9f}',f'{fc_hi[i]:.9f}']+[f'{x:.9f}' for x in vel[i]])
(out/'lesson09_beta_window.csv').write_text(','.join(header)+'\n'+'\n'.join(','.join(r) for r in rows)+'\n',encoding='utf-8')
(out/'lesson09_beta_window.txt').write_text('\n'.join(receipt)+'\n',encoding='utf-8')

def poly(xs,ys,x0,y0,w,h,xmin,xmax,ymin,ymax):
    return ' '.join(f'{x0+(x-xmin)/(xmax-xmin)*w:.1f},{y0+h-(y-ymin)/(ymax-ymin)*h:.1f}' for x,y in zip(xs,ys))

p1=poly(np.array([.048,.024,.012]),particle_beta,55,75,400,145,.010,.050,.498,.506)
p2=poly(DFS,mean_v,555,75,400,145,.015,.170,.22,.51)
p3=poly(WINDOW_MAX[::-1],window_beta[::-1],55,350,400,145,.04,.17,.15,.28)
allb=window_beta[0]
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="590" viewBox="0 0 1050 590" role="img" aria-label="Lesson 09 beta critical-window validation"><style>text{{font-family:system-ui,-apple-system,sans-serif;fill:#20211f}}.box{{fill:#fffdf8;stroke:#d8d1c3}}.ax{{stroke:#444;stroke-width:1}}.a{{fill:none;stroke:#222;stroke-width:2}}.b{{fill:none;stroke:#777;stroke-width:1.5;stroke-dasharray:6 4}}.ttl{{font-size:18px;font-weight:650}}.s{{font-size:12px;fill:#716d66}}</style><rect width="1050" height="590" fill="#fff"/><text x="525" y="28" text-anchor="middle" font-size="22">Reproduction Lab · Lesson 09 · beta needs a stable critical window</text>
<rect class="box" x="35" y="45" width="450" height="225" rx="8"/><text class="ttl" x="55" y="68">1 · Regression gold test: beta = 1/2</text><line class="ax" x1="55" y1="220" x2="455" y2="220"/><line class="ax" x1="55" y1="75" x2="55" y2="220"/><polyline class="a" points="{p1}"/><line class="b" x1="55" y1="183.8" x2="455" y2="183.8"/><text class="s" x="55" y="245">tilted washboard: max |beta−0.5| = {particle_beta_err:.4f}</text>
<rect class="box" x="535" y="45" width="480" height="225" rx="8"/><text class="ttl" x="555" y="68">2 · Eight independent disorder samples</text><line class="ax" x1="555" y1="220" x2="955" y2="220"/><line class="ax" x1="555" y1="75" x2="555" y2="220"/><polyline class="a" points="{p2}"/><text class="s" x="555" y="245">arithmetic disorder mean v(Δf); each sample uses its own fc bracket</text>
<rect class="box" x="35" y="320" width="450" height="225" rx="8"/><text class="ttl" x="55" y="343">3 · Critical-window stability gate</text><line class="ax" x1="55" y1="495" x2="455" y2="495"/><line class="ax" x1="55" y1="350" x2="55" y2="495"/><polyline class="a" points="{p3}"/><text class="s" x="55" y="520">max Δf: .170 → .105 → .065 → .040; drift = {window_drift:.3f} &gt; {WINDOW_DRIFT_GATE:.3f} gate</text>
<rect class="box" x="535" y="320" width="480" height="225" rx="8"/><text class="ttl" x="555" y="343">4 · Precision is not the same as asymptotics</text><line x1="740" y1="408" x2="780" y2="408" stroke="#333" stroke-width="3"/><line x1="760" y1="380" x2="760" y2="436" stroke="#333" stroke-width="3"/><text x="800" y="414" font-size="17">all-six beta = {allb:.3f}</text><text class="s" x="555" y="470">sample bootstrap 95% CI = [{ci[0]:.3f}, {ci[2]:.3f}]</text><text class="s" x="555" y="495">threshold-edge beta span = {threshold_edge_span:.4f}</text><text class="s" x="555" y="520">window drift dominates → universal beta NOT claimed</text></svg>'''
(out/'lesson09_beta_window.svg').write_text(svg,encoding='utf-8')
