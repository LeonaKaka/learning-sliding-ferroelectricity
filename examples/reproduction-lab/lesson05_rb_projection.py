#!/usr/bin/env python3
"""
Reproduction Lab · Lesson 05
Caballero et al. 2020, Sec. IV / Eqs. (20)-(25) / Fig. 4 logic.

Goal
----
Start from continuum white random-bond disorder in the bulk and project it
onto the clean soliton profile. The resulting pinning force F_p(u,y) must
have the short-range correlator Gamma(u) predicted by Eq. (25).

This lesson intentionally uses the bulk-projection route (Eq. 23) rather
than the paper's direct spectral synthesis (Eq. 27). It therefore tests the
model-reduction step itself. The paper-size M=10000, du=0.1 and 256
independent realizations are cheap here because no time evolution is needed.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt

# Clean GL parameters used throughout Caballero 2020.
alpha = 1.0
delta = 1.0
gamma = 1.0
epsilon = 1.0
phi0 = math.sqrt(alpha / delta)
w = math.sqrt(2.0 * gamma / alpha)

# Fig. 4 uses M=10^4 and delta_l=0.1 with 256 realizations.
M = 10_000
du = 0.1
n_realizations = 256
rng = np.random.default_rng(20260901)

# Periodic transverse grid for the convolution. L is hundreds of wall widths,
# so the |u| <= 5 comparison window is insensitive to the periodic closure.
x = (np.arange(M) - M // 2) * du
z = np.clip(x / w, -350.0, 350.0)
sech2 = 1.0 / np.cosh(z) ** 2

# Caballero Eq. (7): phi*(x) = -phi0 tanh(x/w).
phi_prime = -(phi0 / w) * sech2
phi_second = (2.0 * phi0 / w**2) * sech2 * np.tanh(z)
projection_kernel = phi_prime * phi_second
K = np.fft.fft(projection_kernel)

# Eq. (25): Gamma(Delta u) = gamma^2 int dx k(x) k(x-Delta u).
Gamma = gamma**2 * du * np.fft.ifft(np.conj(K) * K).real

# Continuum white-noise discretization:
# <zeta(x) zeta(x')> = delta(x-x')  ->  Var[zeta_i] = 1/du.
base_normal = rng.standard_normal((n_realizations, M))
zeta = base_normal / math.sqrt(du)

# Eq. (23): Fp(u,y) = epsilon*gamma int dx zeta(x+u,y) k(x).
# A cyclic cross-correlation evaluates every u at once.
Fp = (
    epsilon
    * gamma
    * du
    * np.fft.ifft(np.fft.fft(zeta, axis=1) * np.conj(K)[None, :], axis=1).real
)

# Each realization supplies a force-force correlation as a function of Delta u.
Fp_fft = np.fft.fft(Fp, axis=1)
C_each = np.fft.ifft(np.abs(Fp_fft) ** 2, axis=1).real / M
C_avg = C_each.mean(axis=0)

# Deliberately wrong discretization: one N(0,1) per grid point, with no du^-1/2.
# Use the same base_normal so only the normalization changes.
zeta_wrong = base_normal
Fp_wrong = (
    epsilon
    * gamma
    * du
    * np.fft.ifft(
        np.fft.fft(zeta_wrong, axis=1) * np.conj(K)[None, :], axis=1
    ).real
)
C_wrong = np.mean(Fp_wrong**2)


def first_zero(arr, max_index=100):
    s0 = np.sign(arr[0])
    for i in range(1, max_index + 1):
        if np.sign(arr[i]) != s0:
            a, b = arr[i - 1], arr[i]
            frac = abs(a) / (abs(a) + abs(b))
            return (i - 1 + frac) * du
    raise RuntimeError("no zero crossing found in registered window")


# Predeclared comparison window: 0 <= Delta u <= 5.
window = np.arange(0, 51)
rmse_over_Gamma0 = float(
    np.sqrt(np.mean((C_avg[window] - Gamma[window]) ** 2)) / Gamma[0]
)
max_abs_over_Gamma0 = float(
    np.max(np.abs(C_avg[window] - Gamma[window])) / Gamma[0]
)
shape_rmse = float(
    np.sqrt(
        np.mean(
            (C_avg[window] / C_avg[0] - Gamma[window] / Gamma[0]) ** 2
        )
    )
)
amp_ratio = float(C_avg[0] / Gamma[0])
wrong_amp_ratio = float(C_wrong / Gamma[0])
theory_zero = first_zero(Gamma)
empirical_zero = first_zero(C_avg)

# Hard gates. These are intentionally much tighter than a visual comparison.
assert rmse_over_Gamma0 < 0.01, rmse_over_Gamma0
assert max_abs_over_Gamma0 < 0.015, max_abs_over_Gamma0
assert abs(empirical_zero - theory_zero) < 0.01, (empirical_zero, theory_zero)
assert 0.98 < amp_ratio < 1.02, amp_ratio
assert 0.09 < wrong_amp_ratio < 0.11, wrong_amp_ratio

print(f"phi0, w                 = {phi0:.6f}, {w:.6f}")
print(f"M, du, realizations     = {M}, {du:.3f}, {n_realizations}")
print(f"Gamma(0) theory         = {Gamma[0]:.9f}")
print(f"C(0)/Gamma(0)           = {amp_ratio:.6f}")
print(f"RMSE/Gamma(0), 0<=u<=5  = {100*rmse_over_Gamma0:.3f}%")
print(f"max abs/Gamma(0)        = {100*max_abs_over_Gamma0:.3f}%")
print(f"normalized-shape RMSE   = {100*shape_rmse:.3f}%")
print(f"first zero theory       = {theory_zero:.6f}")
print(f"first zero empirical    = {empirical_zero:.6f}")
print(f"WRONG std=1 amplitude   = {wrong_amp_ratio:.6f} x theory")
print("ALL DISORDER-PROJECTION GATES PASS")

# ----- Figure -----
here = Path(__file__).resolve()
repo_root = here.parents[2] if here.parent.name == "reproduction-lab" else here.parent
out_dir = repo_root / "assets" / "reproduction-lab"
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / "lesson05_rb_projection_correlator.svg"

u_plot = np.arange(0, 51) * du
fig = plt.figure(figsize=(11.4, 7.3), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax = fig.add_subplot(gs[:, 0])
for j in range(0, 64, 2):
    ax.plot(u_plot, C_each[j, :51], linewidth=0.55, alpha=0.18)
ax.plot(u_plot, C_avg[:51], linewidth=2.1, label="256-realization average")
ax.plot(u_plot, Gamma[:51], linestyle="--", linewidth=2.0, label="Eq. (25) theory")
ax.axhline(0.0, linewidth=0.7)
ax.set_xlabel("Delta u")
ax.set_ylabel("<Fp(u) Fp(u+Delta u)>")
ax.set_title("Projected pinning-force correlator")
ax.legend(fontsize=8)

ax = fig.add_subplot(gs[0, 1])
for j in range(4):
    start = M // 2
    ax.plot(np.arange(101) * du, Fp[j, start:start + 101], linewidth=1.0,
            label=f"realization {j+1}")
ax.set_xlabel("u")
ax.set_ylabel("Fp(u,y)")
ax.set_title("Four independent projected pinning forces")
ax.legend(fontsize=7)

ax = fig.add_subplot(gs[1, 1])
# Wrong normalization is exactly du times the correctly normalized covariance
# because the same underlying standard-normal field is reused.
C_wrong_curve = C_avg[:51] * du
ax.plot(u_plot, Gamma[:51], linestyle="--", linewidth=2.0, label="Eq. (25)")
ax.plot(u_plot, C_avg[:51], linewidth=1.8, label="correct white-noise scaling")
ax.plot(u_plot, C_wrong_curve, linewidth=1.8, label="wrong: std=1 per grid point")
ax.axhline(0.0, linewidth=0.7)
ax.set_xlabel("Delta u")
ax.set_ylabel("correlator")
ax.set_title("Discretization trap: missing du^(-1/2)")
ax.legend(fontsize=7)

fig.suptitle("Reproduction Lab · Lesson 05 · bulk RB disorder -> correlated pinning force", fontsize=14)
fig.savefig(out)
print(f"saved: {out}")
