#!/usr/bin/env python3
"""Lesson 08: validate steady v(f) before any beta fit (Paper2 method track)."""
from pathlib import Path
import math
import numpy as np

SEED=20260902
FC_LO,FC_HI=0.77763671875,0.777783203125
DT_GATE=5e-3

def disorder(L=32,M=256,du=.25,rf=1.,seed=SEED):
    rng=np.random.default_rng(seed); raw=rng.standard_normal((L,M))
    q=2*np.pi*np.fft.fftfreq(M,d=du); filt=np.exp(-.5*(q*rf)**2)
    F=np.fft.ifft((-1j*q)[None,:]*np.fft.fft(raw,axis=1)*filt[None,:],axis=1).real
    return F/F.std(),du

def fp(u,T,du):
    L,M=T.shape; p=(u/du)%M; i=np.floor(p).astype(int); a=p-i; j=(i+1)%M; x=np.arange(L)
    return (1-a)*T[x,i]+a*T[x,j]

def relax(f,T,du,dt=.05,u0=None,tol=2e-7,max_steps=500_000):
    L,M=T.shape; u=np.zeros(L) if u0 is None else np.array(u0,copy=True); c0=u.mean(); stable=0
    for _ in range(max_steps):
        v=np.roll(u,-1)+np.roll(u,1)-2*u+fp(u,T,du)+f
        if np.max(np.abs(v))<tol:
            stable+=1
            if stable>=10:return 'pinned',u
        else: stable=0
        u+=dt*v
        if u.mean()-c0>2*M*du:return 'moving',u
    raise RuntimeError('unresolved motion classifier')

def threshold(T,du,dt=.05,lo=.4,hi=1.,n=12):
    state,u=relax(lo,T,du,dt); assert state=='pinned'
    assert relax(hi,T,du,dt,u)[0]=='moving'
    last=u.copy()
    for _ in range(n):
        m=(lo+hi)/2; state,um=relax(m,T,du,dt,u)
        if state=='pinned': lo,u,last=m,um,um.copy()
        else: hi=m
    return lo,hi,last

def particle_v(f,dt=.02,warm=2,measure=4):
    P=2*np.pi; u=t=pu=pt=0.; targets=[P*k for k in range(1,warm+measure+1)]; cross=[]; k=0
    for _ in range(2_000_000):
        u+=dt*(f-math.sin(u)); t+=dt
        while k<len(targets) and u>=targets[k]:
            a=(targets[k]-pu)/(u-pu); cross.append(pt+a*(t-pt)); k+=1
        if k==len(targets):break
        pu,pt=u,t
    if k<len(targets):raise RuntimeError('particle traversal incomplete')
    return (P/np.diff(np.r_[0.,cross]))[warm:]

def line_v(f,T,du,u0,dt,warm=1,measure=3):
    L,M=T.shape; P=M*du; u=np.array(u0,copy=True); c0=u.mean(); pc=c0; t=pt=0.
    targets=[c0+P*k for k in range(1,warm+measure+1)]; cross=[]; k=0
    for _ in range(2_000_000):
        v=np.roll(u,-1)+np.roll(u,1)-2*u+fp(u,T,du)+f; u+=dt*v; t+=dt; c=u.mean()
        while k<len(targets) and c>=targets[k]:
            a=(targets[k]-pc)/(c-pc); cross.append(pt+a*(t-pt)); k+=1
        if k==len(targets):break
        pc,pt=c,t
    if k<len(targets):raise RuntimeError('line traversal incomplete')
    vv=P/np.diff(np.r_[0.,cross]); return vv[:warm],vv[warm:]

particle=[]
for f in (1.05,1.10,1.20,1.50):
    ex=math.sqrt(f*f-1); num=particle_v(f).mean(); particle.append((f,ex,num,abs(num-ex)/ex))
p_err=max(x[3] for x in particle); assert p_err<2e-5

L,M,du,rf=32,256,.25,1.; T,du=disorder(L,M,du,rf); lo,hi,u0=threshold(T,du)
assert abs(lo-FC_LO)<1e-12 and abs(hi-FC_HI)<1e-12
fc=(lo+hi)/2; dfs=np.array([.02,.04,.08,.16]); fs=fc+dfs; dts=(.1,.05,.025,.0125)
runs={}
for dt in dts:
    runs[dt]=[]
    for f in fs:
        warm,steady=line_v(f,T,du,u0,dt)
        runs[dt].append((warm[0],steady.mean(),np.max(np.abs(steady-steady.mean()))/steady.mean(),steady))

def errs(dt):return [abs(runs[dt][j][1]-runs[.0125][j][1])/runs[.0125][j][1] for j in range(len(fs))]
coarse,mid,prod=max(errs(.1)),max(errs(.05)),max(errs(.025))
trans=[abs(runs[.025][j][0]-runs[.025][j][1])/runs[.025][j][1] for j in range(len(fs))]
station=max(runs[.025][j][2] for j in range(len(fs)))
assert coarse>DT_GATE and prod<DT_GATE and station<5e-4

