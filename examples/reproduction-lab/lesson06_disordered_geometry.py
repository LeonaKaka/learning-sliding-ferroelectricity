#!/usr/bin/env python3
"""
Reproduction Lab · Lesson 06
Caballero et al. 2020 Fig. 5 logic at a CPU-fast checkpoint.

We evolve
  (a) the 2D disordered Ginzburg-Landau bulk model, and
  (b) the mapped 1D Edwards-Wilkinson interface with correlated pinning,
at T=0.05 and epsilon=0.1 from a flat wall.

The goal is deliberately split in two:
  1) Cross-model geometry mapping at t=1000 must pass using BOTH B(r) and S(q).
  2) The asymptotic random-bond exponent zeta=2/3 is NOT declared passed unless
     B and S give compatible effective exponents in the same scaling regime.

This is a thumbnail checkpoint, not the paper's Lx=256, Ly=4096, t<=1e6 run.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ---------------- Paper parameters ----------------
alpha = delta = gamma = eta = 1.0
phi0 = 1.0
w_exact = math.sqrt(2.0)
eta_tilde = c = 2.0 * math.sqrt(2.0) / 3.0
T = 0.05
epsilon = 0.1

# ---------------- Thumbnail geometry ----------------
dx = dy = 1.0
dt = 0.1
Lx, Ly = 64.0, 128.0
x = np.arange(-Lx / 2.0, Lx / 2.0 + 0.5 * dx, dx)
Nx = x.size
Ny = int(round(Ly / dy))
n_realizations = 8
t_final = 1000.0
n_steps = int(round(t_final / dt))

# ---------------- Semi-implicit 2D GL solver ----------------
# Linear Laplacian is implicit, exactly as in Lesson 04's validated solver.
n_int = Nx - 2
n_freq = Ny // 2 + 1
rx = dt * gamma / (eta * dx**2)
mode = np.arange(n_freq)
lambda_y = 4.0 * np.sin(np.pi * mode / Ny) ** 2 / dy**2
diag = 1.0 + 2.0 * rx + dt * gamma * lambda_y / eta
off = -rx

inv_den = np.empty((n_int, n_freq))
cprime = np.empty((n_int, n_freq))
inv_den[0] = 1.0 / diag
cprime[0] = off * inv_den[0]
for i in range(1, n_int):
    den_i = diag - off * cprime[i - 1]
    inv_den[i] = 1.0 / den_i
    cprime[i] = off * inv_den[i]


def run_disordered_gl(seed=100):
    rng = np.random.default_rng(seed)
    base = -np.tanh(x[:, None] / w_exact)
    phi = np.broadcast_to(base, (n_realizations, Nx, Ny)).copy()
    phi[:, 0, :] = +phi0
    phi[:, -1, :] = -phi0

    # Eq. (20) bulk RB disorder. Here dx=dy=1, so the continuum-white
    # cell-average standard deviation happens numerically to be 1.
    zeta = rng.standard_normal(phi.shape)
    zeta[:, 0, :] = 0.0
    zeta[:, -1, :] = 0.0

    noise_increment = math.sqrt(2.0 * T * dt / (eta * dx * dy))
    forward = np.empty((n_realizations, n_int, n_freq), dtype=np.complex128)
    solution = np.empty_like(forward)

    for _ in range(n_steps):
        interior = phi[:, 1:-1, :]
        zint = zeta[:, 1:-1, :]

        # -d[V(phi)(1+epsilon*zeta)]/dphi
        local_force = (1.0 + epsilon * zint) * (
            alpha * interior - delta * interior**3
        )
        rhs = interior + dt / eta * local_force
        rhs += noise_increment * rng.standard_normal(rhs.shape)

        rhs[:, 0, :] += rx * (+phi0)
        rhs[:, -1, :] += rx * (-phi0)
        rhs_k = np.fft.rfft(rhs, axis=2)

        forward[:, 0, :] = rhs_k[:, 0, :] * inv_den[0][None, :]
        for i in range(1, n_int):
            forward[:, i, :] = (
                rhs_k[:, i, :] - off * forward[:, i - 1, :]
            ) * inv_den[i][None, :]

        solution[:, -1, :] = forward[:, -1, :]
        for i in range(n_int - 2, -1, -1):
            solution[:, i, :] = (
                forward[:, i, :] - cprime[i][None, :] * solution[:, i + 1, :]
            )

        phi[:, 1:-1, :] = np.fft.irfft(solution, n=Ny, axis=2)
        phi[:, 0, :] = +phi0
        phi[:, -1, :] = -phi0

    return phi


def soliton(xv, A, width, u):
    return -A * np.tanh((xv - u) / width)


def extract_interface(field):
    """Paper-style finite-T estimator: fit {A,w,u(y)} in every y-column."""
    nr, _, ny = field.shape
    U = np.full((nr, ny), np.nan)
    Afit = np.full_like(U, np.nan)
    Wfit = np.full_like(U, np.nan)
    fit_rmse = np.full_like(U, np.nan)

    for a in range(nr):
        for j in range(ny):
            profile = field[a, :, j]
            candidates = np.where(profile[:-1] * profile[1:] <= 0.0)[0]
            if candidates.size == 0:
                continue
            i0 = candidates[np.argmin(np.abs(x[candidates]))]
            p1, p2 = profile[i0], profile[i0 + 1]
            u0 = x[i0] + dx * (-p1) / (p2 - p1 + 1e-15)
            mask = (x >= u0 - 6.0) & (x <= u0 + 6.0)

            try:
                pars, _ = curve_fit(
                    soliton,
                    x[mask],
                    profile[mask],
                    p0=(1.0, w_exact, u0),
                    bounds=((0.35, 0.25, u0 - 3.0), (1.7, 5.0, u0 + 3.0)),
                    maxfev=5000,
                )
            except (RuntimeError, ValueError):
                continue

            A, width, u = pars
            pred = soliton(x[mask], A, width, u)
            U[a, j] = u
            Afit[a, j] = A
            Wfit[a, j] = width
            fit_rmse[a, j] = np.sqrt(np.mean((pred - profile[mask]) ** 2))

    return U, Afit, Wfit, fit_rmse


# ---------------- Mapped 1D EW with correlated pinning ----------------
def build_pinning_table(seed=200):
    rng = np.random.default_rng(seed)
    du = 0.1
    M = 1024
    ugrid = (np.arange(M) - M // 2) * du
    z = np.clip(ugrid / w_exact, -350.0, 350.0)
    sech2 = 1.0 / np.cosh(z) ** 2
    phi_prime = -(phi0 / w_exact) * sech2
    phi_second = (2.0 * phi0 / w_exact**2) * sech2 * np.tanh(z)
    kernel = phi_prime * phi_second
    K = np.fft.fft(kernel)

    # Eq. (23): independent bulk-white disorder for each y, projected to Fp(u,y).
    base = rng.standard_normal((n_realizations, Ny, M))
    zeta = base / math.sqrt(du)
    Ftable = (
        epsilon
        * gamma
        * du
        * np.fft.ifft(
            np.fft.fft(zeta, axis=2) * np.conj(K)[None, None, :], axis=2
        ).real
    )
    return rng, Ftable, du, M


def run_disordered_ew():
    rng, Ftable, du, M = build_pinning_table()
    u = np.zeros((n_realizations, Ny), dtype=float)
    noise_increment = math.sqrt(2.0 * T * dt / (eta_tilde * dy))
    ridx = np.arange(n_realizations)[:, None]
    yidx = np.arange(Ny)[None, :]

    for _ in range(n_steps):
        lap = np.roll(u, -1, axis=1) - 2.0 * u + np.roll(u, 1, axis=1)

        pos = (u / du + M / 2.0) % M
        i0 = np.floor(pos).astype(np.int64)
        frac = pos - i0
        i1 = (i0 + 1) % M
        fp = (
            (1.0 - frac) * Ftable[ridx, yidx, i0]
            + frac * Ftable[ridx, yidx, i1]
        )

        u += dt / eta_tilde * (c * lap + fp)
        u += noise_increment * rng.standard_normal(u.shape)

    return u


# ---------------- Observables ----------------
def roughness_B(U, max_r=64):
    r = np.arange(1, max_r + 1, dtype=float)
    B = np.array([
        np.mean((np.roll(U, -int(rr), axis=1) - U) ** 2)
        for rr in r
    ])
    return r * dy, B


def structure_factor(U):
    centered = U - U.mean(axis=1, keepdims=True)
    Uq = np.fft.rfft(centered, axis=1)
    S = np.mean(np.abs(Uq) ** 2 / Ny, axis=0)
    q = 2.0 * np.pi * np.arange(Uq.shape[1]) / Ly
    return q[1:], S[1:]


def log_bin(q, S, n_bins=8, qmin=0.08, qmax=1.5):
    edges = np.geomspace(qmin, qmax, n_bins + 1)
    qb, sb = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (q >= lo) & (q < hi)
        if np.any(mask):
            qb.append(float(np.exp(np.mean(np.log(q[mask])))))
            sb.append(float(np.exp(np.mean(np.log(S[mask])))))
    return np.array(qb), np.array(sb)


def symmetric_relative(a, b):
    return np.abs(a - b) / (0.5 * (a + b))


# ---------------- Run + analyze ----------------
phi_final = run_disordered_gl()
U_gl, A_gl, W_gl, profile_rmse_gl = extract_interface(phi_final)
assert np.isfinite(U_gl).all(), "GL wall fit failed in at least one column"
U_ew = run_disordered_ew()

r, B_gl = roughness_B(U_gl)
_, B_ew = roughness_B(U_ew)
q, S_gl = structure_factor(U_gl)
_, S_ew = structure_factor(U_ew)
qb_gl, Sb_gl = log_bin(q, S_gl)
qb_ew, Sb_ew = log_bin(q, S_ew)
assert np.allclose(qb_gl, qb_ew)

# Cross-model mapping gates at the same t=1000 checkpoint.
b_window = (r >= 4.0) & (r <= 32.0)
B_median_rel = float(np.median(symmetric_relative(B_gl[b_window], B_ew[b_window])))
S_binned_median_rel = float(np.median(symmetric_relative(Sb_gl, Sb_ew)))

# Effective exponents are diagnostics, NOT the main gate.
b_fit = (r >= 4.0) & (r <= 20.0)
zeta_B_gl = float(np.polyfit(np.log(r[b_fit]), np.log(B_gl[b_fit]), 1)[0] / 2.0)
zeta_B_ew = float(np.polyfit(np.log(r[b_fit]), np.log(B_ew[b_fit]), 1)[0] / 2.0)
q_fit = (q >= 0.1) & (q <= 0.5)
zeta_S_gl = float((-np.polyfit(np.log(q[q_fit]), np.log(S_gl[q_fit]), 1)[0] - 1.0) / 2.0)
zeta_S_ew = float((-np.polyfit(np.log(q[q_fit]), np.log(S_ew[q_fit]), 1)[0] - 1.0) / 2.0)

A_mean = float(np.mean(A_gl))
W_mean = float(np.mean(W_gl))
profile_rmse = float(np.mean(profile_rmse_gl))

# Mapping must pass in both real and Fourier space.
assert B_median_rel < 0.05, B_median_rel
assert S_binned_median_rel < 0.10, S_binned_median_rel
assert abs(zeta_B_gl - zeta_B_ew) < 0.06
assert abs(zeta_S_gl - zeta_S_ew) < 0.06
assert 0.95 < A_mean < 1.02
assert 1.20 < W_mean < 1.50

# Deliberately DO NOT assert zeta=2/3. At this thumbnail time/size, B and S
# still give different effective exponents: this is the crossover warning.
assert abs(zeta_B_gl - zeta_S_gl) > 0.10
assert abs(zeta_B_ew - zeta_S_ew) > 0.10

print("Caballero Fig.5 geometry checkpoint")
print(f"T, epsilon, t          = {T:.3f}, {epsilon:.3f}, {t_final:.1f}")
print(f"GL size / EW length    = {int(Lx)}x{Ny} / {Ny}")
print(f"realizations           = {n_realizations}")
print(f"B median rel, r=4..32  = {100*B_median_rel:.3f}%")
print(f"S log-bin median rel   = {100*S_binned_median_rel:.3f}%")
print(f"zeta_B GL / EW         = {zeta_B_gl:.6f} / {zeta_B_ew:.6f}")
print(f"zeta_S GL / EW         = {zeta_S_gl:.6f} / {zeta_S_ew:.6f}")
print(f"GL fitted A, w         = {A_mean:.6f}, {W_mean:.6f}")
print(f"GL profile-fit RMSE    = {profile_rmse:.6f}")
print("CROSS-MODEL GEOMETRY PASS; ASYMPTOTIC ZETA GATE NOT PASSED")

# ---------------- Figure ----------------
here = Path(__file__).resolve()
repo_root = here.parents[2] if here.parent.name == "reproduction-lab" else here.parent
out_dir = repo_root / "assets" / "reproduction-lab"
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / "lesson06_disordered_geometry_checkpoint.svg"

fig, axes = plt.subplots(2, 2, figsize=(11.4, 8.2), constrained_layout=True)

ax = axes[0, 0]
ax.loglog(r, B_gl, linewidth=1.8, label="2D GL extracted wall")
ax.loglog(r, B_ew, linestyle="--", linewidth=1.8, label="1D EW")
ax.loglog(r, (T / c) * r, linestyle=":", linewidth=1.5, label="thermal Tr/c")
# A slope guide only; amplitude anchored at r=10, not a fit claim.
rref = np.array([6.0, 28.0])
anchor_r = 10.0
anchor_B = np.interp(anchor_r, r, 0.5 * (B_gl + B_ew))
ax.loglog(rref, anchor_B * (rref / anchor_r) ** (4.0 / 3.0), linestyle="-.", linewidth=1.3,
          label="slope guide: r^(4/3)")
ax.axvspan(4.0, 32.0, alpha=0.06)
ax.set_xlabel("r")
ax.set_ylabel("B(r,t)")
ax.set_title("Real-space roughness at t=1000")
ax.legend(fontsize=7)

ax = axes[0, 1]
ax.loglog(q, S_gl, linewidth=1.2, label="2D GL")
ax.loglog(q, S_ew, linestyle="--", linewidth=1.2, label="1D EW")
ax.scatter(qb_gl, Sb_gl, s=20, label="GL log bins")
ax.scatter(qb_ew, Sb_ew, s=20, marker="x", label="EW log bins")
ax.axvspan(0.1, 0.5, alpha=0.06)
ax.set_xlabel("q")
ax.set_ylabel("S(q,t)")
ax.set_title("Fourier-space structure factor")
ax.legend(fontsize=7)

ax = axes[1, 0]
ax.plot(np.arange(Ny), U_gl[0] - U_gl[0].mean(), linewidth=1.0, label="GL realization 1")
ax.plot(np.arange(Ny), U_ew[0] - U_ew[0].mean(), linewidth=1.0, label="EW realization 1")
ax.set_xlabel("y")
ax.set_ylabel("u(y)-mean(u)")
ax.set_title("Representative interfaces")
ax.legend(fontsize=7)

ax = axes[1, 1]
labels = ["zeta_B GL", "zeta_B EW", "zeta_S GL", "zeta_S EW", "2/3"]
vals = [zeta_B_gl, zeta_B_ew, zeta_S_gl, zeta_S_ew, 2.0 / 3.0]
ax.bar(np.arange(len(vals)), vals)
ax.set_xticks(np.arange(len(vals)), labels, rotation=24, ha="right")
ax.set_ylim(0.0, 0.8)
ax.set_ylabel("effective zeta")
ax.set_title("Mapping passes before asymptotic exponent closes")

fig.suptitle("Reproduction Lab · Lesson 06 · disordered GL vs EW geometry", fontsize=14)
fig.savefig(out)
print(f"saved: {out}")
