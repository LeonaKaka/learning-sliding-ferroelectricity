#!/usr/bin/env python3
"""Reproduction Lab · Lesson 10 · super-rough depinning geometry.

Validates roughness estimators before any finite-size-scaling claim.
For d=1 QEW depinning, zeta_global>1 is super-rough: local B(r) need not
return the same exponent as S(q). This lesson checks that logic on a
synthetic zeta=1.25 interface, then on last-pinned QEW configurations.
"""
from pathlib import Path
import math, csv
import numpy as np
from numba import njit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DU=0.25; DT=0.05; RF=1.0; THRESH_ITERS=10; TOL=2e-7; MAX_STEPS=400_000
REALIZATIONS=6; BOOTSTRAPS=1000; SYNTH_ZETA=1.25

@njit
def relax_line(f, table, du, dt, max_steps, tol, disp_periods, u_init):
    L,M=table.shape; period=M*du; u=u_init.copy(); c0=0.0
    for x in range(L): c0+=u[x]
    c0/=L; stable=0; v=np.empty(L)
    for step in range(max_steps):
        maxr=0.0; s=0.0
        for x in range(L):
            xm=x-1 if x>0 else L-1; xp=x+1 if x<L-1 else 0
            p=(u[x]/du)%M; i=int(math.floor(p)); a=p-i; j=i+1
            if j==M: j=0
            fp=(1-a)*table[x,i]+a*table[x,j]
            val=u[xp]+u[xm]-2*u[x]+fp+f; v[x]=val
            av=abs(val); maxr=max(maxr,av)
        if maxr<tol:
            stable+=1
            if stable>=10: return 0,u,step+1,maxr
        else: stable=0
        for x in range(L): u[x]+=dt*v[x]; s+=u[x]
        if s/L-c0>disp_periods*period: return 1,u,step+1,maxr
    return 2,u,max_steps,maxr

def disorder(L,M,seed):
    rng=np.random.default_rng(seed); raw=rng.standard_normal((L,M))
    q=2*np.pi*np.fft.fftfreq(M,d=DU); filt=np.exp(-.5*(q*RF)**2)
    F=np.fft.ifft((-1j*q)[None,:]*np.fft.fft(raw,axis=1)*filt[None,:],axis=1).real
    return F/F.std()

def threshold(table,disp_periods=1.0):
    L,M=table.shape; lo,hi=.30,1.30; z=np.zeros(L)
    st,u_lo,*_=relax_line(lo,table,DU,DT,MAX_STEPS,TOL,disp_periods,z)
    if st!=0: raise RuntimeError(f'low-force unresolved: {st}')
    st,*_=relax_line(hi,table,DU,DT,MAX_STEPS,TOL,disp_periods,u_lo)
    if st!=1: raise RuntimeError(f'high-force unresolved: {st}')
    last=u_lo.copy()
    for _ in range(THRESH_ITERS):
        mid=.5*(lo+hi); st,u_mid,*_=relax_line(mid,table,DU,DT,MAX_STEPS,TOL,disp_periods,u_lo)
        if st==0: lo,u_lo,last=mid,u_mid,u_mid.copy()
        elif st==1: hi=mid
        else: raise RuntimeError(f'threshold unresolved at f={mid}')
    return lo,hi,last

