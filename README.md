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

## Reproduction Lab

The site also contains a separate 12-lesson numerical-method track. It is a teaching and validation chain, **not a ninth first-level module** and not evidence by itself that a real sliding-ferroelectric wall belongs to the QEW universality class.

- **L01–L06 · Paper1 methods:** clean TDGL wall → 2D wall extraction → EW thermal roughening → GL→EW validity boundary → bulk-disorder projection → disordered geometry.
- **L07–L12 · Paper2 methods:** sample-dependent depinning threshold → steady velocity → β window audit → super-rough ζ measurement → finite-size threshold scaling / ν → thermal rounding and the creep boundary.

The Lab deliberately preserves failed gates. In particular, an effective exponent is never upgraded to a universal exponent merely because one fit is numerically close to a literature benchmark. Statistical independence is kept at the disorder-realization level rather than treating q bins, r bins, temperatures, or drive points as independent samples.

The Pages UI exposes the Lab in three places: the homepage top navigation, a dedicated homepage Lab card, and the persistent left-side all-pages navigation. On wide screens every page also has a right-side in-page table of contents; on narrow screens both sidebars become drawer buttons.

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

The current frontier conclusion is deliberately conservative: recent 3R-MoS₂ / h-BN work provides strong, mutually reinforcing evidence for domain-wall-mediated switching and pinning-sensitive dynamics, while a full universality test in a sliding-ferroelectric system still requires a common, material-grounded evidence chain such as constant-field `v(E)`, roughness `B(r)` / `S(q)`, correlation-length scaling and finite-size scaling. The Reproduction Lab demonstrates how to validate those estimators on controlled models; it does not substitute for that material-level evidence.

## Repository layout

- `index.html` — eight-module knowledge map, reading route, and prominent Reproduction Lab entry
- `curriculum.js` — curated paper/module metadata
- `modules/` — eight deep-reading modules, Research Track, and Reproduction Lab L01–L12 pages
- `examples/reproduction-lab/` — reproducible numerical lesson scripts
- `assets/` — frozen paper figures, lesson outputs, receipts, and raw tables
- `site-nav.js` / `site-nav.css` — persistent all-pages navigation and per-page contents navigation
- `.github/workflows/pages.yml` — static evidence/asset validation and GitHub Pages deployment

## Deployment

The site is dependency-free and deployed directly from `main` by `.github/workflows/pages.yml`.

The workflow checks internal image references, selectable source-text requirements, evidence-chain markers, L01–L12 receipts/raw-data cardinalities, cross-lesson links, and frozen/reused source assets before publishing. It does **not** download literature or generate/crop figures during deployment.
