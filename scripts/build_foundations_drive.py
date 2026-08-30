from pathlib import Path
import fitz
from PIL import Image, ImageDraw, ImageOps

OUT = Path('assets/foundations')
OUT.mkdir(parents=True, exist_ok=True)
DPI = 600
S = DPI / 72

PDF = {
    'wu': Path('/tmp/foundations/wu2021.pdf'),
    'yas': Path('/tmp/foundations/yasuda2021.pdf'),
    'viz': Path('/tmp/foundations/vizner2021.pdf'),
    'meng': Path('/tmp/foundations/meng2022.pdf'),
}
EXPECTED_GEOMETRY = {
    'wu': (585.0, 783.0),
    'yas': (612.0, 792.0),
    'viz': (612.0, 792.0),
    'meng': (595.3, 790.9),
}


def guard_geometry(doc, key):
    w, h = doc[0].rect.width, doc[0].rect.height
    ew, eh = EXPECTED_GEOMETRY[key]
    if abs(w-ew) > 1.0 or abs(h-eh) > 1.0:
        raise RuntimeError(f'{key}: unexpected PDF geometry {(w,h)}; expected {(ew,eh)}')


def render(page, rect, maxw=1800):
    pix = page.get_pixmap(matrix=fitz.Matrix(S, S), clip=fitz.Rect(rect), alpha=False)
    im = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    if im.width > maxw:
        im = im.resize((maxw, round(im.height*maxw/im.width)), Image.Resampling.LANCZOS)
    return im


def trim(im, margin=24, threshold=248):
    g = ImageOps.grayscale(im)
    mask = g.point(lambda x: 255 if x < threshold else 0)
    box = mask.getbbox()
    if not box:
        return im
    l, t, r, b = box
    return im.crop((max(0,l-margin), max(0,t-margin), min(im.width,r+margin), min(im.height,b+margin)))


def save(im, name, quality=91):
    p = OUT / name
    im.save(p, 'WEBP', quality=quality, method=6)
    if p.stat().st_size < 18_000:
        raise RuntimeError(f'suspiciously small crop: {name} ({p.stat().st_size} bytes)')
    with Image.open(p) as check:
        check.verify()
    print(name, im.size, p.stat().st_size)


def stitch(parts, name, maxw=1500):
    parts = [trim(x) for x in parts]
    gap = 54
    w = max(x.width for x in parts)
    h = sum(x.height for x in parts) + gap*(len(parts)-1)
    c = Image.new('RGB', (w,h), 'white')
    d = ImageDraw.Draw(c)
    y = 0
    for i, part in enumerate(parts):
        c.paste(part, ((w-part.width)//2, y))
        y += part.height
        if i < len(parts)-1:
            d.line((35, y+gap//2, w-35, y+gap//2), fill=(215,215,215), width=2)
            y += gap
    if c.width > maxw:
        c = c.resize((maxw, round(c.height*maxw/c.width)), Image.Resampling.LANCZOS)
    save(c, name)


# 1) Wu & Li 2021 — exact published PNAS PDF from the project Drive.
wu = fitz.open(PDF['wu']); guard_geometry(wu, 'wu')
p = wu[1]
# One logical paragraph crosses the two publication columns.
left = fitz.Rect(42.9, 255.6, 284.7, 419.1)
end_hits = p.search_for('down layer, as shown in Fig. 1A.') or p.search_for('down layer, as shown in Fig. 1A')
if not end_hits:
    raise RuntimeError('Wu paragraph end sentence not found')
end = end_hits[-1]
right = fitz.Rect(300.5, 47.3, 542.4, end.y1+2)
stitch([render(p,left,1700), render(p,right,1700)], 'wu2021-paragraph-model.webp')
save(render(p, (130.5, 441.0, 454.9, 672.2), 1800), 'wu2021-fig1-mechanism.webp')

# 2) Yasuda et al. 2021 — exact Science PDF from the project Drive.
yas = fitz.open(PDF['yas']); guard_geometry(yas, 'yas')
p = yas[0]
# Complete main-text paragraph beginning "The development of vdW assembly...".
# It begins at the bottom of the left column and continues at the top of the right column.
yas_left = fitz.Rect(36.0, 626.5, 302.6, 733.2)
yas_right = fitz.Rect(312.1, 326.5, 578.7, 613.1)
stitch([render(p,yas_left,1700), render(p,yas_right,1700)], 'yasuda2021-paragraph-stacking.webp')
p = yas[5]
save(render(p, (47.9, 72.0, 564.1, 317.5), 1800), 'yasuda2021-fig1-stacking.webp')

# 3) Vizner Stern et al. 2021 — exact Science PDF from the project Drive.
viz = fitz.open(PDF['viz']); guard_geometry(viz, 'viz')
p = viz[1]
save(trim(render(p, (36.0, 187.9, 302.6, 642.7), 1800)), 'vizner2021-paragraph-domains.webp')
p = viz[7]
save(render(p, (132.0, 72.0, 480.0, 299.8), 1800), 'vizner2021-fig2-domains.webp')

# 4) Meng et al. 2022 — exact Nature Communications PDF from the project Drive.
meng = fitz.open(PDF['meng']); guard_geometry(meng, 'meng')
p = meng[0]
save(trim(render(p, (217.3, 270.4, 561.3, 461.7), 1800)), 'meng2022-paragraph-multistate.webp')
p = meng[4]
# Fig. 3e only: preserve panel label, all interface arrows and initial/intermediate/final states.
save(render(p, (60.5, 329.0, 540.5, 522.3), 1800), 'meng2022-fig3e-multistate.webp')

expected = {
    'wu2021-paragraph-model.webp', 'wu2021-fig1-mechanism.webp',
    'yasuda2021-paragraph-stacking.webp', 'yasuda2021-fig1-stacking.webp',
    'vizner2021-paragraph-domains.webp', 'vizner2021-fig2-domains.webp',
    'meng2022-paragraph-multistate.webp', 'meng2022-fig3e-multistate.webp',
}
found = {p.name for p in OUT.glob('*.webp')}
# Ignore no files here: this builder owns exactly the Foundations crop set.
if found != expected:
    raise RuntimeError(f'Foundations asset mismatch: missing={expected-found}, extra={found-expected}')
