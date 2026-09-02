#!/usr/bin/env python3
"""Reproduction Lab · Lesson 11 · finite-size threshold fluctuations and nu.

Default mode is intentionally cheap: it analyzes a frozen CSV of independently
computed sample thresholds.  The raw thresholds were generated with the same
T=0 QEW pinned/moving classifier used in Lessons 07/10, using a one-u-period
moving certificate and M_phys ~ L^1.25.  This script does NOT claim that the
resulting small-system effective exponent is thermodynamic.
"""
from pathlib import Path
import csv, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TARGET_NU=4/3
WINDOW_DRIFT_GATE=0.15
BOOTSTRAPS=3000
EXPECTED={32:320,64:736,128:1728,256:4096}
N_PER_SIZE=48

def load_raw(path):
    rows=[]
    with open(path,newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append({k:(int(v) if k in ('L','M','seed') else float(v)) for k,v in r.items()})
    for L,M in EXPECTED.items():
        rr=[r for r in rows if r['L']==L]
        assert len(rr)==N_PER_SIZE, (L,len(rr))
        assert all(r['M']==M for r in rr)
        assert len({r['seed'] for r in rr})==N_PER_SIZE
        assert all(abs((r['fc_hi']-r['fc_lo'])-1/512)<1e-12 for r in rr)
    return rows

def fit_nu(Ls,stds):
    slope,inter=np.polyfit(np.log(Ls),np.log(stds),1)
    return -1/slope,slope,inter

def collapse_score(rows,Ls,nu,probs=np.linspace(.1,.9,9)):
    q=[]
    for L in Ls:
        x=np.array([r['fc_mid'] for r in rows if r['L']==L])
        x=(x-x.mean())*L**(1/nu)
        q.append(np.quantile(x,probs))
    A=np.vstack(q)
    denom=np.sqrt(np.mean(A*A))
    return np.sqrt(np.mean((A-A.mean(0))**2))/denom

def synthetic_gold(Ls,nu=TARGET_NU,seed=20261110):
    rng=np.random.default_rng(seed); s=[]
    for L in Ls:
        x=.04*(L/Ls[0])**(-1/nu)*rng.normal(size=512)
        s.append(np.std(x,ddof=1))
    return np.array(s),fit_nu(Ls,np.array(s))[0]

root=Path(__file__).resolve().parents[2]
raw_path=root/'assets'/'reproduction-lab'/'lesson11_fc_raw.csv'
rows=load_raw(raw_path)
Ls=np.array(sorted(EXPECTED),dtype=float)
means=np.array([np.mean([r['fc_mid'] for r in rows if r['L']==L]) for L in Ls])
stds=np.array([np.std([r['fc_mid'] for r in rows if r['L']==L],ddof=1) for L in Ls])
nu_all=fit_nu(Ls,stds)[0]
nu_small=fit_nu(Ls[:3],stds[:3])[0]
nu_large=fit_nu(Ls[1:],stds[1:])[0]
window_drift=max(nu_all,nu_small,nu_large)-min(nu_all,nu_small,nu_large)

syn_stds,syn_nu=synthetic_gold(Ls)
assert abs(syn_nu-TARGET_NU)<.05

rng=np.random.default_rng(20261111); boot=[]
for _ in range(BOOTSTRAPS):
    ss=[]
    for L in Ls:
        x=np.array([r['fc_mid'] for r in rows if r['L']==L])
        xb=x[rng.integers(0,len(x),len(x))]
        ss.append(np.std(xb,ddof=1))
    boot.append(fit_nu(Ls,np.array(ss))[0])
boot=np.array(boot); ci=np.percentile(boot,[2.5,50,97.5])

grid=np.linspace(.8,2.2,281)
scores=np.array([collapse_score(rows,Ls,n) for n in grid])
best_nu=float(grid[np.argmin(scores)]); best_score=float(scores.min())
score_sts=float(collapse_score(rows,Ls,TARGET_NU)); score_fit=float(collapse_score(rows,Ls,nu_all))
window_pass=window_drift<WINDOW_DRIFT_GATE

receipt=[
'Lesson 11 finite-size threshold scaling',
'paper relation                 = Var(fc_sample) ~ L^(-2/nu_dep)',
'paper aspect protocol          = M_phys ~ L^zeta_dep with zeta_dep=1.25',
'raw statistical unit           = disorder realization',
f'realizations per L            = {N_PER_SIZE}',
'L ladder                       = 32, 64, 128, 256',
'M grid ladder                  = 320, 736, 1728, 4096',
'moving certificate             = 1 u-period',
'fc bracket width               = 0.001953125',
f'synthetic target nu           = {TARGET_NU:.6f}',
f'synthetic recovered nu        = {syn_nu:.6f}',
'SYNTHETIC FSS GOLD TEST         = PASS',
]
for L,M,mu,sd in zip(Ls,[EXPECTED[int(L)] for L in Ls],means,stds):
    receipt += [f'L={int(L):3d} M={M:4d} mean fc             = {mu:.9f}',f'L={int(L):3d} M={M:4d} std(fc)             = {sd:.9f}']
receipt += [
 f'nu all four sizes             = {nu_all:.6f}',
 f'nu smallest three             = {nu_small:.6f}',
 f'nu largest three              = {nu_large:.6f}',
 f'size-window nu drift          = {window_drift:.6f}',
 f'size-window drift gate        = < {WINDOW_DRIFT_GATE:.3f}',
 f'realization-bootstrap 95% nu  = [{ci[0]:.6f}, {ci[2]:.6f}]',
 f'quantile-collapse best nu      = {best_nu:.6f}',
 f'collapse score best            = {best_score:.6f}',
 f'collapse score nu=4/3          = {score_sts:.6f}',
 f'collapse score variance-fit nu = {score_fit:.6f}',
 f'SIZE-WINDOW STABILITY GATE     = {"PASS" if window_pass else "NOT PASSED"}',
 'UNIVERSAL NU CLAIM              = NOT AUTHORIZED',
 'FINITE-SIZE TREND EXISTS; THERMODYNAMIC CLOSURE REQUIRES LARGER-SCALE EVIDENCE',
]
print('\n'.join(receipt))
out=root/'assets'/'reproduction-lab'; out.mkdir(parents=True,exist_ok=True)
(out/'lesson11_fss_nu.txt').write_text('\n'.join(receipt)+'\n',encoding='utf-8')

def finish(fig,name):
    fig.tight_layout(); fig.savefig(out/name,dpi=220,bbox_inches='tight'); plt.close(fig)

# 1) Same finite-size threshold observable as the source figure: mean fc versus L.
fig,ax=plt.subplots(figsize=(7.0,4.4))
ax.errorbar(Ls,means,yerr=stds,marker='o',capsize=4,label='mean ± sample std')
ax.set_xscale('log',base=2); ax.set_xticks(Ls,labels=[str(int(x)) for x in Ls])
ax.set_xlabel('system size L')
ax.set_ylabel('sample threshold fc')
ax.set_title('Finite-size sample thresholds in our normalization')
ax.legend()
finish(fig,'lesson11_mean_fc.png')

# 2) The nu-sensitive statistic: width of the sample-threshold distribution.
fig,ax=plt.subplots(figsize=(7.0,4.5))
ax.loglog(Ls,stds,marker='o',label='measured std(fc)')
coef=np.polyfit(np.log(Ls),np.log(stds),1)
yfit=np.exp(coef[1])*Ls**coef[0]
ax.loglog(Ls,yfit,'--',label=f'all-four fit: nu={nu_all:.3f}')
ax.set_xlabel('system size L')
ax.set_ylabel('std(fc across disorder realizations)')
ax.set_title('Threshold fluctuations shrink with L')
ax.legend()
finish(fig,'lesson11_std_fc.png')

# 3) Window dependence of the effective nu.
fig,ax=plt.subplots(figsize=(7.0,4.4))
labels=['32-128','32-256','64-256']; vals=[nu_small,nu_all,nu_large]
ax.plot(labels,vals,marker='o')
ax.axhline(TARGET_NU,linestyle='--',label='QEW benchmark 4/3')
ax.set_xlabel('size window used in fit')
ax.set_ylabel('effective nu')
ax.set_title('The inferred nu changes too much when the size window changes')
ax.legend()
finish(fig,'lesson11_nu_vs_window.png')

# 4) Collapse score scan: the optimum is shallow, not an independent proof.
fig,ax=plt.subplots(figsize=(7.0,4.4))
ax.plot(grid,scores)
ax.axvline(best_nu,linestyle='-',label=f'best score at nu={best_nu:.3f}')
ax.axvline(TARGET_NU,linestyle='--',label='nu=4/3')
ax.axvline(nu_all,linestyle=':',label=f'variance-fit nu={nu_all:.3f}')
ax.set_xlabel('trial nu')
ax.set_ylabel('quantile-collapse score (lower is better)')
ax.set_title('Distribution-collapse score has a broad shallow minimum')
ax.legend(fontsize=8)
finish(fig,'lesson11_collapse_score.png')

print('saved matplotlib plots:', ', '.join(['lesson11_mean_fc.png','lesson11_std_fc.png','lesson11_nu_vs_window.png','lesson11_collapse_score.png']))

