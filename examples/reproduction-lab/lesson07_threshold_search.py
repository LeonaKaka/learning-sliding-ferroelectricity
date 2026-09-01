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

# ---------------- Compact SVG figure ----------------
def map_points(xs, ys, x0, y0, width, height, xmin, xmax, ymin, ymax):
    pts = []
    for xv, yv in zip(xs, ys):
        X = x0 + (xv - xmin) / (xmax - xmin) * width
        Y = y0 + height - (yv - ymin) / (ymax - ymin) * height
        pts.append(f"{X:.1f},{Y:.1f}")
    return " ".join(pts)

here = Path(__file__).resolve()
repo_root = here.parents[2] if here.parent.name == "reproduction-lab" else here.parent
out_dir = repo_root / "assets" / "reproduction-lab"
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / "lesson07_threshold_search.svg"

sine_x = np.linspace(0.0, 2.0*np.pi, 61)
sine_y = np.sin(sine_x)
pinned_centered = pinned_u - pinned_u.mean()
iterations = np.arange(1, len(hist) + 1)
los = np.array([h[0] for h in hist])
his = np.array([h[1] for h in hist])
mids = 0.5 * (los + his)

sine_pts = map_points(sine_x, sine_y, 55,70,410,180,0,2*np.pi,-1.1,1.1)
prof_pts = map_points(np.arange(L), pinned_centered, 560,70,410,180,0,L-1,-4,5.5)
low_pts = map_points(iterations, los, 55,340,410,180,1,len(hist),0.69,1.01)
hi_pts = map_points(iterations, his, 55,340,410,180,1,len(hist),0.69,1.01)
mid_pts = map_points(iterations, mids, 55,340,410,180,1,len(hist),0.69,1.01)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="600" viewBox="0 0 1050 600" role="img" aria-label="Lesson 07 threshold validation">
<style>text{{font-family:system-ui,-apple-system,sans-serif;fill:#20211f}} .ax{{stroke:#444;stroke-width:1}} .curve{{fill:none;stroke:#333;stroke-width:2}} .dash{{stroke-dasharray:7 5}} .muted{{fill:#716d66;font-size:12px}} .ttl{{font-size:18px;font-weight:650}} .lab{{font-size:13px}} .box{{fill:#fffdf8;stroke:#d8d1c3}}</style>
<rect width="1050" height="600" fill="#fff"/><text x="525" y="30" text-anchor="middle" font-size="22">Reproduction Lab · Lesson 07 · finite-sample depinning threshold</text>
<rect class="box" x="35" y="45" width="450" height="235" rx="8"/><text class="ttl" x="55" y="65">Gold test: exact saddle-node threshold</text><line class="ax" x1="55" y1="250" x2="465" y2="250"/><line class="ax" x1="55" y1="70" x2="55" y2="250"/><polyline class="curve" points="{sine_pts}"/><line class="curve dash" x1="55" y1="78.2" x2="465" y2="78.2"/><text class="lab" x="62" y="92">exact f_c = 1</text><text class="muted" x="55" y="272">numerical midpoint error = {particle_err:.2e}</text>
<rect class="box" x="540" y="45" width="475" height="235" rx="8"/><text class="ttl" x="560" y="65">Last pinned configuration, same quenched sample</text><line class="ax" x1="560" y1="250" x2="970" y2="250"/><line class="ax" x1="560" y1="70" x2="560" y2="250"/><polyline class="curve" points="{prof_pts}"/><text class="muted" x="560" y="272">L={L} · random-bond-like smooth potential · f−={lo_line:.9f}</text>
<rect class="box" x="35" y="315" width="450" height="235" rx="8"/><text class="ttl" x="55" y="335">Pinned / moving bracket contracts monotonically</text><line class="ax" x1="55" y1="520" x2="465" y2="520"/><line class="ax" x1="55" y1="340" x2="55" y2="520"/><polyline points="{low_pts}" fill="none" stroke="#777" stroke-width="1.3"/><polyline points="{hi_pts}" fill="none" stroke="#777" stroke-width="1.3"/><polyline class="curve" points="{mid_pts}"/><text class="muted" x="55" y="542">{len(hist)} bisections → width {line_width:.3e}</text>
<rect class="box" x="540" y="315" width="475" height="235" rx="8"/><text class="ttl" x="560" y="335">Time-step invariance gate</text><text x="580" y="390" font-size="17">dt = 0.100</text><text x="770" y="390" font-size="17">{line_mid[0.10]:.9f}</text><text x="580" y="430" font-size="17">dt = 0.050</text><text x="770" y="430" font-size="17">{line_mid[0.05]:.9f}</text><text x="580" y="470" font-size="17">dt = 0.025</text><text x="770" y="470" font-size="17">{line_mid[0.025]:.9f}</text><line x1="755" y1="505" x2="955" y2="505" stroke="#333" stroke-width="2"/><text class="muted" x="560" y="532">midpoint spread = {line_spread:.3e}</text></svg>'''
out.write_text(svg, encoding="utf-8")
receipt_out = out_dir / "lesson07_threshold_search.txt"
receipt_out.write_text("\n".join(receipt_lines) + "\n", encoding="utf-8")
print(f"saved figure:  {out}")
print(f"saved receipt: {receipt_out}")
