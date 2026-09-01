#!/usr/bin/env python3
"""
Reproduction Lab · Lesson 05
Caballero et al. 2020 Eqs. (23)-(27), Figure 4 logic:
bulk random-bond disorder -> finite-correlated interface pinning force.

Three independent checks are kept separate:
  1) direct real-space Eq. (25) using the analytic soliton derivatives;
  2) the Fourier spectrum Eq. (27) on the discrete periodic u grid;
  3) the sample autocorrelation of 256 generated pinning-force realizations.

We use the GL-consistent parameters alpha=delta=gamma=1 from Lessons 1-4,
so w=sqrt(2) and D=2/9. The paper also gives a separate synthetic generator
example with D=1; D rescales the covariance amplitude but not its normalized
shape for fixed w. Keeping those conventions separate avoids a hidden
normalization switch.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt

alpha = delta = gamma = 1.0
epsilon = 1.0
w = math.sqrt(2.0 * gamma / alpha)
D = 2.0 * alpha**3 * gamma / (9.0 * delta**2)

# Paper Fig.4 uses 256 independent correlations, M=1e4 and du=0.1.
# We preserve the 256 independent realizations and du=0.1 but use M=4096
# for a CPU-fast thumbnail. L=409.6 is still >> the wall width.
M = 4096
du = 0.1
L = M * du
n_realizations = 256
rng = np.random.default_rng(20260901)


def g_spectrum(q, wall_width):
    """Caballero Eq. (27): Gamma_hat(q)=D*g(q,w)^2."""
    q = np.asarray(q, dtype=float)
    z = wall_width * q
    out = np.zeros_like(z)
    nz = np.abs(z) > 1e-12
    out[nz] = (
        np.pi / (8.0 * wall_width)
        * z[nz] ** 2
        * (z[nz] ** 2 + 4.0)
        / np.sinh(np.pi * z[nz] / 2.0)
    )
    # The q->0 limit is zero.
    return out


def soliton_kernel(x):
    """gamma*phi_star'(x)*phi_star''(x) entering Eq. (25)."""
    t = x / w
    sech2 = 1.0 / np.cosh(t) ** 2
    phi_prime = -(1.0 / w) * sech2
    phi_second = (2.0 / w**2) * sech2 * np.tanh(t)
    return gamma * phi_prime * phi_second


# ---------------------------------------------------------------------
# A. Eq. (27) -> discrete periodic target covariance.
# ---------------------------------------------------------------------
q = 2.0 * np.pi * np.fft.rfftfreq(M, d=du)
g = g_spectrum(q, w)

# For F(u)=eps*sqrt(D/L)*sum_q exp(i q u) g(q) z_q,
# np.fft.irfft needs coefficients multiplied by M because irfft carries 1/M.
# Positive-frequency z_q have E|z_q|^2=1 and Hermitian symmetry is supplied
# by irfft. The Nyquist coefficient is real with unit variance.
z = (
    rng.standard_normal((n_realizations, q.size))
    + 1j * rng.standard_normal((n_realizations, q.size))
) / math.sqrt(2.0)
z[:, 0] = 0.0
if M % 2 == 0:
    z[:, -1] = rng.standard_normal(n_realizations)

coeff = M * epsilon * math.sqrt(D / L) * g[None, :] * z
forces = np.fft.irfft(coeff, n=M, axis=1)

# Periodic discrete covariance implied by Eq. (27).
gamma_spectral = (
    epsilon**2 * D / L * M * np.fft.irfft(g**2, n=M)
)

# ---------------------------------------------------------------------
# B. Sample correlation of each generated pinning force.
# ---------------------------------------------------------------------
force_fft = np.fft.rfft(forces, axis=1)
corr_each = np.fft.irfft(np.abs(force_fft) ** 2, n=M, axis=1) / M
corr_average = corr_each.mean(axis=0)

# ---------------------------------------------------------------------
# C. Independent direct Eq. (25) real-space integral.
# ---------------------------------------------------------------------
u_check = np.arange(0.0, 5.0 + 0.5 * du, du)
x_dense = np.arange(-20.0, 20.0 + 0.001, 0.002)
k0 = soliton_kernel(x_dense)
gamma_direct = np.array([
    epsilon**2 * np.trapezoid(k0 * soliton_kernel(x_dense - shift), x_dense)
    for shift in u_check
])

n_check = u_check.size
spectral_rms = float(
    np.sqrt(np.mean((gamma_spectral[:n_check] - gamma_direct) ** 2))
    / gamma_direct[0]
)
sample_rms = float(
    np.sqrt(np.mean((corr_average[:n_check] - gamma_direct) ** 2))
    / gamma_direct[0]
)
sample_max = float(
    np.max(np.abs(corr_average[:n_check] - gamma_direct))
    / gamma_direct[0]
)
amplitude_error = float(abs(corr_average[0] - gamma_direct[0]) / gamma_direct[0])
mean_force = float(np.mean(forces))

