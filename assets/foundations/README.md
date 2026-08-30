# Foundations static evidence assets

These files are frozen teaching assets for `modules/foundations.html`.

Authoritative source PDFs are the copies already stored in the project Google Drive folder `sliding ferroelectric/` and its project subfolders. They are not downloaded again during GitHub Pages deployment.

Production rule used for this set:

1. open the Drive PDF used by the project;
2. render the source page at 600 DPI;
3. crop the complete paragraph / figure / panel needed for one teaching question;
4. visually inspect labels, axes, color bars, arrows, text, borders, and neighboring panels;
5. re-crop if needed;
6. freeze the accepted result here as a repository asset;
7. Pages only validates references and deploys the static site.

## Source-to-asset map

- Wu & Li 2021, *Sliding ferroelectricity in 2D van der Waals materials: Related physics and future opportunities*
  - `wu2021-paragraph-model.png`
  - `wu2021-fig1-mechanism.webp`
- Yasuda et al. 2021, *Stacking-engineered ferroelectricity in bilayer boron nitride*
  - `yasuda2021-paragraph-stacking.png`
  - `yasuda2021-fig1-stacking.webp`
- Vizner Stern et al. 2021, *Interfacial ferroelectricity by van der Waals sliding*
  - `vizner2021-paragraph-domains.png`
  - `vizner2021-fig2-domains.webp`
- Meng et al. 2022, *Sliding induced multiple polarization states in two-dimensional ferroelectrics*
  - `meng2022-paragraph-multistate-part1.png` … `part8.png` — main-text argument kept in reading order across columns/pages; original wording unchanged
  - `meng2022-fig3e-multistate.webp` — panel e only; adjacent panel axis removed during crop QA
- Ji et al. 2023, *General Theory for Bilayer Stacking Ferroelectricity*
  - `ji2023-paragraph-general-theory.png`
  - `ji2023-fig1-principles.webp`

Paragraph screenshots remain screenshots of the published PDFs; no OCR text is substituted for the source paragraph. GitHub Pages performs no paper download and no image generation/cropping.
