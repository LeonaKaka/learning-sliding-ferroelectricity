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

lx=np.log10(Ls); sy=np.log10(stds); syny=np.log10(syn_stds)
def poly(xs,ys,x0,y0,w,h):
    xmin,xmax=min(xs),max(xs); ymin,ymax=min(ys),max(ys); pad=.08*(ymax-ymin or 1); ymin-=pad; ymax+=pad
    return ' '.join(f'{x0+(x-xmin)/(xmax-xmin)*w:.1f},{y0+h-(y-ymin)/(ymax-ymin)*h:.1f}' for x,y in zip(xs,ys))
p_real=poly(lx,sy,55,80,400,155); p_syn=poly(lx,syny,555,80,400,155)
wn=np.array([nu_small,nu_all,nu_large]); wx=np.arange(3)
p_win=poly(wx,wn,55,350,400,140); p_col=poly(grid,scores,555,350,400,140)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="590" viewBox="0 0 1050 590" role="img" aria-label="Lesson 11 finite-size scaling validation"><style>text{{font-family:system-ui,-apple-system,sans-serif;fill:#20211f}}.box{{fill:#fffdf8;stroke:#d8d1c3}}.ax{{stroke:#444}}.a{{fill:none;stroke:#222;stroke-width:2}}.b{{fill:none;stroke:#777;stroke-width:1.6;stroke-dasharray:6 4}}.ttl{{font-size:18px;font-weight:650}}.small{{font-size:12px;fill:#716d66}}.big{{font-size:24px;font-weight:700}}</style><rect width="1050" height="590" fill="#fff"/><text x="525" y="28" text-anchor="middle" font-size="22">Reproduction Lab · Lesson 11 · finite-size threshold fluctuations</text><rect class="box" x="35" y="48" width="450" height="225" rx="8"/><text class="ttl" x="55" y="72">1 · Real QEW: std(fc) decreases with L</text><line class="ax" x1="55" y1="235" x2="455" y2="235"/><line class="ax" x1="55" y1="80" x2="55" y2="235"/><polyline class="a" points="{p_real}"/><text class="small" x="55" y="255">48 independent disorder samples per L · variance-fit nu={nu_all:.3f}</text><rect class="box" x="535" y="48" width="480" height="225" rx="8"/><text class="ttl" x="555" y="72">2 · Synthetic nu=4/3 gold test</text><line class="ax" x1="555" y1="235" x2="955" y2="235"/><line class="ax" x1="555" y1="80" x2="555" y2="235"/><polyline class="a" points="{p_syn}"/><text class="big" x="585" y="150">recovered nu = {syn_nu:.3f}</text><text class="small" x="555" y="255">Same log-std vs log-L regression pipeline.</text><rect class="box" x="35" y="315" width="450" height="220" rx="8"/><text class="ttl" x="55" y="340">3 · Size-window stability is not closed</text><line class="ax" x1="55" y1="490" x2="455" y2="490"/><polyline class="a" points="{p_win}"/><text class="small" x="55" y="515">small3={nu_small:.3f} · all4={nu_all:.3f} · large3={nu_large:.3f} · drift={window_drift:.3f}</text><rect class="box" x="535" y="315" width="480" height="220" rx="8"/><text class="ttl" x="555" y="340">4 · Quantile collapse is shallow, not decisive</text><line class="ax" x1="555" y1="490" x2="955" y2="490"/><polyline class="a" points="{p_col}"/><text class="small" x="555" y="515">best nu={best_nu:.3f} · score(best)={best_score:.3f} · score(4/3)={score_sts:.3f}</text></svg>'''
(out/'lesson11_fss_nu.svg').write_text(svg,encoding='utf-8')
