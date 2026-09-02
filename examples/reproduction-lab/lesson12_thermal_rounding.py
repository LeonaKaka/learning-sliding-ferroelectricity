#!/usr/bin/env python3
"""Reproduction Lab · Lesson 12 · finite-T rounding and creep boundary.

Default mode is cheap and analyzes frozen raw Langevin runs.  The raw data were
produced with Euler-Maruyama for the same smooth random-bond-like QEW line used
in Lessons 07-11, at L=32, M=320, du=0.25, dt=0.025.  Quenched disorder
realizations are the statistical units.  Thermal trajectory repeats live inside
a realization and are averaged before disorder-level inference.

The lesson deliberately separates two claims:
(1) thermal rounding at a finite-sample threshold, v(fc,T) ~ T^psi;
(2) subthreshold activated motion / creep.  Ordinary finite-time Langevin is
not allowed to claim an asymptotic creep law when low-T trajectories do not
resolve a stationary activated velocity.
"""
from pathlib import Path
import math
import numpy as np
import pandas as pd

PSI_SYNTH=0.15
PSI_WINDOW_GATE=0.03
BOOTSTRAPS=5000
ROUND_SEEDS=8

def log_slope(x,y,n=None):
    if n is not None: x,y=x[:n],y[:n]
    return float(np.polyfit(np.log(x),np.log(y),1)[0])

def brownian_gold(seed=20261201,ntraj=10000,dt=.02,steps=500,f=.17,T=.08):
    rng=np.random.default_rng(seed); u=np.zeros(ntraj); sig=math.sqrt(2*T*dt)
    for _ in range(steps): u += f*dt + sig*rng.standard_normal(ntraj)
    t=dt*steps; em=f*t; ev=2*T*t
    mean=float(u.mean()); var=float(u.var(ddof=1))
    return mean,em,abs(mean-em)/abs(em),var,ev,abs(var-ev)/ev

def synthetic_psi_gold(Ts,seed=20261202,psi=PSI_SYNTH,n=512):
    rng=np.random.default_rng(seed); vals=[]
    for T in Ts:
        amp=np.exp(.04*rng.standard_normal(n)-.5*.04**2)
        vals.append(np.mean((T**psi)*amp))
    vals=np.asarray(vals); fits=[log_slope(Ts,vals,nw) for nw in (4,5,6)]
    return vals,fits

root=Path(__file__).resolve().parents[2]
out=root/'assets'/'reproduction-lab'
rounding=pd.read_csv(out/'lesson12_rounding_raw.csv')
sub=pd.read_csv(out/'lesson12_subthreshold_raw.csv')
assert len(rounding)==144 and len(sub)==40
assert set(rounding.authority)=={'lo','mid','hi'}
Ts=np.array(sorted(rounding['T'].unique()),float)
assert len(Ts)==6 and len(rounding.seed.unique())==ROUND_SEEDS
for a in ('lo','mid','hi'):
    assert len(rounding[rounding.authority==a])==ROUND_SEEDS*len(Ts)

# Cheap stochastic-integrator gold test: free drift-diffusion.
bm,bm_ex,bm_err,bv,bv_ex,bv_err=brownian_gold()
assert bm_err<.01 and bv_err<.03

# Regression gold test for the new thermal exponent pipeline.
synth_vals,synth_fits=synthetic_psi_gold(Ts)
assert max(abs(x-PSI_SYNTH) for x in synth_fits)<.005

agg={}; psis={}
for a in ('lo','mid','hi'):
    d=rounding[rounding.authority==a]
    vv=np.array([d[d['T']==T].v_mean_within_disorder.mean() for T in Ts])
    agg[a]=vv; psis[a]=[log_slope(Ts,vv,nw) for nw in (4,5,6)]
mid_drift=max(psis['mid'])-min(psis['mid'])
authority_span=max(x[2] for x in psis.values())-min(x[2] for x in psis.values())

# Hierarchical logic: resample quenched disorder, not the three thermal repeats.
seeds=np.array(sorted(rounding.seed.unique()))
dm=rounding[rounding.authority=='mid']
V=np.array([[dm[(dm.seed==s)&(dm['T']==T)].v_mean_within_disorder.iloc[0] for T in Ts] for s in seeds])
rng=np.random.default_rng(20261212); b6=[]; b4=[]; bd=[]
for _ in range(BOOTSTRAPS):
    idx=rng.integers(0,len(seeds),size=len(seeds)); vals=V[idx].mean(axis=0)
    p4=log_slope(Ts,vals,4); p6=log_slope(Ts,vals,6)
    b4.append(p4); b6.append(p6); bd.append(p6-p4)
