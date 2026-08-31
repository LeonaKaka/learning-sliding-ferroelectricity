# Learning Sliding Ferroelectricity

A literature-first teaching site for learning how sliding ferroelectrics switch, from stacking physics to domain-wall dynamics, disorder and depinning.

GitHub Pages: `https://leonakaka.github.io/learning-sliding-ferroelectricity/`

## Learning route

The V1 knowledge tree is organized as eight first-level modules:

1. **What is Sliding FE?** — stacking, symmetry and polarization
2. **Switching Pathways** — intermediate states and pathway selection
3. **Domain Walls** — what actually moves under the electric field
4. **Pinning, Creep & Roughness** — real walls in a disorder landscape
5. **Depinning** — threshold, critical geometry and finite-size scaling
6. **Disorder & RFIM** — disorder-controlled switching and the limits of elastic-line language
7. **Numerical Modeling** — phase field / TDGL → emergent interface → grid/disorder sanity checks
8. **Current Frontiers** — evidence audit of 2025–2026 sliding-FE work and the remaining universality gap

Every module has a dedicated deep-reading page under `modules/`.

## Editorial / evidence policy

This is a learning site, not a paper gallery.

- Core claims are tied to authoritative paper text and figures.
- Original paper wording is kept as selectable HTML text, not paragraph screenshots.
- Scientific figures are frozen local assets from the project literature PDFs; the deployment workflow never downloads or crops papers.
- Figure crops preserve scientific content: axes, legends, panel labels and data are not casually removed or redrawn.
- Pages distinguish **direct evidence**, **authors' interpretation**, and **our teaching connection**.
- Similar words are not treated as equivalent evidence: e.g. `avalanchelike`, `superlubric`, a single pinning/depinning event, and a critical depinning universality class are separate claims.
- Numerical-modeling sections distinguish continuum physical disorder strength from grid-level noise amplitude and require dx/dt/size/seed convergence logic.

## Current scientific spine

The site now connects this causal chain:

**stacking → symmetry breaking → polarization → switching pathway → pre-existing domain wall → pinning / creep → depinning → disorder / RFIM → phase-field / elastic-interface modeling → frontier evidence audit**

The current frontier conclusion is deliberately conservative: recent 3R-MoS₂ / h-BN work provides strong, mutually reinforcing evidence for domain-wall-mediated switching and pinning-sensitive dynamics, while a full universality test still requires a common set of observables such as constant-field `v(E)`, roughness `B(r)` / `S(q)`, correlation-length scaling and finite-size scaling.

## Repository layout

- `index.html` — eight-module knowledge map and reading route
- `curriculum.js` — curated paper/module metadata
- `modules/` — deep-reading lesson pages
- `assets/` — frozen paper figures and provenance notes
- `.github/workflows/pages.yml` — static evidence/asset validation and GitHub Pages deployment

## Deployment

The site is dependency-free and deployed directly from `main` by `.github/workflows/pages.yml`.

The workflow checks internal image references, selectable source-text requirements, evidence-chain markers, and frozen/reused source assets before publishing. It does **not** download literature or generate/crop figures during deployment.
