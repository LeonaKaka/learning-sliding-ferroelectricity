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
    Bs=[]; Ss=[]; spans=[]; fcs=[]; rows=[]
    for k in range(REALIZATIONS):
        seed=seed0+k; table=disorder(L,M,seed); lo,hi,u=threshold(table,1.0); rs,B,q,S=observables(u)
        Bs.append(B); Ss.append(S); span=(u.max()-u.min())/(M*DU); spans.append(span); fcs.append(.5*(lo+hi))
        rows.append((L,M,seed,lo,hi,.5*(lo+hi),span))
    Bs=np.array(Bs); Ss=np.array(Ss); Bm=Bs.mean(0); Sm=Ss.mean(0); nlo,nhi=((4,16) if L==128 else (8,32))
    zb=zeta_B(rs,Bm); zs=zeta_S(q,Sm,nlo,nhi)
    rng=np.random.default_rng(20267000+L); boot_b=[]; boot_s=[]
    for _ in range(BOOTSTRAPS):
        idx=rng.integers(0,REALIZATIONS,size=REALIZATIONS); boot_b.append(zeta_B(rs,Bs[idx].mean(0))); boot_s.append(zeta_S(q,Ss[idx].mean(0),nlo,nhi))
    ci_b=np.percentile(boot_b,[2.5,50,97.5]); ci_s=np.percentile(boot_s,[2.5,50,97.5])
    return dict(L=L,M=M,rs=rs,B=Bm,q=q,S=Sm,zB=zb,zS=zs,ciB=ci_b,ciS=ci_s,
                span_max=float(np.max(spans)),span_median=float(np.median(spans)),fc_mean=float(np.mean(fcs)),fc_std=float(np.std(fcs)),rows=rows)

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

def poly(xs,ys,x0,y0,W,H,xmin,xmax,ymin,ymax):
    return ' '.join(f'{x0+(x-xmin)/(xmax-xmin)*W:.1f},{y0+H-(y-ymin)/(ymax-ymin)*H:.1f}' for x,y in zip(xs,ys))
def lg(x): return np.log10(x)
b128=(r128['rs']>=1)&(r128['rs']<=32); b256=(r256['rs']>=1)&(r256['rs']<=64)
s128n=np.arange(1,len(r128['q'])+1); s128=(s128n>=2)&(s128n<=32); s256n=np.arange(1,len(r256['q'])+1); s256=(s256n>=4)&(s256n<=64)
bxs=np.concatenate([lg(r128['rs'][b128]),lg(r256['rs'][b256])]); bys=np.concatenate([lg(r128['B'][b128]),lg(r256['B'][b256])]); sxs=np.concatenate([lg(r128['q'][s128]),lg(r256['q'][s256])]); sys=np.concatenate([lg(r128['S'][s128]),lg(r256['S'][s256])])
pB128=poly(lg(r128['rs'][b128]),lg(r128['B'][b128]),55,80,410,165,bxs.min(),bxs.max(),bys.min(),bys.max()); pB256=poly(lg(r256['rs'][b256]),lg(r256['B'][b256]),55,80,410,165,bxs.min(),bxs.max(),bys.min(),bys.max())
pS128=poly(lg(r128['q'][s128]),lg(r128['S'][s128]),555,80,410,165,sxs.min(),sxs.max(),sys.min(),sys.max()); pS256=poly(lg(r256['q'][s256]),lg(r256['S'][s256]),555,80,410,165,sxs.min(),sxs.max(),sys.min(),sys.max())
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="600" viewBox="0 0 1050 600" role="img" aria-label="Lesson 10 super-rough roughness validation"><style>text{{font-family:system-ui,-apple-system,sans-serif;fill:#20211f}}.box{{fill:#fffdf8;stroke:#d8d1c3}}.ax{{stroke:#444}}.a{{fill:none;stroke:#222;stroke-width:2}}.b{{fill:none;stroke:#777;stroke-width:1.7;stroke-dasharray:7 5}}.ttl{{font-size:18px;font-weight:650}}.small{{font-size:12px;fill:#716d66}}.big{{font-size:24px;font-weight:700}}</style><rect width="1050" height="600" fill="#fff"/><text x="525" y="30" text-anchor="middle" font-size="22">Reproduction Lab · Lesson 10 · super-rough depinning geometry</text><rect class="box" x="35" y="50" width="450" height="235" rx="8"/><text class="ttl" x="55" y="74">1 · Local B(r): super-roughness saturates near 1</text><line class="ax" x1="55" y1="245" x2="465" y2="245"/><line class="ax" x1="55" y1="80" x2="55" y2="245"/><polyline class="a" points="{pB128}"/><polyline class="b" points="{pB256}"/><text class="small" x="55" y="267">L=128 zeta_B={r128['zB']:.3f} · L=256 zeta_B={r256['zB']:.3f} · fit r=2…8</text><rect class="box" x="535" y="50" width="480" height="235" rx="8"/><text class="ttl" x="555" y="74">2 · Structure factor carries global zeta</text><line class="ax" x1="555" y1="245" x2="965" y2="245"/><line class="ax" x1="555" y1="80" x2="555" y2="245"/><polyline class="a" points="{pS128}"/><polyline class="b" points="{pS256}"/><text class="small" x="555" y="267">L=128 zeta_S={r128['zS']:.3f} · L=256 zeta_S={r256['zS']:.3f} · same fractional q window</text><rect class="box" x="35" y="320" width="450" height="225" rx="8"/><text class="ttl" x="55" y="346">3 · Synthetic zeta_global=1.25 gold test</text><text class="big" x="70" y="410">zeta_B(local) = {synth_zB:.3f}</text><text class="big" x="70" y="452">zeta_S(global) = {synth_zS:.3f}</text><text class="small" x="55" y="515">The estimators are supposed to disagree for a super-rough interface.</text><rect class="box" x="535" y="320" width="480" height="225" rx="8"/><text class="ttl" x="555" y="346">4 · Do not promote this to thermodynamic zeta yet</text><text class="big" x="570" y="410">delta zeta_S(size) = {global_drift:.3f}</text><text class="big" x="570" y="452">gate &lt; {THERMO_GATE:.2f} → {'PASS' if thermo_pass else 'NOT PASSED'}</text><text class="small" x="555" y="495">realization-bootstrap S(q) intervals are broad at R=6</text><text class="small" x="555" y="515">Lesson11 must do the size ladder / finite-size scaling.</text></svg>'''
(out/'lesson10_superrough_zeta.svg').write_text(svg,encoding='utf-8'); print('saved:',out/'lesson10_superrough_zeta.svg')
