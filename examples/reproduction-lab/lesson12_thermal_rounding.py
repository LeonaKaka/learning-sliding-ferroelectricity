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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

def finish(fig,name):
    fig.tight_layout(); fig.savefig(out/name,dpi=220,bbox_inches='tight'); plt.close(fig)

# 1) Thermal rounding observable itself: v(fc,T) on log-log axes.
fig,ax=plt.subplots(figsize=(7.2,4.6))
for a,ls in zip(('lo','mid','hi'),('-', '--', ':')):
    ax.loglog(Ts,agg[a],ls,marker='o',label=f'fc authority: {a}')
# show the registered midpoint fits over low4 and all6 to make window drift visible
for nw,ls in ((4,'-.'),(6,(0,(3,1,1,1)))):
    coef=np.polyfit(np.log(Ts[:nw]),np.log(agg['mid'][:nw]),1)
    y=np.exp(coef[1])*Ts[:nw]**coef[0]
    ax.loglog(Ts[:nw],y,linestyle=ls,linewidth=2,label=f'midpoint fit first {nw}: psi={coef[0]:.3f}')
ax.set_xlabel('temperature T')
ax.set_ylabel(r'$v(f_c,T)$')
ax.set_title('Thermal rounding: the fitted psi changes with the temperature window')
ax.legend(fontsize=8)
finish(fig,'lesson12_rounding_vT.png')

# 2) psi versus registered temperature window.
fig,ax=plt.subplots(figsize=(7.0,4.4))
windows=np.array([4,5,6])
for a in ('lo','mid','hi'):
    ax.plot(windows,psis[a],marker='o',label=f'fc authority: {a}')
ax.axhline(PSI_SYNTH,linestyle='--',label='synthetic-gold target 0.15 (not a QEW benchmark)')
ax.set_xticks(windows,labels=['low 4 T','low 5 T','all 6 T'])
ax.set_ylabel('effective psi')
ax.set_title('Window drift dominates threshold-bracket uncertainty')
ax.legend(fontsize=8)
finish(fig,'lesson12_psi_vs_window.png')

# 3) Subthreshold finite-time activated motion.
fig,ax=plt.subplots(figsize=(7.0,4.4))
sv=np.array([x[1] for x in subagg])
ax.plot(subTs,sv,marker='o')
ax.set_xlabel('temperature T')
ax.set_ylabel('mean subthreshold velocity')
ax.set_title('Below threshold, finite-time activated velocity increases with T')
finish(fig,'lesson12_subthreshold_vT.png')

# 4) Why low-T creep asymptotics are not resolved.
fig,ax=plt.subplots(figsize=(7.0,4.4))
rf=np.array([x[2] for x in subagg]); hd=np.array([x[3] for x in subagg])
ax.plot(subTs,rf,marker='o',label='resolved trajectory fraction')
ax.axhline(1.0,linestyle='--',label='required resolved fraction = 1')
ax.set_xlabel('temperature T')
ax.set_ylabel('resolved trajectory fraction')
ax.set_ylim(0,1.05)
ax.set_title('The lowest-T ensemble is not fully resolved in the observation window')
ax.legend()
finish(fig,'lesson12_resolved_fraction.png')

fig,ax=plt.subplots(figsize=(7.0,4.4))
ax.semilogy(subTs,hd,marker='o')
ax.axhline(.2,linestyle='--',label='registered half-window stability gate = 0.2')
ax.set_xlabel('temperature T')
ax.set_ylabel('median relative difference: first half vs second half')
ax.set_title('Low-T velocity is strongly nonstationary, so a creep exponent is not fit')
ax.legend()
finish(fig,'lesson12_halfwindow_stability.png')

print('saved matplotlib plots:', ', '.join(['lesson12_rounding_vT.png','lesson12_psi_vs_window.png','lesson12_subthreshold_vT.png','lesson12_resolved_fraction.png','lesson12_halfwindow_stability.png']))

