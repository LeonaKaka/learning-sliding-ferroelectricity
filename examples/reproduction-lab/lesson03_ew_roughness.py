#!/usr/bin/env python3
"""
Reproduction Lab · Lesson 03
Caballero et al. 2020 Eq. (15,17,19):
1D Edwards-Wilkinson thermal roughening from a flat interface.

Goal: reproduce the time-dependent roughness B(r,t) with a small,
CPU-fast simulation and compare directly against the paper's analytic Eq. (19).
This is a thumbnail reproduction of Fig. 2 logic, not the paper's full
L=4096, t<=1e6 protocol.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# Caballero Eq. (16) for alpha=delta=gamma=eta=1.
eta_tilde = 2.0 * math.sqrt(2.0) / 3.0
c = eta_tilde
T = 0.05
F = 0.0

# Small-system thumbnail. Paper: L=4096, dy=1, dt=1e-2.
N = 256
dy = 1.0
dt = 0.1
n_realizations = 64
target_times = (10.0, 100.0, 1000.0)
t_max = max(target_times)

rng = np.random.default_rng(12345)
u = np.zeros((n_realizations, N), dtype=np.float64)

# Discrete FDT for eta_tilde du/dt = c lap(u) + xi,
# <xi(y,t)xi(y',t')> = 2 eta_tilde T delta(y-y')delta(t-t').
noise_increment = math.sqrt(2.0 * T * dt / (eta_tilde * dy))


def roughness_B(interfaces, max_r=64):
    """Average B(r)=<[u(y+r)-u(y)]^2> over y and realizations."""
    r_index = np.arange(1, max_r + 1)
    B = np.array(
        [np.mean((np.roll(interfaces, -rr, axis=1) - interfaces) ** 2)
         for rr in r_index]
    )
    return r_index * dy, B


def analytic_B(r, t):
    """Caballero et al. Eq. (19), continuum EW line from a flat initial state."""
    r = np.asarray(r, dtype=float)
    z = math.sqrt(eta_tilde / (8.0 * c * t))
    s = z * r
    erf_s = np.array([math.erf(float(v)) for v in s])
    return (T * r / c) * (
        1.0
        - erf_s
        - (np.exp(-s * s) - 1.0) / (math.sqrt(math.pi) * s)
    )


snapshots = {}
n_steps = int(round(t_max / dt))
target_steps = {int(round(t / dt)): t for t in target_times}

for step in range(1, n_steps + 1):
    lap = (
        np.roll(u, -1, axis=1)
        - 2.0 * u
        + np.roll(u, 1, axis=1)
    ) / dy**2

    u += dt * (c / eta_tilde) * lap
    u += noise_increment * rng.standard_normal(u.shape)

    if step in target_steps:
        snapshots[target_steps[step]] = u.copy()

# --- Quantitative comparison ---
results = {}
for t in target_times:
    r, B_sim = roughness_B(snapshots[t], max_r=64)
    B_theory = analytic_B(r, t)

    # Predeclared window: skip the first few lattice spacings and stay below L/2.
    fit = (r >= 4.0) & (r <= 64.0)
    rel = np.abs(B_sim[fit] - B_theory[fit]) / B_theory[fit]
    results[t] = {
        "r": r,
        "sim": B_sim,
        "theory": B_theory,
        "median_rel": float(np.median(rel)),
        "rms_rel": float(np.sqrt(np.mean(rel**2))),
        "max_rel": float(np.max(rel)),
    }

# Late-time short-scale behavior should approach B_th(r)=T r/c.
r_late = results[1000.0]["r"]
B_late = results[1000.0]["sim"]
eq = T * r_late / c
local = (r_late >= 2.0) & (r_late <= 10.0)
late_ratio = float(np.mean(B_late[local] / eq[local]))

# --- Hard gates ---
for t in target_times:
    assert results[t]["median_rel"] < 0.03, (t, results[t]["median_rel"])
    assert results[t]["rms_rel"] < 0.04, (t, results[t]["rms_rel"])
assert 0.88 < late_ratio < 1.08, late_ratio

print(f"eta_tilde = c     = {c:.9f}")
print(f"T                 = {T:.3f}")
print(f"N, realizations   = {N}, {n_realizations}")
print(f"dy, dt            = {dy:.3f}, {dt:.3f}")
for t in target_times:
    print(
        f"t={t:6.1f}: median rel err={100*results[t]['median_rel']:.2f}%  "
        f"rms={100*results[t]['rms_rel']:.2f}%  "
        f"max={100*results[t]['max_rel']:.2f}%"
    )
print(f"late B/(Tr/c), r=2..10 = {late_ratio:.4f}")
print("ALL THUMBNAIL GATES PASS")

# --- Figure ---
here = Path(__file__).resolve()
if here.parent.name == "reproduction-lab" and here.parent.parent.name == "examples":
    repo_root = here.parents[2]
else:
    repo_root = here.parent
out_dir = repo_root / "assets" / "reproduction-lab"
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / "lesson03_ew_roughness_thumbnail.svg"

fig = plt.figure(figsize=(11.3, 7.2), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax = fig.add_subplot(gs[:, 0])
for t in target_times:
    rr = results[t]["r"]
    ax.loglog(rr, results[t]["sim"], marker="o", markersize=2.5, linewidth=1.1,
              label=f"数值模拟 t={t:g}")
    ax.loglog(rr, results[t]["theory"], linestyle="--", linewidth=1.6,
              label=f"Eq.19 t={t:g}")
ax.loglog(r_late, T*r_late/c, linestyle=":", linewidth=2.0, label=r"$B_{\rm th}=Tr/c$")
ax.set_xlabel("r")
ax.set_ylabel(r"$B(r,t)$")
ax.set_title("EW 粗糙度：数值模拟与 Caballero Eq. (19) 对照")
ax.legend(fontsize=7.5, ncol=2)

ax = fig.add_subplot(gs[0, 1])
for t in target_times:
    rr = results[t]["r"]
    rel = np.abs(results[t]["sim"] - results[t]["theory"]) / results[t]["theory"]
    ax.semilogx(rr, 100*rel, label=f"t={t:g}")
ax.axvspan(4, 64, alpha=0.08)
ax.set_xlabel("r")
ax.set_ylabel("|数值-理论| / 理论 (%)")
ax.set_title("预先声明的比较区间：4 ≤ r ≤ 64")
ax.legend(fontsize=8)

ax = fig.add_subplot(gs[1, 1])
offset = 0.0
for t in target_times:
    sample = snapshots[t][0] - snapshots[t][0].mean()
    ax.plot(np.arange(N), sample + offset, linewidth=0.8, label=f"t={t:g}")
    offset += 2.2
ax.set_xlim(0, N)
ax.set_xlabel("y")
ax.set_ylabel("u(y) + 纵向偏移")
ax.set_title("单个热噪声样本：粗糙度随时间增长")
ax.legend(fontsize=8)

fig.suptitle("复现实验室 · 第 03 课 · EW 热粗糙化缩略复现", fontsize=14)
fig.savefig(out)
print(f"saved: {out}")