def observables(u):
    L=len(u); x=u-u.mean(); rs=np.arange(1,L//4+1)
    B=np.array([np.mean((np.roll(x,-r)-x)**2) for r in rs])
    fft=np.fft.rfft(x); S=(np.abs(fft)**2)/L; q=2*np.pi*np.arange(len(S))/L
    return rs,B,q[1:],S[1:]

def zeta_B(rs,B,rlo=2,rhi=8):
    m=(rs>=rlo)&(rs<=rhi); slope=np.polyfit(np.log(rs[m]),np.log(B[m]),1)[0]; return .5*slope

def zeta_S(q,S,nlo,nhi):
    n=np.arange(1,len(q)+1); m=(n>=nlo)&(n<=nhi)
    slope=np.polyfit(np.log(q[m]),np.log(S[m]),1)[0]; return -.5*(slope+1)

def synthetic_superrough(L=256,R=256,zeta=SYNTH_ZETA,seed=20266256):
    rng=np.random.default_rng(seed); n=np.arange(0,L//2+1); target=np.zeros_like(n,dtype=float)
    target[1:]=n[1:]**(-(1+2*zeta)); Bs=[]; Ss=[]
    for _ in range(R):
        a=np.zeros(L//2+1,dtype=np.complex128); re=rng.normal(size=L//2-1); im=rng.normal(size=L//2-1)
        a[1:-1]=np.sqrt(target[1:-1]/2)*(re+1j*im); a[-1]=np.sqrt(target[-1])*rng.normal()
        u=np.fft.irfft(a,n=L)*L; rs,B,q,S=observables(u); Bs.append(B); Ss.append(S)
    Bm=np.mean(Bs,axis=0); Sm=np.mean(Ss,axis=0)
    return rs,Bm,q,Sm,zeta_B(rs,Bm),zeta_S(q,Sm,8,32)

def qew_ensemble(L,M,seed0):
    Bs=[]; Ss=[]; spans=[]; fcs=[]; rows=[]; representative=None
    for k in range(REALIZATIONS):
        seed=seed0+k; table=disorder(L,M,seed); lo,hi,u=threshold(table,1.0); rs,B,q,S=observables(u)
        Bs.append(B); Ss.append(S); span=(u.max()-u.min())/(M*DU); spans.append(span); fcs.append(.5*(lo+hi))
        if representative is None: representative=u.copy()
        rows.append((L,M,seed,lo,hi,.5*(lo+hi),span))
    Bs=np.array(Bs); Ss=np.array(Ss); Bm=Bs.mean(0); Sm=Ss.mean(0); nlo,nhi=((4,16) if L==128 else (8,32))
    zb=zeta_B(rs,Bm); zs=zeta_S(q,Sm,nlo,nhi)
    rng=np.random.default_rng(20267000+L); boot_b=[]; boot_s=[]
    for _ in range(BOOTSTRAPS):
        idx=rng.integers(0,REALIZATIONS,size=REALIZATIONS); boot_b.append(zeta_B(rs,Bs[idx].mean(0))); boot_s.append(zeta_S(q,Ss[idx].mean(0),nlo,nhi))
    ci_b=np.percentile(boot_b,[2.5,50,97.5]); ci_s=np.percentile(boot_s,[2.5,50,97.5])
    return dict(L=L,M=M,rs=rs,B=Bm,q=q,S=Sm,zB=zb,zS=zs,ciB=ci_b,ciS=ci_s,
                span_max=float(np.max(spans)),span_median=float(np.median(spans)),fc_mean=float(np.mean(fcs)),fc_std=float(np.std(fcs)),rows=rows,profile=representative)

srs,sB,sq,sS,synth_zB,synth_zS=synthetic_superrough()
assert abs(synth_zS-SYNTH_ZETA)<.05 and .85<synth_zB<1.05 and synth_zS-synth_zB>.15

cert=[]
for seed in (20265001,20265002):
    table=disorder(128,2048,seed); a=threshold(table,1.0); b=threshold(table,2.0)
    amid=.5*(a[0]+a[1]); bmid=.5*(b[0]+b[1]); cert.append((seed,amid,bmid,abs(amid-bmid)))
cert_spread=max(r[-1] for r in cert); assert cert_spread<5e-4

r128=qew_ensemble(128,2048,20269128); r256=qew_ensemble(256,4096,20269256)
for r in (r128,r256):
    assert r['span_max']<.35 and .85<r['zB']<1.05 and r['zS']>1.00 and r['zS']-r['zB']>.08

global_drift=abs(r128['zS']-r256['zS']); local_drift=abs(r128['zB']-r256['zB']); THERMO_GATE=.10; thermo_pass=global_drift<THERMO_GATE
receipt=['Lesson 10 super-rough roughness validation','track                         = Paper2-oriented',
         'synthetic target zeta_global = 1.250000',f'synthetic zeta_B local       = {synth_zB:.6f}',f'synthetic zeta_S global      = {synth_zS:.6f}',
         'SYNTHETIC SUPER-ROUGH GOLD TEST = PASS',f'moving-cert midpoint spread = {cert_spread:.6e}',
         'moving certificate          = 1 period validated against 2 periods on 2 realizations']
for r in (r128,r256):
    receipt += [f"L={r['L']} M={r['M']} realizations       = {REALIZATIONS}",f"L={r['L']} zeta_B local                  = {r['zB']:.6f}",
                f"L={r['L']} zeta_B realization-bootstrap 95% = [{r['ciB'][0]:.6f}, {r['ciB'][2]:.6f}]",f"L={r['L']} zeta_S global                 = {r['zS']:.6f}",
                f"L={r['L']} zeta_S realization-bootstrap 95% = [{r['ciS'][0]:.6f}, {r['ciS'][2]:.6f}]",f"L={r['L']} max wall-span / u-period      = {r['span_max']:.6f}"]
receipt += [f'cross-size zeta_B drift      = {local_drift:.6f}',f'cross-size zeta_S drift      = {global_drift:.6f}',
            f'thermodynamic zeta drift gate = < {THERMO_GATE:.3f}','SMALL-QEW SUPER-ROUGH SIGNATURE = PASS',
            f"THERMODYNAMIC ZETA CLOSURE   = {'PASS' if thermo_pass else 'NOT PASSED'}",'FINITE-SIZE SCALING REQUIRED BEFORE UNIVERSAL ZETA CLAIM']
print('\n'.join(receipt))
root=Path(__file__).resolve().parents[2]; out=root/'assets'/'reproduction-lab'; out.mkdir(parents=True,exist_ok=True)
(out/'lesson10_superrough_zeta.txt').write_text('\n'.join(receipt)+'\n',encoding='utf-8')
with (out/'lesson10_superrough_zeta.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['L','M','seed','fc_lo','fc_hi','fc_mid','wall_span_over_period']); w.writerows(r128['rows']+r256['rows'])

# ---------------- Real matplotlib evidence plots ----------------

def finish(fig, name):
    fig.tight_layout()
    fig.savefig(out/name, dpi=220, bbox_inches='tight')
    plt.close(fig)

def fit_line_B(r, B):
    m=(r>=2)&(r<=8)
    coef=np.polyfit(np.log(r[m]),np.log(B[m]),1)
    return m, np.exp(coef[1])*r[m]**coef[0]

def fit_line_S(q, S, nlo, nhi):
    n=np.arange(1,len(q)+1); m=(n>=nlo)&(n<=nhi)
    coef=np.polyfit(np.log(q[m]),np.log(S[m]),1)
    return m, np.exp(coef[1])*q[m]**coef[0]

# 1) Representative critical configurations: what is being measured?
fig,ax=plt.subplots(figsize=(7.2,4.4))
for r in (r128,r256):
    x=np.arange(r['L'])
    u=r['profile']-r['profile'].mean()
    ax.plot(x,u,label=f"L={r['L']} representative last-pinned profile")
ax.set_xlabel('x (lattice site)')
ax.set_ylabel(r'$u(x)-\langle u\rangle$')
ax.set_title('Critical-sample interface profiles used for geometry measurements')
ax.legend()
finish(fig,'lesson10_profiles.png')

# 2) Local real-space correlation B(r).
fig,ax=plt.subplots(figsize=(7.2,4.6))
for r,ls in ((r128,'-'),(r256,'--')):
    ax.loglog(r['rs'],r['B'],ls,marker='o',markersize=3,label=f"L={r['L']} data; zeta_B={r['zB']:.3f}")
    m,yfit=fit_line_B(r['rs'],r['B'])
    ax.loglog(r['rs'][m],yfit,':',linewidth=2,label=f"L={r['L']} fit r=2..8")
ax.set_xlabel('separation r')
ax.set_ylabel(r'$B(r)=\langle[u(x+r)-u(x)]^2\rangle$')
ax.set_title('Local roughness: the short-distance fit saturates near zeta_local = 1')
ax.legend(fontsize=8)
finish(fig,'lesson10_Br.png')

# 3) Structure factor S(q), directly matching the paper observable.
fig,ax=plt.subplots(figsize=(7.2,4.6))
for r,(nlo,nhi),ls in ((r128,(4,16),'-'),(r256,(8,32),'--')):
    ax.loglog(r['q'],r['S'],ls,marker='o',markersize=3,label=f"L={r['L']} data; zeta_S={r['zS']:.3f}")
    m,yfit=fit_line_S(r['q'],r['S'],nlo,nhi)
    ax.loglog(r['q'][m],yfit,':',linewidth=2,label=f"L={r['L']} fit window")
# paper reference slope -3.5, normalized to pass through the L=256 curve near the fit window
qref=r256['q']; Sref=r256['S']; idx=15
ref=Sref[idx]*(qref/qref[idx])**(-3.5)
ax.loglog(qref,ref,'-.',linewidth=1.5,label=r'paper reference slope $q^{-3.5}$ ($\zeta=1.25$)')
ax.set_xlabel('wave number q')
ax.set_ylabel(r'$S(q)$')
ax.set_title('Structure factor: same observable and scaling form as Ferrero PRE Fig. 1')
ax.legend(fontsize=8)
finish(fig,'lesson10_Sq.png')

# 4) Size dependence with realization-bootstrap intervals.
fig,ax=plt.subplots(figsize=(6.8,4.5))
Ls_plot=np.array([128,256],float)
zB=np.array([r128['zB'],r256['zB']]); zS=np.array([r128['zS'],r256['zS']])
loB=np.array([r128['ciB'][0],r256['ciB'][0]]); hiB=np.array([r128['ciB'][2],r256['ciB'][2]])
loS=np.array([r128['ciS'][0],r256['ciS'][0]]); hiS=np.array([r128['ciS'][2],r256['ciS'][2]])
ax.errorbar(Ls_plot,zB,yerr=np.vstack([zB-loB,hiB-zB]),marker='o',capsize=4,label='local zeta from B(r)')
ax.errorbar(Ls_plot,zS,yerr=np.vstack([zS-loS,hiS-zS]),marker='s',capsize=4,label='global zeta from S(q)')
ax.axhline(1.25,linestyle='--',linewidth=1.2,label='QEW literature benchmark 1.25')
ax.set_xscale('log',base=2)
ax.set_xticks([128,256],labels=['128','256'])
ax.set_xlabel('system size L')
ax.set_ylabel('effective roughness exponent')
ax.set_title('Only two sizes: super-rough signature is visible, thermodynamic zeta is not closed')
ax.legend(fontsize=8)
finish(fig,'lesson10_zeta_vs_size.png')

# Machine-readable mean curves used in the plots.
with (out/'lesson10_geometry_curves.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['L','observable','x','mean_value','fit_window'])
    for r,(nlo,nhi) in ((r128,(4,16)),(r256,(8,32))):
        for x,y in zip(r['rs'],r['B']): w.writerow([r['L'],'B(r)',x,y,int(2<=x<=8)])
        for n,(x,y) in enumerate(zip(r['q'],r['S']),start=1): w.writerow([r['L'],'S(q)',x,y,int(nlo<=n<=nhi)])

print('saved matplotlib plots:', ', '.join([
    'lesson10_profiles.png','lesson10_Br.png','lesson10_Sq.png','lesson10_zeta_vs_size.png']))