ci4=np.percentile(b4,[2.5,50,97.5]); ci6=np.percentile(b6,[2.5,50,97.5]); cid=np.percentile(bd,[2.5,50,97.5])

# Subthreshold diagnostic. resolved_fraction is the within-disorder fraction
# of two thermal trajectories whose COM crossed 0.25 of the disorder period.
subTs=np.array(sorted(sub['T'].unique()),float); subagg=[]
for T in subTs:
    d=sub[sub['T']==T]
    subagg.append((T,float(d.mean_v.mean()),float(d.resolved_fraction.mean()),float(np.median(d.max_half_rel_diff))))
creep_resolved=[(rf==1.0 and hd<.2) for _,_,rf,hd in subagg]
lowT_resolved=creep_resolved[0]
assert not lowT_resolved

receipt=[
'Lesson 12 thermal rounding + creep boundary',
'paper relation                  = v(fc,T) ~ T^psi',
'paper collapse                  = v T^-psi ~ h_+(f T^-psi/beta), h_-(...)',
'rounding statistical unit       = quenched disorder realization',
'rounding disorder realizations  = 8',
'rounding thermal repeats/sample = 3',
'rounding T ladder               = 0.0025, 0.005, 0.01, 0.02, 0.04, 0.08',
'fc authority audit              = lo, midpoint, hi of each sample bracket',
'Brownian gold mean rel error    = %.6f%%'%(100*bm_err),
'Brownian gold variance rel err  = %.6f%%'%(100*bv_err),
'BROWNIAN NOISE-NORMALIZATION GOLD TEST = PASS',
'synthetic target psi            = %.6f'%PSI_SYNTH,
'synthetic psi low4/low5/all6    = %.6f / %.6f / %.6f'%tuple(synth_fits),
'SYNTHETIC THERMAL-EXPONENT GOLD TEST = PASS',
]
for a in ('lo','mid','hi'):
    receipt += [f'{a} psi low4/low5/all6          = {psis[a][0]:.6f} / {psis[a][1]:.6f} / {psis[a][2]:.6f}']
receipt += [
 f'midpoint psi window drift      = {mid_drift:.6f}',
 f'psi window drift gate          = < {PSI_WINDOW_GATE:.3f}',
 f'threshold-authority all6 span  = {authority_span:.6f}',
 f'midpoint psi low4 bootstrap95  = [{ci4[0]:.6f}, {ci4[2]:.6f}]',
 f'midpoint psi all6 bootstrap95  = [{ci6[0]:.6f}, {ci6[2]:.6f}]',
 f'window-drift bootstrap95       = [{cid[0]:.6f}, {cid[2]:.6f}]',
 f'THERMAL-ROUNDING WINDOW GATE    = {"PASS" if mid_drift<PSI_WINDOW_GATE else "NOT PASSED"}',
 'UNIVERSAL PSI CLAIM             = NOT AUTHORIZED',
 'subthreshold drive              = f = fc_lo - 0.08',
 'subthreshold thermal repeats    = 2 per disorder sample',
]
for T,v,rf,hd in subagg:
    receipt += [f'sub T={T:.3f} mean v / resolved / half-diff = {v:.6f} / {rf:.4f} / {hd:.6f}']
receipt += [
 'resolved activated-motion rule  = trajectory fraction 1.0 AND median half-diff < 0.2',
 'LOW-T CREEP ASYMPTOTIC RESOLVED = NO',
 'CREEP-LAW / MU CLAIM             = NOT AUTHORIZED',
 'FINITE-T ROUNDING OBSERVED; ASYMPTOTIC THERMAL AND CREEP EXPONENTS REMAIN OPEN',
]
print('\n'.join(receipt))
out.mkdir(parents=True,exist_ok=True)
(out/'lesson12_thermal_rounding.txt').write_text('\n'.join(receipt)+'\n',encoding='utf-8')

