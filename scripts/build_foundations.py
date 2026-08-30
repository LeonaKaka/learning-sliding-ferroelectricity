from pathlib import Path
import fitz
from PIL import Image, ImageDraw, ImageOps

OUT = Path('assets/foundations')
OUT.mkdir(parents=True, exist_ok=True)
DPI = 600
SCALE = DPI / 72


def trim(im, margin=30, threshold=246):
    gray = ImageOps.grayscale(im)
    mask = gray.point(lambda x: 255 if x < threshold else 0)
    box = mask.getbbox()
    if not box:
        return im
    l, t, r, b = box
    return im.crop((max(0, l-margin), max(0, t-margin), min(im.width, r+margin), min(im.height, b+margin)))


def render(page, rect, maxw=1800):
    pix = page.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=rect, alpha=False)
    im = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.Resampling.LANCZOS)
    return im


def save(im, name, quality=92):
    p = OUT / name
    im.save(p, 'WEBP', quality=quality, method=6)
    if p.stat().st_size < 18_000:
        raise RuntimeError(f'suspicious asset {name}: {p.stat().st_size}')
    print(name, im.size, p.stat().st_size)


def stitch(parts, name, maxw=1500):
    parts = [trim(x) for x in parts]
    gap = 56
    w = max(x.width for x in parts)
    h = sum(x.height for x in parts) + gap * (len(parts)-1)
    canvas = Image.new('RGB', (w, h), 'white')
    y = 0
    for i, x in enumerate(parts):
        canvas.paste(x, ((w-x.width)//2, y))
        y += x.height
        if i < len(parts)-1:
            ImageDraw.Draw(canvas).line((30, y+gap//2, w-30, y+gap//2), fill=(214,214,214), width=2)
            y += gap
    if canvas.width > maxw:
        canvas = canvas.resize((maxw, round(canvas.height * maxw / canvas.width)), Image.Resampling.LANCZOS)
    save(canvas, name)


def page_with(doc, needle):
    needle = needle.lower()
    for p in doc:
        if needle in p.get_text().lower():
            return p
    raise RuntimeError(f'cannot find page containing {needle!r}')


def block_with(page, needle):
    needle = needle.lower()
    for b in page.get_text('blocks', sort=True):
        if needle in b[4].lower():
            return b
    raise RuntimeError(f'cannot find block {needle!r} on page {page.number+1}')


def largest_image_rect(page):
    infos = page.get_image_info(xrefs=True)
    if not infos:
        raise RuntimeError(f'no image on page {page.number+1}')
    info = max(infos, key=lambda x: (x['bbox'][2]-x['bbox'][0]) * (x['bbox'][3]-x['bbox'][1]))
    return fitz.Rect(info['bbox'])


# Wu & Li 2021. NSF PAR author copy is used because PNAS blocks GitHub Actions.
wu = fitz.open('/tmp/foundations/wu2021.pdf')
p = page_with(wu, 'According to the model of sliding ferroelectricity')
left = block_with(p, 'According to the model of sliding ferroelectricity')
start = p.search_for('According to the model of sliding ferroelectricity')[0]
end_hits = p.search_for('down layer, as shown in Fig. 1A') or p.search_for('down layer, as shown in Fig. 1A.')
if not end_hits:
    raise RuntimeError('Wu paragraph end not found')
end = end_hits[-1]
if end.x0 >= start.x0 and end.y0 >= start.y0:
    save(trim(render(p, fitz.Rect(left[0], start.y0-2, left[2], end.y1+3), 1800)), 'wu2021-paragraph-model.webp')
else:
    blocks = p.get_text('blocks', sort=True)
    right_candidates = [b for b in blocks if b[0] > p.rect.width/2 and ('symmetry' in b[4].lower() or 'polarization' in b[4].lower())]
    if not right_candidates:
        raise RuntimeError('Wu continuation block not found')
    right = right_candidates[0]
    a = render(p, fitz.Rect(left[0], start.y0-2, left[2], left[3]), 1800)
    b = render(p, fitz.Rect(right[0], right[1], right[2], end.y1+3), 1800)
    stitch([a, b], 'wu2021-paragraph-model.webp')
figp = page_with(wu, 'Fig. 1. Mechanism of sliding ferroelectricity')
save(render(figp, largest_image_rect(figp), 1800), 'wu2021-fig1-mechanism.webp')

# Yasuda 2021 — public arXiv author manuscript. Keep the whole abstract paragraph.
yas = fitz.open('/tmp/foundations/yasuda2021.pdf')
p = page_with(yas, '2D ferroelectrics with robust polarization')
b = block_with(p, '2D ferroelectrics with robust polarization')
save(trim(render(p, fitz.Rect(b[0], b[1], b[2], b[3]), 1800)), 'yasuda2021-paragraph-abstract.webp')
figp = page_with(yas, 'Fig. 1. Ferroelectricity of AB-stacked bilayer boron nitride')
save(render(figp, largest_image_rect(figp), 1800), 'yasuda2021-fig1-stacking.webp')

# Vizner Stern 2021 — public arXiv manuscript. Keep the whole abstract paragraph.
viz = fitz.open('/tmp/foundations/vizner2021.pdf')
p = page_with(viz, 'Despite their ionic nature')
b = block_with(p, 'Despite their ionic nature')
save(trim(render(p, fitz.Rect(b[0], b[1], b[2], b[3]), 1800)), 'vizner2021-paragraph-abstract.webp')
figp = page_with(viz, 'Fig. 2. Direct measurement of interfacial polarization')
save(render(figp, largest_image_rect(figp), 1800), 'vizner2021-fig2-domains.webp')

# Meng 2022 — public arXiv manuscript. Its abstract is split into many PDF text
# blocks/lines, so use the first and final sentence as geometric anchors instead
# of trusting one text block.
meng = fitz.open('/tmp/foundations/meng2022.pdf')
p = page_with(meng, 'When the atomic layers in a non-centrosymmetric van der Waals structure')
start_hits = p.search_for('When the atomic layers in a non-centrosymmetric van der Waals structure')
end_hits = p.search_for('novel sliding ferroelectric devices')
if not start_hits or not end_hits:
    raise RuntimeError('Meng abstract anchors not found')
s = start_hits[0]
e = end_hits[-1]
abstract_rect = fitz.Rect(20, max(0, s.y0-12), p.rect.width-20, min(p.rect.height, e.y1+12))
save(trim(render(p, abstract_rect, 1800)), 'meng2022-paragraph-multistate.webp')

figp = page_with(meng, 'Static transport properties of dual-gate FET devices')
full_fig3 = render(figp, largest_image_rect(figp), 1800)
# Panel e is the lower switching-pathway schematic. 0.66 preserves the "e"
# label while removing the residual x-axis from panel d seen in artifact QA.
y0 = int(full_fig3.height * 0.66)
panel_e = trim(full_fig3.crop((0, y0, full_fig3.width, full_fig3.height)), margin=18)
save(panel_e, 'meng2022-fig3e-multistate.webp')

expected = {
    'wu2021-paragraph-model.webp', 'wu2021-fig1-mechanism.webp',
    'yasuda2021-paragraph-abstract.webp', 'yasuda2021-fig1-stacking.webp',
    'vizner2021-paragraph-abstract.webp', 'vizner2021-fig2-domains.webp',
    'meng2022-paragraph-multistate.webp', 'meng2022-fig3e-multistate.webp',
}
found = {p.name for p in OUT.glob('*.webp')}
if found != expected:
    raise RuntimeError(f'Foundations asset mismatch: missing={expected-found}, extra={found-expected}')
