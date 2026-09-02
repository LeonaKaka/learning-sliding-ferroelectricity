#!/usr/bin/env python3
"""
Reproduction Lab · Lesson 02
Caballero et al. 2020 clean GL model:
2D bulk field -> extracted interface u(y) -> flat-wall roughness B(r) ~ 0.

This is a small-system gold test, not a full reproduction of the paper's
large-system finite-temperature/disordered figures.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt

# --- Caballero clean phi^4 / Model-A parameters ---
alpha = 1.0
delta = 1.0
gamma = 1.0
eta = 1.0
phi0 = math.sqrt(alpha / delta)
w_exact = math.sqrt(2.0 * gamma / alpha)

# --- Small, fast 2D grid ---
Lx, Ly = 48.0, 24.0
dx, dy = 0.20, 0.50
dt = 0.004
steps = 22_000

x = np.arange(-Lx / 2, Lx / 2 + 0.5 * dx, dx)
y = np.arange(0.0, Ly, dy)
X = x[:, None]

# Deliberately start from a wavy wall so the 2D solver must flatten it.
u_initial = 1.5 * np.sin(2.0 * np.pi * y / Ly)
phi = -phi0 * np.tanh((X - u_initial[None, :]) / w_exact)
phi[0, :] = +phi0
phi[-1, :] = -phi0


def free_energy(field):
    V = -0.5 * alpha * field**2 + 0.25 * delta * field**4
    dphidx = (field[1:, :] - field[:-1, :]) / dx
    dphidy = (np.roll(field, -1, axis=1) - field) / dy
    return (
        np.sum(V) * dx * dy
        + 0.5 * gamma * np.sum(dphidx**2) * dx * dy
        + 0.5 * gamma * np.sum(dphidy**2) * dx * dy
    )


def extract_zero_crossing(field):
    """One linear-interpolated phi=0 crossing per y column."""
    u = np.empty(field.shape[1])
    for j in range(field.shape[1]):
        col = field[:, j]
        ids = np.where((col[:-1] >= 0.0) & (col[1:] < 0.0))[0]
        if len(ids) != 1:
            raise RuntimeError(
                f"column {j}: expected exactly one wall crossing, found {len(ids)}"
            )
        i = ids[0]
        u[j] = x[i] - col[i] * (x[i + 1] - x[i]) / (col[i + 1] - col[i])
    return u


def roughness_B(u):
    """Periodic B(r)=< [u(y+r)-u(y)]^2 >_y."""
    k = np.arange(1, len(u) // 2 + 1)
    r = k * dy
    B = np.array([np.mean((np.roll(u, -kk) - u) ** 2) for kk in k])
    return r, B


energy_t = [0.0]
energy_F = [free_energy(phi)]

for n in range(1, steps + 1):
    lap_x = (phi[2:, :] - 2.0 * phi[1:-1, :] + phi[:-2, :]) / dx**2
    lap_y = (
        np.roll(phi[1:-1, :], -1, axis=1)
        - 2.0 * phi[1:-1, :]
        + np.roll(phi[1:-1, :], 1, axis=1)
    ) / dy**2

    rhs = (
        gamma * (lap_x + lap_y)
        + alpha * phi[1:-1, :]
        - delta * phi[1:-1, :] ** 3
    ) / eta

    phi[1:-1, :] += dt * rhs
    phi[0, :] = +phi0
    phi[-1, :] = -phi0

    if n % 500 == 0:
        energy_t.append(n * dt)
        energy_F.append(free_energy(phi))

u_final = extract_zero_crossing(phi)
r0, B0 = roughness_B(u_initial)
r, B = roughness_B(u_final)

# Mean transverse profile should still be the analytic kink.
mean_profile = phi.mean(axis=1)
analytic = -phi0 * np.tanh(x / w_exact)
fit_mask = np.abs(x) < 8.0
profile_rmse = float(
    np.sqrt(np.mean((mean_profile[fit_mask] - analytic[fit_mask]) ** 2))
)
wall_rms = float(np.std(u_final))
wall_max = float(np.max(np.abs(u_final)))
B_max = float(np.max(B))
energy_drop = float(energy_F[0] - energy_F[-1])

# --- Hard gates ---
assert wall_rms < 5e-3, wall_rms
assert wall_max < 8e-3, wall_max
assert B_max < 5e-5, B_max
assert profile_rmse < 8e-4, profile_rmse
assert energy_drop > 0.0, energy_drop
assert np.all(np.diff(energy_F) <= 2e-9), "sampled free energy is not monotone"

print(f"grid              = {len(x)} x {len(y)}")
print(f"dx, dy            = {dx:.3f}, {dy:.3f}")
print(f"dt, steps         = {dt:.4f}, {steps}")
print(f"analytic width    = {w_exact:.6f}")
print(f"final wall RMS    = {wall_rms:.6e}")
print(f"max |u(y)|        = {wall_max:.6e}")
print(f"max B(r)          = {B_max:.6e}")
print(f"profile RMSE      = {profile_rmse:.6e}")
print(f"free-energy drop  = {energy_drop:.6f}")
print("ALL HARD GATES PASS")

# --- Figure ---
here = Path(__file__).resolve()
if here.parent.name == "reproduction-lab" and here.parent.parent.name == "examples":
    repo_root = here.parents[2]
else:
    repo_root = here.parent
out_dir = repo_root / "assets" / "reproduction-lab"
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / "lesson02_2d_wall_extract.svg"
fig = plt.figure(figsize=(11.5, 8.4), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax = fig.add_subplot(gs[0, 0])
im = ax.imshow(
    phi.T,
    origin="lower",
    aspect="auto",
    extent=[x[0], x[-1], y[0], y[-1] + dy],
    vmin=-1,
    vmax=1,
)
ax.plot(u_final, y + 0.5 * dy, linewidth=1.5, label=r"提取的 $u(y)$")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("弛豫后的二维体场")
ax.legend(loc="upper right", fontsize=8)
fig.colorbar(im, ax=ax, shrink=0.8, label=r"$\phi(x,y)$")

ax = fig.add_subplot(gs[0, 1])
ax.plot(y, u_initial, label="初始起伏畴壁")
ax.plot(y, u_final, label="最终提取畴壁")
ax.axhline(0.0, linewidth=1, linestyle="--")
ax.set_xlabel("y")
ax.set_ylabel("u(y)")
ax.set_title("弥散场 → 单值界面")
ax.legend(fontsize=8)

ax = fig.add_subplot(gs[1, 0])
ax.semilogy(r0, B0, marker="o", markersize=3, label="初始")
ax.semilogy(r, B, marker="o", markersize=3, label="最终")
ax.set_xlabel("r")
ax.set_ylabel(r"$B(r)$")
ax.set_title(r"平直畴壁已知答案测试：$B(r)\rightarrow0$")
ax.legend(fontsize=8)

ax = fig.add_subplot(gs[1, 1])
ax.plot(x, mean_profile, label="数值平均剖面")
ax.plot(x, analytic, linestyle="--", label="解析 tanh")
ax.set_xlim(-6, 6)
ax.set_xlabel("x")
ax.set_ylabel(r"$\phi$")
ax.set_title(f"横向剖面 RMSE = {profile_rmse:.2e}")
ax.legend(fontsize=8)

fig.suptitle(
    "复现实验室 · 第 02 课 · 二维 GL 场 → u(y) → B(r)",
    fontsize=14,
)
fig.savefig(out, dpi=170)
print(f"saved: {out}")
