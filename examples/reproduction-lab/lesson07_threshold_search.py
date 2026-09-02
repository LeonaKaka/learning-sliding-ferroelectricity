#!/usr/bin/env python3
"""
Reproduction Lab · Lesson 07 · Paper2-oriented methods
Threshold search for a T=0 driven elastic line in quenched disorder.

Paper anchors:
- Ferrero et al. 2013, Sec. 4.3.1: for a finite disorder sample, f_c^sample is
  the maximal force for which a metastable configuration still exists.
- Middleton properties motivate monotone forward threshold logic.

This lesson does NOT claim to reproduce Ferrero's exact metastable-state
algorithm. Instead it validates a direct-relaxation threshold bracket before
we use thresholds in velocity scaling.

Validation ladder:
1) analytic one-particle saddle-node gold test: du/dt = f - sin(u), exact fc=1;
2) small quenched elastic line with a smooth random-bond-like potential;
3) bisection bracket width and time-step invariance gates.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

SEED = 20260902

# ---------------- Gold test: tilted washboard particle ----------------
def relax_particle(f, dt=0.02, max_steps=500_000, tol=2e-7,
                   disp_limit=4*math.pi, u0=0.0):
    u = float(u0)
    start = u
    stable = 0
    for step in range(max_steps):
        v = f - math.sin(u)
        if abs(v) < tol:
            stable += 1
            if stable >= 10:
                return "pinned", u, step + 1, abs(v), u - start
        else:
            stable = 0
        u += dt * v
        if u - start > disp_limit:
            return "moving", u, step + 1, abs(v), u - start
    return "uncertain", u, max_steps, abs(v), u - start


def particle_threshold(dt=0.02, lo=0.7, hi=1.25, n_iter=14):
    state, u_lo, *_ = relax_particle(lo, dt=dt)
    assert state == "pinned"
    state, *_ = relax_particle(hi, dt=dt, u0=u_lo)
    assert state == "moving"
    history = []
    for _ in range(n_iter):
        mid = 0.5 * (lo + hi)
        state, u_mid, steps, residual, disp = relax_particle(mid, dt=dt, u0=u_lo)
        if state == "pinned":
            lo, u_lo = mid, u_mid
        elif state == "moving":
            hi = mid
        else:
            raise RuntimeError(f"particle classification unresolved at f={mid}")
        history.append((lo, hi, mid, state, steps, residual, disp))
    return lo, hi, history


# ---------------- Quenched elastic line ----------------
def make_random_bond_force(L=32, M=256, du=0.25, rf=1.0, seed=SEED):
    """Smooth periodic random potential U_i(u), then Fp=-dU/du.

    The u-period is deliberately much larger than rf, so the local force is
    short-range correlated over the displacement window relevant here.
    This is a pedagogical RB-like disorder construction, not Ferrero's exact
    disorder generator.
    """
    rng = np.random.default_rng(seed)
    raw_U = rng.standard_normal((L, M))
    q = 2.0 * np.pi * np.fft.fftfreq(M, d=du)
    smooth = np.exp(-0.5 * (q * rf)**2)
    Uk = np.fft.fft(raw_U, axis=1) * smooth[None, :]
    Fp = np.fft.ifft((-1j * q)[None, :] * Uk, axis=1).real
    Fp /= Fp.std()
    return Fp, du


def pinning_force(u, table, du):
    L, M = table.shape
    pos = (u / du) % M
    i0 = np.floor(pos).astype(np.int64)
    frac = pos - i0
    i1 = (i0 + 1) % M
    ii = np.arange(L)
    return (1.0 - frac) * table[ii, i0] + frac * table[ii, i1]


def relax_line(f, table, du, c=1.0, dt=0.05, max_steps=500_000,
               tol=2e-7, u0=None):
    L, M = table.shape
    period = M * du
    # Requiring two full disorder periods of center-of-mass advance makes the
    # moving certificate deliberately conservative for this periodic box.
    disp_limit = 2.0 * period
    u = np.zeros(L) if u0 is None else np.array(u0, copy=True)
    com_start = float(u.mean())
    stable = 0
    for step in range(max_steps):
        fp = pinning_force(u, table, du)
        elastic = c * (np.roll(u, -1) + np.roll(u, 1) - 2.0*u)
        v = elastic + fp + f
        residual = float(np.max(np.abs(v)))
        if residual < tol:
            stable += 1
            if stable >= 10:
                return "pinned", u, step + 1, residual, float(u.mean() - com_start)
        else:
            stable = 0
        u += dt * v
        if float(u.mean() - com_start) > disp_limit:
            return "moving", u, step + 1, residual, float(u.mean() - com_start)
    return "uncertain", u, max_steps, residual, float(u.mean() - com_start)


def line_threshold(table, du, dt=0.05, lo=0.4, hi=1.0, n_iter=12):
    state, u_lo, *_ = relax_line(lo, table, du, dt=dt)
    assert state == "pinned"
    state, *_ = relax_line(hi, table, du, dt=dt, u0=u_lo)
    assert state == "moving"
    history = []
    last_pinned = u_lo.copy()
    last_moving = None
    for _ in range(n_iter):
        mid = 0.5 * (lo + hi)
        state, u_mid, steps, residual, disp = relax_line(mid, table, du, dt=dt, u0=u_lo)
        if state == "pinned":
            lo, u_lo = mid, u_mid
            last_pinned = u_mid.copy()
        elif state == "moving":
            hi = mid
            last_moving = u_mid.copy()
        else:
            raise RuntimeError(f"line classification unresolved at f={mid}")
        history.append((lo, hi, mid, state, steps, residual, disp))
    return lo, hi, history, last_pinned, last_moving


# ---------------- Run validation ladder ----------------
particle_runs = {}
for dt in (0.04, 0.02, 0.01):
    particle_runs[dt] = particle_threshold(dt=dt)
particle_mid = {dt: 0.5*(v[0]+v[1]) for dt, v in particle_runs.items()}
particle_err = max(abs(fc - 1.0) for fc in particle_mid.values())
particle_width = max(v[1]-v[0] for v in particle_runs.values())

L, M, du, rf = 32, 256, 0.25, 1.0
table, du = make_random_bond_force(L=L, M=M, du=du, rf=rf)
line_runs = {}
for dt in (0.10, 0.05, 0.025):
    line_runs[dt] = line_threshold(table, du, dt=dt)
line_mid = {dt: 0.5*(v[0]+v[1]) for dt, v in line_runs.items()}
line_spread = max(line_mid.values()) - min(line_mid.values())
line_width = max(v[1]-v[0] for v in line_runs.values())

# Hard gates fixed before interpreting the final line result.
assert particle_err < 5e-5, particle_err
assert particle_width < 5e-5, particle_width
assert line_width < 2e-4, line_width
assert line_spread < 5e-4, line_spread
assert all(v[0] < v[1] for v in line_runs.values())

fc_line = line_mid[0.05]
lo_line, hi_line, hist, pinned_u, moving_u = line_runs[0.05]
receipt_lines = [
    "Lesson 07 threshold-search validation",
    f"seed                        = {SEED}",
    "classifier residual tol     = 2.000e-07",
    "moving certificate          = COM advance > 2 u-periods",
    "particle exact fc           = 1.000000000",
]
for dt in (0.04, 0.02, 0.01):
    lo, hi, *_ = particle_runs[dt]
    receipt_lines.append(f"particle dt={dt:0.3f} bracket   = [{lo:.9f}, {hi:.9f}]")
receipt_lines += [
    f"particle max |fc-1|         = {particle_err:.3e}",
    f"line L, M, du, rf           = {L}, {M}, {du:.3f}, {rf:.3f}",
]
for dt in (0.10, 0.05, 0.025):
    lo, hi, *_ = line_runs[dt]
    receipt_lines.append(f"line dt={dt:0.3f} bracket       = [{lo:.9f}, {hi:.9f}]")
receipt_lines += [
    f"line fc midpoint (dt=.05)   = {fc_line:.9f}",
    f"line dt-spread              = {line_spread:.3e}",
    f"line final bracket width    = {line_width:.3e}",
    "THRESHOLD GOLD TEST + SMALL-LINE BRACKET PASS",
]
print("\n".join(receipt_lines))

# ---------------- Real matplotlib evidence plots ----------------
here = Path(__file__).resolve()
repo_root = here.parents[2] if here.parent.name == "reproduction-lab" else here.parent
out_dir = repo_root / "assets" / "reproduction-lab"
out_dir.mkdir(parents=True, exist_ok=True)
receipt_out = out_dir / "lesson07_threshold_search.txt"
receipt_out.write_text("\n".join(receipt_lines) + "\n", encoding="utf-8")

def finish(fig, name):
    fig.tight_layout()
    fig.savefig(out_dir/name, dpi=220, bbox_inches='tight')
    plt.close(fig)

# 1) What a pinned sample looks like at the upper edge of the bracket.
fig,ax=plt.subplots(figsize=(7.2,4.2))
x=np.arange(L)
ax.plot(x,pinned_u-pinned_u.mean(),marker='o',markersize=3)
ax.set_xlabel('x（格点编号）')
ax.set_ylabel(r'$u(x)-\langle u\rangle$')
ax.set_title(f'最后一个钉扎构型：f={lo_line:.6f}（一个无序样本）')
finish(fig,'lesson07_last_pinned_profile.png')

# 2) Bisection history: the two certified sides close onto each other.
it=np.arange(1,len(hist)+1)
los=np.array([h[0] for h in hist]); his=np.array([h[1] for h in hist])
fig,ax=plt.subplots(figsize=(7.2,4.3))
ax.plot(it,los,marker='o',label='最后一个钉扎点 f_minus')
ax.plot(it,his,marker='s',label='第一个运动点 f_plus')
ax.fill_between(it,los,his,alpha=.15,label='未决阈值区间')
ax.set_xlabel('二分迭代次数')
ax.set_ylabel('驱动力 f')
ax.set_title('单个淬火无序弹性界面的阈值搜索')
ax.legend()
finish(fig,'lesson07_bisection.png')

# 3) Time-step audit of the final bracket.  Use categorical x labels so the
# reader sees the actual dt values instead of log-axis powers of two.
dt_vals=np.array([0.10,0.05,0.025])
mid_vals=np.array([line_mid[d] for d in dt_vals])
half_width=np.array([(line_runs[d][1]-line_runs[d][0])/2 for d in dt_vals])
xpos=np.arange(len(dt_vals))
fig,ax=plt.subplots(figsize=(6.6,4.2))
ax.errorbar(xpos,mid_vals,yerr=half_width,marker='o',capsize=5)
ax.set_xticks(xpos,[f'{d:.3f}' for d in dt_vals])
ax.set_xlabel('积分步长 dt（向右减小）')
ax.set_ylabel('单样本阈值区间中点')
ax.set_title('减小 dt 后单样本阈值区间保持不变')
finish(fig,'lesson07_dt_threshold.png')

# 4) Analytic gold test: plot the tiny error from the exact fc=1 rather than
# a y axis near 1 with a confusing scientific-notation offset.
pdt=np.array([0.04,0.02,0.01])
pmid=np.array([particle_mid[d] for d in pdt])
phalf=np.array([(particle_runs[d][1]-particle_runs[d][0])/2 for d in pdt])
err_micro=(pmid-1.0)*1e6
half_micro=phalf*1e6
xpos=np.arange(len(pdt))
fig,ax=plt.subplots(figsize=(6.6,4.2))
ax.errorbar(xpos,err_micro,yerr=half_micro,marker='o',capsize=5,label='数值阈值区间')
ax.axhline(0.0,linestyle='--',label='解析值 fc=1')
ax.set_xticks(xpos,[f'{d:.3f}' for d in pdt])
ax.set_xlabel('积分步长 dt（向右减小）')
ax.set_ylabel(r'$10^6\,(f_{c,\mathrm{num}}-1)$')
ax.set_title('已知答案测试：数值阈值围绕解析 fc=1')
ax.legend()
finish(fig,'lesson07_particle_gold.png')

print('saved figures:', ', '.join(['lesson07_last_pinned_profile.png','lesson07_bisection.png','lesson07_dt_threshold.png','lesson07_particle_gold.png']))
print(f'saved receipt: {receipt_out}')
