#!/usr/bin/env python3
"""Lesson 08: validate steady v(f) before any beta fit (Paper2 method track)."""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

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

out=Path(__file__).resolve().parents[2]/'assets'/'reproduction-lab'
out.mkdir(parents=True,exist_ok=True)
(out/'lesson08_steady_velocity.txt').write_text('\n'.join(R)+'\n')

def finish(fig,name):
    fig.tight_layout(); fig.savefig(out/name,dpi=220,bbox_inches='tight'); plt.close(fig)

# 1) Direct observable bridge: steady center-of-mass velocity versus drive.
fig,ax=plt.subplots(figsize=(7.2,4.5))
vprod=np.array([r[1] for r in runs[.025]])
vref=np.array([r[1] for r in runs[.0125]])
ax.plot(fs,vprod,marker='o',label='正式计算 dt=0.025')
ax.plot(fs,vref,marker='s',linestyle='--',label='参考 dt=0.0125')
ax.axvline(fc,linestyle=':',label='L07 阈值区间中点')
ax.set_xlabel('驱动力 f')
ax.set_ylabel('质心稳态速度 v')
ax.set_title('只在单样本阈值上方测量稳态 v(f)')
ax.legend()
finish(fig,'lesson08_vf.png')

# 2) Why the first traversal is discarded.
fig,ax=plt.subplots(figsize=(7.2,4.5))
for j,df in enumerate(dfs):
    vv=np.r_[runs[.025][j][0],runs[.025][j][3]]
    ax.plot(np.arange(1,5),vv,marker='o',label=f'Δf={df:.3f}')
ax.axvline(1.5,linestyle=':',label='第 1 个周期后开始测量')
ax.set_xticks([1,2,3,4])
ax.set_xlabel('无序周期编号')
ax.set_ylabel('周期平均速度')
ax.set_title('第 1 个周期仍含退钉扎瞬态')
ax.legend(fontsize=8)
finish(fig,'lesson08_transient_periods.png')

# 3) Time-step convergence as an actual error plot.
fig,ax=plt.subplots(figsize=(7.2,4.5))
for dt in (.1,.05,.025):
    ax.plot(dfs,100*np.array(errs(dt)),marker='o',label=f'dt={dt:g}')
ax.axhline(100*DT_GATE,linestyle='--',label='预设 0.5% 判据')
ax.set_xlabel('Δf = f - fc（阈值区间中点）')
ax.set_ylabel('相对 dt=0.0125 参考值的误差（%）')
ax.set_title('速度估计量的 dt 收敛')
ax.legend()
finish(fig,'lesson08_dt_error.png')

# 4) Analytic moving-state gold test.
fig,ax=plt.subplots(figsize=(6.8,4.3))
px=np.array([x[0] for x in particle]); ex=np.array([x[1] for x in particle]); nu=np.array([x[2] for x in particle])
ax.plot(px,ex,marker='o',label=r'解析 $\sqrt{f^2-1}$')
ax.plot(px,nu,marker='s',linestyle='--',label='数值速度估计')
ax.set_xlabel('驱动力 f')
ax.set_ylabel('平均速度')
ax.set_title('运动态速度估计量的已知答案测试')
ax.legend()
finish(fig,'lesson08_particle_velocity_gold.png')

print('saved matplotlib plots:', ', '.join(['lesson08_vf.png','lesson08_transient_periods.png','lesson08_dt_error.png','lesson08_particle_velocity_gold.png']))