R=[
'Lesson 08 steady-velocity validation',f'seed                         = {SEED}',
f'registered fc bracket        = [{lo:.9f}, {hi:.9f}]',f'registered fc midpoint       = {fc:.9f}',
f'velocity dt gate             = {100*DT_GATE:.3f}%', 'particle gold-test dt        = 0.0200',
f'particle max rel error       = {100*p_err:.6f}%',f'line L, M, du, rf            = {L}, {M}, {du:.3f}, {rf:.3f}',
'line delta-f ladder          = 0.02, 0.04, 0.08, 0.16','steady protocol             = discard 1 u-period; measure next 3 periods',
f'coarse dt=.100 max error     = {100*coarse:.3f}%  FAIL (<0.5% gate)',f'dt=.050 max error            = {100*mid:.3f}%',
f'production dt=.025 max err  = {100*prod:.3f}%  PASS','reference dt=.0125           = comparison authority for this lesson',
f'first-period transient shift = {100*min(trans):.2f}% .. {100*max(trans):.2f}%',f'steady 3-period spread max   = {100*station:.4f}%']
for j,(df,f) in enumerate(zip(dfs,fs)):
    R.append(f"df={df:.3f} f={f:.9f} v(dt=.025)={runs[.025][j][1]:.9f} v(dt=.0125)={runs[.0125][j][1]:.9f}")
R+=['NO BETA FIT IN LESSON 08','STEADY VELOCITY ESTIMATOR + DT CONVERGENCE PASS']; print('\n'.join(R))

def poly(xs,ys,x0,y0,w,h,xmin,xmax,ymin,ymax):
    return ' '.join(f'{x0+(x-xmin)/(xmax-xmin)*w:.1f},{y0+h-(y-ymin)/(ymax-ymin)*h:.1f}' for x,y in zip(xs,ys))
px=np.array([x[0] for x in particle]); ex=np.array([x[1] for x in particle]); nu=np.array([x[2] for x in particle])
p1,p1n=poly(px,ex,55,75,400,155,1.04,1.51,.25,1.2),poly(px,nu,55,75,400,155,1.04,1.51,.25,1.2)
trav=[poly(np.arange(1,5),np.r_[runs[.025][j][0],runs[.025][j][3]],555,75,400,155,1,4,.25,.52) for j in range(4)]
p3=[poly(dfs,100*np.array(errs(dt)),55,345,400,155,.02,.16,0,1.1) for dt in (.1,.05,.025)]
v=np.array([x[1] for x in runs[.025]]); p4=poly(dfs,v,555,345,400,155,.02,.16,.28,.52)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="590" viewBox="0 0 1050 590"><style>text{{font-family:system-ui,sans-serif;fill:#20211f}}.box{{fill:#fffdf8;stroke:#d8d1c3}}.ax{{stroke:#444}}.a{{fill:none;stroke:#222;stroke-width:2}}.b{{fill:none;stroke:#666;stroke-width:1.5;stroke-dasharray:6 4}}.c{{fill:none;stroke:#999;stroke-width:1.5}}.t{{font-size:18px;font-weight:650}}.s{{font-size:12px;fill:#716d66}}</style><rect width="1050" height="590" fill="#fff"/><text x="525" y="28" text-anchor="middle" font-size="22">Reproduction Lab · Lesson 08 · steady velocity before beta</text>
<rect class="box" x="35" y="45" width="450" height="225" rx="8"/><text class="t" x="55" y="68">1 · Analytic velocity gold test</text><line class="ax" x1="55" y1="230" x2="455" y2="230"/><line class="ax" x1="55" y1="75" x2="55" y2="230"/><polyline class="a" points="{p1}"/><polyline class="b" points="{p1n}"/><text class="s" x="55" y="252">v̄ = √(f²−1); numerical max rel error {100*p_err:.4f}%</text>
<rect class="box" x="535" y="45" width="480" height="225" rx="8"/><text class="t" x="555" y="68">2 · First disorder period is transient</text><line class="ax" x1="555" y1="230" x2="955" y2="230"/><line class="ax" x1="555" y1="75" x2="555" y2="230"/>{''.join(f'<polyline class="a" opacity=".72" points="{z}"/>' for z in trav)}<line class="b" x1="688" y1="75" x2="688" y2="230"/><text class="s" x="555" y="252">period 1 discarded; transient shift {100*min(trans):.1f}–{100*max(trans):.1f}%</text>
<rect class="box" x="35" y="315" width="450" height="225" rx="8"/><text class="t" x="55" y="338">3 · Preserve the 0.5% dt gate</text><line class="ax" x1="55" y1="500" x2="455" y2="500"/><line class="ax" x1="55" y1="345" x2="55" y2="500"/><line class="b" x1="55" y1="429.5" x2="455" y2="429.5"/><polyline class="a" points="{p3[0]}"/><polyline class="b" points="{p3[1]}"/><polyline class="c" points="{p3[2]}"/><text class="s" x="55" y="522">dt=.100 max {100*coarse:.3f}% FAIL · dt=.025 max {100*prod:.3f}% PASS vs .0125</text>
<rect class="box" x="535" y="315" width="480" height="225" rx="8"/><text class="t" x="555" y="338">4 · Production v(f) values — no exponent fit</text><line class="ax" x1="555" y1="500" x2="955" y2="500"/><line class="ax" x1="555" y1="345" x2="555" y2="500"/><polyline class="a" points="{p4}"/><text class="s" x="555" y="522">Δf = f − midpoint([f−,f+]); β fitting is explicitly forbidden here.</text></svg>'''
out=Path(__file__).resolve().parents[2]/'assets'/'reproduction-lab'; out.mkdir(parents=True,exist_ok=True)
(out/'lesson08_steady_velocity.txt').write_text('\n'.join(R)+'\n'); (out/'lesson08_steady_velocity.svg').write_text(svg)
