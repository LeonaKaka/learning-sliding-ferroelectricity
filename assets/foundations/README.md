# Foundations static evidence assets

These files are frozen teaching assets for `modules/foundations.html`.

The authoritative sources are the copies already stored in the project Google Drive folder `sliding ferroelectric/` and its project subfolders. GitHub Pages does not download papers or generate/crop figures during deployment.

## Presentation rule

- Published-paper paragraphs are presented as selectable, searchable HTML text, transcribed from the authoritative Drive PDFs in the paper's reading order.
- When a paragraph crosses columns or pages, the page labels explicitly say `跨栏拼接` or `跨栏/跨页拼接，原文未改`.
- Figures are rendered from the corresponding Drive PDF pages at 600 DPI and frozen as lossless PNG files. They are not converted to low-bitrate WebP or otherwise lossily recompressed for deployment.
- Every accepted crop is visually checked for panel boundaries, labels, axes, color bars, arrows, text and neighboring-panel contamination.
- The lesson links each figure to its repository file at original resolution so it can be opened separately and inspected closely.

## Current Foundations figure set

- Wu & Li 2021 — `wu2021-fig1-mechanism.png` — 2720×1940
- Yasuda et al. 2021 — `yasuda2021-fig1-stacking.png` — 4350×2080
- Vizner Stern et al. 2021 — `vizner2021-fig2-domains.png` — 2910×1910
- Meng et al. 2022 — `meng2022-fig3e-multistate.png` — 4040×1490; panel e crop, adjacent Fig. 3d axis excluded
- Ji et al. 2023 — `ji2023-fig1-principles.png` — 3460×2920

The five PNG byte streams were transferred into the repository through a one-time workflow and checked against local SHA-256 values before commit. That transfer workflow removed itself after the verified commit. The permanent Pages workflow only validates local image references and deploys the static site.
