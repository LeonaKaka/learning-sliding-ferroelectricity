"""
Reproduction Lab · Lesson 01
Caballero et al. (2020): clean 1D Ginzburg–Landau domain wall

Goal
----
Start from an intentionally too-wide wall, evolve overdamped TDGL at h=T=0,
and verify that the numerical stationary profile converges to

    phi*(x) = -phi0 tanh(x / w)
    phi0 = sqrt(alpha / delta)
    w    = sqrt(2 gamma / alpha)

This is a pedagogical reduction of the clean bulk model used in Caballero et al.
It is NOT yet their full 2D GL ↔ elastic-line simulation.
"""

import numpy as np
import matplotlib.pyplot as plt

alpha = 1.0
delta = 1.0
gamma = 1.0
eta = 1.0

phi0 = np.sqrt(alpha / delta)
w_exact = np.sqrt(2.0 * gamma / alpha)

Lx = 40.0
Nx = 401
x = np.linspace(-Lx / 2, Lx / 2, Nx)
dx = x[1] - x[0]

dt = 0.15 * dx**2 * eta / gamma
n_steps = 15_000

# Deliberately start with a wall three times too wide.
phi = -phi0 * np.tanh(x / (3.0 * w_exact))
phi[0] = +phi0
phi[-1] = -phi0

snapshots = {}
energies = []

for step in range(n_steps + 1):
    if step in (0, 200, 1000, 5000, 15000):
        snapshots[step] = phi.copy()

    if step % 50 == 0:
        grad = np.diff(phi) / dx
        V = -0.5 * alpha * phi**2 + 0.25 * delta * phi**4
        F = 0.5 * gamma * np.sum(grad**2) * dx + np.sum(V) * dx
        energies.append((step * dt, F))

    if step == n_steps:
        break

    lap = (phi[2:] - 2.0 * phi[1:-1] + phi[:-2]) / dx**2
    rhs = (
        gamma * lap
        + alpha * phi[1:-1]
        - delta * phi[1:-1] ** 3
    ) / eta

    phi[1:-1] += dt * rhs
    phi[0] = +phi0
    phi[-1] = -phi0

phi_exact = -phi0 * np.tanh(x / w_exact)
mask = np.abs(x) <= 6.0 * w_exact
rmse = np.sqrt(np.mean((phi[mask] - phi_exact[mask]) ** 2))

i0 = np.argmin(np.abs(x))
dphi0 = (phi[i0 + 1] - phi[i0 - 1]) / (2.0 * dx)
w_num = abs(phi0 / dphi0)
width_error = abs(w_num - w_exact) / w_exact

print(f"dx                = {dx:.4f}")
print(f"dt                = {dt:.6f}")
print(f"analytic width    = {w_exact:.6f}")
print(f"numerical width   = {w_num:.6f}")
print(f"relative w error  = {100 * width_error:.4f}%")
print(f"profile RMSE      = {rmse:.3e}")

assert rmse < 5e-4
assert width_error < 5e-3

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
for step in (0, 200, 1000, 5000, 15000):
    ax1.plot(x, snapshots[step], label=f"t={step * dt:.1f}")
ax1.plot(x, phi_exact, "--", linewidth=2, label="解析扭结")
ax1.set_xlim(-7, 7)
ax1.set_xlabel("x")
ax1.set_ylabel("φ")
ax1.set_title("畴壁剖面弛豫")
ax1.legend(fontsize=8)

times = np.array([t for t, _ in energies])
free_energy = np.array([F for _, F in energies])
ax2.plot(times, free_energy - free_energy[-1])
ax2.set_yscale("log")
ax2.set_xlabel("t")
ax2.set_ylabel("F(t) - F(final)")
ax2.set_title("TDGL 下自由能下降")

fig.tight_layout()
fig.savefig("lesson01_tdgl_wall_result.png", dpi=180)
plt.show()
