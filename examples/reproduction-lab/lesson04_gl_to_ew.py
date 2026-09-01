#!/usr/bin/env python3
"""
Reproduction Lab · Lesson 04
Caballero et al. 2020 clean 2D Ginzburg-Landau -> 1D interface mapping.

Two deliberately different regimes:
  T=0.05 : low-temperature mapping should agree with EW Eq. (19).
  T=0.30 : small-noise / elastic-line reduction should visibly deteriorate.

This is a CPU-fast boundary thumbnail, not the paper's full
Lx=256, Ly=4096, t=1e3 temperature sweep.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- Paper model: alpha=delta=gamma=eta=1, h=0 ---
alpha = delta = gamma = eta = 1.0
phi0_exact = 1.0
w_exact = math.sqrt(2.0)
eta_tilde = c = 2.0 * math.sqrt(2.0) / 3.0

# --- Small thumbnail geometry ---
dx = dy = 1.0
dt = 0.1
Lx, Ly = 64.0, 128.0
x = np.arange(-Lx / 2.0, Lx / 2.0 + 0.5 * dx, dx)
Nx = x.size
Ny = int(round(Ly / dy))
n_realizations = 12
target_times = (10.0, 100.0)
max_r = 48

# Paper uses semi-implicit Euler in Fourier space.
# Here the linear 2D Laplacian is treated implicitly:
# periodic y is diagonalized by FFT; Dirichlet x is solved by a
# precomputed tridiagonal Thomas factorization for every y-mode.
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


def run_gl(T, seed):
    base = -np.tanh(x[:, None] / w_exact)
    phi = np.broadcast_to(base, (n_realizations, Nx, Ny)).copy()
    phi[:, 0, :] = +phi0_exact
    phi[:, -1, :] = -phi0_exact

    rng = np.random.default_rng(seed)
    # Eq. (4) discretized in 2D:
    # <xi xi> = 2 eta T delta^2(r-r') delta(t-t')
    noise_increment = math.sqrt(2.0 * T * dt / (eta * dx * dy))

    snapshots = {}
    target_steps = {int(round(t / dt)): t for t in target_times}
    n_steps = max(target_steps)

    forward = np.empty((n_realizations, n_int, n_freq), dtype=np.complex128)
    solution = np.empty_like(forward)

    for step in range(1, n_steps + 1):
        interior = phi[:, 1:-1, :]
        rhs = interior + dt / eta * (alpha * interior - delta * interior**3)
        rhs += noise_increment * rng.standard_normal(rhs.shape)

        # Known Dirichlet boundaries enter the implicit x solve.
        rhs[:, 0, :] += rx * (+phi0_exact)
        rhs[:, -1, :] += rx * (-phi0_exact)

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
        phi[:, 0, :] = +phi0_exact
        phi[:, -1, :] = -phi0_exact

        if step in target_steps:
            snapshots[target_steps[step]] = phi.copy()

    return snapshots


def soliton(xv, A, w, u):
    return -A * np.tanh((xv - u) / w)


def extract_interface(field):
    """
    Paper-inspired estimator:
    for every y-column, fit phi(x) to -A tanh[(x-u)/w],
    with {A,w,u} free. A zero crossing is used only to initialize
    the nonlinear fit; it is NOT the final wall estimator.
    """
    nr, _, ny = field.shape
    U = np.full((nr, ny), np.nan)
    Afit = np.full_like(U, np.nan)
    Wfit = np.full_like(U, np.nan)
    fit_rmse = np.full_like(U, np.nan)
    crossing_count = np.zeros((nr, ny), dtype=int)

    for a in range(nr):
        for j in range(ny):
            profile = field[a, :, j]
            candidates = np.where(profile[:-1] * profile[1:] <= 0.0)[0]
            crossing_count[a, j] = candidates.size
            if candidates.size == 0:
                continue

            # Initialize near the central wall.
            i0 = candidates[np.argmin(np.abs(x[candidates]))]
            p1, p2 = profile[i0], profile[i0 + 1]
            u0 = x[i0] + dx * (-p1) / (p2 - p1 + 1e-15)
            mask = (x >= u0 - 5.0) & (x <= u0 + 5.0)

            try:
                pars, _ = curve_fit(
                    soliton,
                    x[mask],
                    profile[mask],
                    p0=(1.0, w_exact, u0),
                    bounds=((0.5, 0.4, u0 - 2.0), (1.5, 3.5, u0 + 2.0)),
                    maxfev=1500,
                )
            except (RuntimeError, ValueError):
                continue

            A, w, u = pars
            pred = soliton(x[mask], A, w, u)
            U[a, j] = u
            Afit[a, j] = A
            Wfit[a, j] = w
            fit_rmse[a, j] = np.sqrt(np.mean((pred - profile[mask]) ** 2))

    return U, Afit, Wfit, fit_rmse, crossing_count


def roughness_B(U, max_r=max_r):
    rr = np.arange(1, max_r + 1)
    BB = np.array([
        np.nanmean((np.roll(U, -r, axis=1) - U) ** 2)
        for r in rr
    ])
    return rr * dy, BB


def ew_eq19(r, t, T):
    r = np.asarray(r, dtype=float)
    z = math.sqrt(eta_tilde / (8.0 * c * t))
    s = z * r
    erf_s = np.array([math.erf(float(v)) for v in s])
    return (T * r / c) * (
        1.0
        - erf_s
        - (np.exp(-s * s) - 1.0) / (math.sqrt(math.pi) * s)
    )


def analyze(T, seed):
    snapshots = run_gl(T, seed)
    out = {}
    for t in target_times:
        U, A, W, fit_rmse, crossings = extract_interface(snapshots[t])
        assert np.isfinite(U).all(), f"T={T}, t={t}: fit failure"
        r, B = roughness_B(U)
        theory = ew_eq19(r, t, T)
        window = (r >= 4.0) & (r <= 32.0)
        rel = np.abs(B[window] - theory[window]) / theory[window]
        out[t] = {
            "U": U, "A": A, "W": W, "fit_rmse": fit_rmse,
            "crossings": crossings, "r": r, "B": B, "theory": theory,
            "median_rel": float(np.median(rel)),
            "rms_rel": float(np.sqrt(np.mean(rel**2))),
            "max_rel": float(np.max(rel)),
            "A_mean": float(np.nanmean(A)), "A_std": float(np.nanstd(A)),
            "W_mean": float(np.nanmean(W)), "W_std": float(np.nanstd(W)),
            "profile_rmse": float(np.nanmean(fit_rmse)),
            "multi_cross": float(np.mean(crossings > 1)),
        }
    return out


low = analyze(0.05, seed=123)
high = analyze(0.30, seed=456)

# --- Hard gates ---
# Low-T mapping: small-system GL must be close to EW prediction.
for t in target_times:
    assert low[t]["median_rel"] < 0.10, (t, low[t]["median_rel"])
    assert low[t]["rms_rel"] < 0.10, (t, low[t]["rms_rel"])
assert 0.95 < low[100.0]["A_mean"] < 1.02
assert 1.20 < low[100.0]["W_mean"] < 1.50
assert low[100.0]["multi_cross"] < 0.01

# High-T stress test: do NOT force an elastic-line pass.
assert high[100.0]["median_rel"] > 0.30
assert high[100.0]["W_std"] > 2.0 * low[100.0]["W_std"]
assert high[100.0]["multi_cross"] > 0.03

print("Caballero low-T bulk->line thumbnail")
for T, data, label in ((0.05, low, "LOW-T"), (0.30, high, "HIGH-T")):
    for t in target_times:
        d = data[t]
        print(
            f"{label} T={T:.2f} t={t:5.1f}: "
            f"median={100*d['median_rel']:.2f}% "
            f"rms={100*d['rms_rel']:.2f}% "
            f"A={d['A_mean']:.4f}+/-{d['A_std']:.4f} "
            f"w={d['W_mean']:.4f}+/-{d['W_std']:.4f} "
            f"multi={100*d['multi_cross']:.2f}%"
        )
print("LOW-T MAPPING PASS; HIGH-T BREAKDOWN DETECTED")

# --- Figure ---
here = Path(__file__).resolve()
if here.parent.name == "reproduction-lab" and here.parent.parent.name == "examples":
    repo_root = here.parents[2]
else:
    repo_root = here.parent
out_dir = repo_root / "assets" / "reproduction-lab"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "lesson04_gl_to_ew_boundary.svg"

fig, axes = plt.subplots(2, 2, figsize=(11.4, 8.0), constrained_layout=True)

for ax, T, data, title in (
    (axes[0, 0], 0.05, low, "Low T: bulk GL follows EW"),
    (axes[0, 1], 0.30, high, "High T: mapping breaks down"),
):
    for t in target_times:
        d = data[t]
        ax.loglog(d["r"], d["B"], "o-", markersize=2.6, linewidth=1.0,
                  label=f"GL fit-u, t={t:g}")
        ax.loglog(d["r"], d["theory"], "--", linewidth=1.5,
                  label=f"EW Eq.19, t={t:g}")
    ax.set_xlabel("r")
    ax.set_ylabel("B(r,t)")
    ax.set_title(title)
    ax.legend(fontsize=7.5)

ax = axes[1, 0]
bins = np.linspace(0.4, 3.5, 42)
ax.hist(low[100.0]["W"].ravel(), bins=bins, alpha=0.65, density=True, label="T=0.05")
ax.hist(high[100.0]["W"].ravel(), bins=bins, alpha=0.55, density=True, label="T=0.30")
ax.axvline(w_exact, linestyle="--", linewidth=1.5, label=r"$w=\sqrt{2}$")
ax.set_xlabel("fitted wall width w")
ax.set_ylabel("density")
ax.set_title("Profile-fit diagnostic")
ax.legend(fontsize=8)

ax = axes[1, 1]
labels = ["median\nEq.19 error", "multi-\ncrossing", "width\nstd / sqrt(2)"]
lowvals = [
    100 * low[100.0]["median_rel"],
    100 * low[100.0]["multi_cross"],
    100 * low[100.0]["W_std"] / w_exact,
]
highvals = [
    100 * high[100.0]["median_rel"],
    100 * high[100.0]["multi_cross"],
    100 * high[100.0]["W_std"] / w_exact,
]
xx = np.arange(3)
width = 0.36
ax.bar(xx - width / 2, lowvals, width, label="T=0.05")
ax.bar(xx + width / 2, highvals, width, label="T=0.30")
ax.set_xticks(xx, labels)
ax.set_ylabel("%")
ax.set_title("The mapping fails before we force a zeta fit")
ax.legend(fontsize=8)

fig.suptitle("Reproduction Lab · Lesson 04 · 2D GL -> 1D EW validity boundary", fontsize=14)
fig.savefig(out_path)
print(f"saved: {out_path}")
