# Disorder & RFIM lesson assets

Authoritative sources are PDFs inside the project Google Drive folder `sliding ferroelectric/`, under the depinning / elastic-interface / RFIM literature branch.

## Evidence policy

- Source passages in `modules/disorder-rfim.html` are selectable HTML text; paragraph screenshots are forbidden.
- Figure crops preserve axes, labels, legends and teaching-relevant panels. No scientific annotation is added.
- `drossel1998-fig3a-percolative-wall.png` is a direct lossless extraction of the PDF's embedded 400×400 1-bit figure object; it is intentionally not upscaled.
- GitHub Pages deploys frozen local assets only and does not download papers or regenerate figures.

## Frozen assets

- `dahmen1996-fig2-disorder-hysteresis.png` — Dahmen & Sethna (1996), Fig. 2: disorder-driven change from a macroscopic hysteresis jump through the critical endpoint to smooth response. Final deployed size: 15013 bytes. SHA256 `51c25a8d5932587447e29cd7d7928eb45520ced7cd6fa9ed03cf82d56a7017b7`.
- `drossel1998-fig3a-percolative-wall.png` — Drossel & Dahmen (1998), Fig. 3(a): percolative invaded region with internal unflipped bubbles. Final deployed size: 4690 bytes. SHA256 `65131f0b51238f1780ce4a2c24b4901bb0807fabf875b3232c2864f7749360c2`.
- `zhou2012-fig2-anomalous-roughness.png` — Zhou, Zheng & He, Drive arXiv version, Fig. 2: global roughness and local height-correlation scaling. Final deployed size: 4833 bytes. SHA256 `6e2aff6781b4f3b47248a533e1a270bea0e39683fc1e977d2cebb078f2826b31`.

## QA

The completed lesson was rendered locally at 1365 px desktop width and 412 px mobile width. The page has no horizontal overflow; all three figures remain legible and all source passages remain selectable text.

The byte sizes and SHA256 values above were rechecked against the actual GitHub Pages artifact produced from `main`, so the provenance record describes the deployed files rather than an earlier local conversion.