# Useful geometry of the short-range correlator.
zc = np.where(gamma_direct[:-1] * gamma_direct[1:] < 0.0)[0][0]
zero_crossing = float(
    u_check[zc]
    + du * (-gamma_direct[zc]) / (gamma_direct[zc + 1] - gamma_direct[zc])
)
min_idx = int(np.argmin(gamma_direct))
minimum_u = float(u_check[min_idx])
minimum_gamma = float(gamma_direct[min_idx])

# D=1 synthetic rescaling: same normalized shape, different amplitude.
gamma_D1 = gamma_spectral * (1.0 / D)
shape_diff = float(np.max(np.abs(
    gamma_D1[:n_check] / gamma_D1[0]
    - gamma_spectral[:n_check] / gamma_spectral[0]
)))

# ---------------------------------------------------------------------
# Hard gates.
# ---------------------------------------------------------------------
assert spectral_rms < 1e-10, spectral_rms
assert sample_rms < 0.015, sample_rms
assert sample_max < 0.025, sample_max
assert amplitude_error < 0.02, amplitude_error
assert abs(mean_force) < 1e-12, mean_force
assert 0.9 < zero_crossing < 1.2, zero_crossing
assert 1.5 < minimum_u < 2.1, minimum_u
assert shape_diff < 1e-12, shape_diff

print(f"w                 = {w:.9f}")
print(f"D (GL mapping)    = {D:.9f}")
print(f"M, du, L          = {M}, {du:.3f}, {L:.1f}")
print(f"realizations      = {n_realizations}")
print(f"Gamma(0) direct   = {gamma_direct[0]:.9f}")
print(f"Gamma(0) sample   = {corr_average[0]:.9f}")
print(f"Eq25-vs-Eq27 RMS  = {100*spectral_rms:.6f}% of Gamma(0)")
print(f"sample RMS error  = {100*sample_rms:.3f}% of Gamma(0)")
print(f"sample max error  = {100*sample_max:.3f}% of Gamma(0)")
print(f"amplitude error   = {100*amplitude_error:.3f}%")
print(f"zero crossing     = {zero_crossing:.4f} = {zero_crossing/w:.3f} w")
print(f"negative minimum  = u={minimum_u:.2f}, Gamma={minimum_gamma:.6f}")
print(f"mean force        = {mean_force:.3e}")
print("PINNING-CORRELATOR GOLD TEST PASS")

# ---------------------------------------------------------------------
# Figure: paper-Fig4-like structure plus normalization diagnostics.
# ---------------------------------------------------------------------
here = Path(__file__).resolve()
if here.parent.name == "reproduction-lab" and here.parent.parent.name == "examples":
    repo_root = here.parents[2]
else:
    repo_root = here.parent
out_dir = repo_root / "assets" / "reproduction-lab"
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / "lesson05_pinning_correlator.svg"

fig = plt.figure(figsize=(11.4, 7.6), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax = fig.add_subplot(gs[:, 0])
for i in range(min(64, n_realizations)):
    ax.plot(u_check, corr_each[i, :n_check], linewidth=0.45, alpha=0.16)
ax.plot(u_check, corr_average[:n_check], linewidth=2.0, label="average of 256")
ax.plot(u_check, gamma_direct, "--", linewidth=2.0, label="Eq.25 direct")
ax.plot(u_check, gamma_spectral[:n_check], ":", linewidth=1.8, label="Eq.27 spectral")
ax.axhline(0.0, linewidth=0.7)
ax.set_xlabel(r"$u_2-u_1$")
ax.set_ylabel(r"$\langle F_p(u_1)F_p(u_2)\rangle$")
ax.set_title("Pinning-force correlator: three independent checks")
ax.legend(fontsize=8)

ax = fig.add_subplot(gs[0, 1])
show_u = np.arange(0.0, 10.0, du)
for i in range(4):
    ax.plot(show_u, forces[i, :show_u.size], linewidth=1.0)
ax.set_xlabel("u")
ax.set_ylabel(r"$F_p(u)$")
ax.set_title("Four quenched pinning-force realizations")

ax = fig.add_subplot(gs[1, 1])
ax.plot(u_check / w, gamma_spectral[:n_check] / gamma_spectral[0], label="GL D=2/9")
ax.plot(u_check / w, gamma_D1[:n_check] / gamma_D1[0], "--", label="synthetic D=1")
ax.axvline(zero_crossing / w, linestyle=":", linewidth=1.2)
ax.set_xlabel(r"$u/w$")
ax.set_ylabel(r"$\Gamma(u)/\Gamma(0)$")
ax.set_title("D changes amplitude; wall width sets correlation shape")
ax.legend(fontsize=8)

fig.suptitle("Reproduction Lab · Lesson 05 · bulk RB -> correlated interface pinning", fontsize=14)
fig.savefig(out)
print(f"saved: {out}")