def poly(xs,ys,x0,y0,w,h,xmin=None,xmax=None,ymin=None,ymax=None):
    xs=np.asarray(xs,float); ys=np.asarray(ys,float)
    xmin=float(xs.min() if xmin is None else xmin); xmax=float(xs.max() if xmax is None else xmax)
    ymin=float(ys.min() if ymin is None else ymin); ymax=float(ys.max() if ymax is None else ymax)
    if ymax==ymin:ymax+=1
    return ' '.join(f'{x0+(x-xmin)/(xmax-xmin)*w:.1f},{y0+h-(y-ymin)/(ymax-ymin)*h:.1f}' for x,y in zip(xs,ys))
lT=np.log10(Ts); lv=np.log10(agg['mid']); p_round=poly(lT,lv,55,80,400,155)
p_auth=[]; ymin=min(np.log10(agg[a]).min() for a in agg); ymax=max(np.log10(agg[a]).max() for a in agg)
for a in ('lo','mid','hi'): p_auth.append(poly(lT,np.log10(agg[a]),555,80,400,155,lT.min(),lT.max(),ymin,ymax))
p_sub=poly(subTs,[x[1] for x in subagg],55,355,400,135)
p_res=poly(subTs,[x[2] for x in subagg],555,355,400,135,subTs.min(),subTs.max(),0,1)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="590" viewBox="0 0 1050 590" role="img" aria-label="Lesson 12 thermal rounding and creep boundary"><style>text{{font-family:system-ui,-apple-system,sans-serif;fill:#20211f}}.box{{fill:#fffdf8;stroke:#d8d1c3}}.ax{{stroke:#444}}.a{{fill:none;stroke:#222;stroke-width:2}}.b{{fill:none;stroke:#777;stroke-width:1.5;stroke-dasharray:6 4}}.c{{fill:none;stroke:#aaa;stroke-width:1.5}}.ttl{{font-size:18px;font-weight:650}}.small{{font-size:12px;fill:#716d66}}.big{{font-size:23px;font-weight:700}}</style><rect width="1050" height="590" fill="#fff"/><text x="525" y="28" text-anchor="middle" font-size="22">Reproduction Lab · Lesson 12 · finite-T rounding / creep boundary</text><rect class="box" x="35" y="48" width="450" height="225" rx="8"/><text class="ttl" x="55" y="72">1 · v(fc,T) rises with T, but psi drifts</text><line class="ax" x1="55" y1="235" x2="455" y2="235"/><line class="ax" x1="55" y1="80" x2="55" y2="235"/><polyline class="a" points="{p_round}"/><text class="small" x="55" y="255">midpoint psi: low4={psis['mid'][0]:.3f} · low5={psis['mid'][1]:.3f} · all6={psis['mid'][2]:.3f}</text><rect class="box" x="535" y="48" width="480" height="225" rx="8"/><text class="ttl" x="555" y="72">2 · Threshold bracket is not the main drift</text><line class="ax" x1="555" y1="235" x2="955" y2="235"/><line class="ax" x1="555" y1="80" x2="555" y2="235"/><polyline class="c" points="{p_auth[0]}"/><polyline class="a" points="{p_auth[1]}"/><polyline class="b" points="{p_auth[2]}"/><text class="small" x="555" y="255">all6 psi span across fc lo/mid/hi = {authority_span:.4f}; T-window drift = {mid_drift:.4f}</text><rect class="box" x="35" y="320" width="450" height="215" rx="8"/><text class="ttl" x="55" y="345">3 · Subthreshold activated velocity exists</text><line class="ax" x1="55" y1="490" x2="455" y2="490"/><polyline class="a" points="{p_sub}"/><text class="small" x="55" y="515">f = fc_lo - 0.08 · direct finite-time Langevin</text><rect class="box" x="535" y="320" width="480" height="215" rx="8"/><text class="ttl" x="555" y="345">4 · But low-T creep is unresolved</text><line class="ax" x1="555" y1="490" x2="955" y2="490"/><polyline class="a" points="{p_res}"/><text class="big" x="585" y="415">T=.02 resolved = {subagg[0][2]*100:.1f}%</text><text class="small" x="555" y="515">Low-T half-window velocity instability is large → no creep μ claim.</text></svg>'''
(out/'lesson12_thermal_rounding.svg').write_text(svg,encoding='utf-8')
