#!/usr/bin/env bash
set -euxo pipefail
sudo apt-get update -qq
sudo apt-get install -y -qq poppler-utils python3-pil
mkdir -p assets/domain-walls /tmp/papers

curl -fL --retry 3 -A 'Mozilla/5.0' 'https://liutheory.westlake.edu.cn/pdf/Ke25p046201.pdf' -o /tmp/papers/ke2025.pdf
curl -fL --retry 3 -A 'Mozilla/5.0' 'https://liutheory.westlake.edu.cn/pdf/Chen26p011066.pdf' -o /tmp/papers/chen2026.pdf
curl -fL --retry 3 -A 'Mozilla/5.0' 'https://arxiv.org/pdf/2605.21210' -o /tmp/papers/liu2026.pdf

pdftoppm -f 2 -l 2 -singlefile -r 600 -png /tmp/papers/ke2025.pdf /tmp/papers/ke-p2
pdftoppm -f 2 -l 2 -singlefile -r 600 -png /tmp/papers/chen2026.pdf /tmp/papers/chen-p2
pdftoppm -f 3 -l 3 -singlefile -r 600 -png /tmp/papers/chen2026.pdf /tmp/papers/chen-p3
pdftoppm -f 2 -l 2 -singlefile -r 600 -png /tmp/papers/liu2026.pdf /tmp/papers/liu-p2
pdftoppm -f 3 -l 3 -singlefile -r 600 -png /tmp/papers/liu2026.pdf /tmp/papers/liu-p3

python3 - <<'PY'
from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
out = Path('assets/domain-walls')

def crop_resize(src, box, maxw):
    page = Image.open(src).convert('RGB')
    crop = page.crop(box)
    if crop.width > maxw:
        crop = crop.resize((maxw, round(crop.height * maxw / crop.width)), Image.Resampling.LANCZOS)
    return crop

def trim_text(im, margin=30):
    gray = ImageOps.grayscale(im)
    mask = gray.point(lambda x: 255 if x < 245 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return im
    l,t,r,b = bbox
    return im.crop((max(0,l-margin), max(0,t-margin), min(im.width,r+margin), min(im.height,b+margin)))

def stitch(parts, outfile, maxw=1400):
    gap = 72
    width = max(p.width for p in parts)
    height = sum(p.height for p in parts) + gap * (len(parts)-1)
    canvas = Image.new('RGB', (width,height), 'white')
    y = 0
    for i, part in enumerate(parts):
        canvas.paste(part, ((width-part.width)//2, y))
        y += part.height
        if i < len(parts)-1:
            ImageDraw.Draw(canvas).line((40,y+gap//2,width-40,y+gap//2), fill=(210,210,210), width=2)
            y += gap
    if canvas.width > maxw:
        canvas = canvas.resize((maxw, round(canvas.height*maxw/canvas.width)), Image.Resampling.LANCZOS)
    canvas.save(out/outfile, 'WEBP', quality=90, method=6)

specs = [
    ('/tmp/papers/ke-p2.png',   (400,385,2500,1740),  'ke2025-fig1-bec-force.webp', 1800),
    ('/tmp/papers/ke-p2.png',   (2550,2240,4780,4758),'ke2025-paragraph-bec.webp', 1400),
    ('/tmp/papers/chen-p2.png', (650,380,4510,3550),  'chen2026-fig1.webp', 1800),
    ('/tmp/papers/chen-p3.png', (400,2440,2550,4218), 'chen2026-paragraph-no-dw.webp', 1400),
    ('/tmp/papers/chen-p3.png', (2580,540,4750,2560), 'chen2026-paragraph-kpfm.webp', 1400),
    ('/tmp/papers/chen-p3.png', (2600,3148,4670,4918),'chen2026-fig2-pinning.webp', 1800),
    ('/tmp/papers/liu-p3.png',  (780,338,4600,2245),  'liu2026-fig2-raman-switching.webp', 1800),
]
for src, box, name, maxw in specs:
    crop_resize(src, box, maxw).save(out/name, 'WEBP', quality=90, method=6)

p2 = Image.open('/tmp/papers/liu-p2.png').convert('RGB')
p3 = Image.open('/tmp/papers/liu-p3.png').convert('RGB')
if p2.size != (5100,6600) or p3.size != (5100,6600):
    raise SystemExit(f'Unexpected Liu page geometry: {p2.size}, {p3.size}')

stitch([
    trim_text(p2.crop((2610,4884,4815,6570))),
    trim_text(p3.crop((240,2985,2550,3405))),
], 'liu2026-paragraph-single-domain.webp')

stitch([
    trim_text(p3.crop((240,5862,2550,6570))),
    trim_text(p3.crop((2580,2985,4830,4095))),
], 'liu2026-paragraph-pinning.webp')

expected = [name for _,_,name,_ in specs] + [
    'liu2026-paragraph-single-domain.webp',
    'liu2026-paragraph-pinning.webp',
]
for name in expected:
    p = out/name
    if not p.exists() or p.stat().st_size < 20_000:
        raise SystemExit(f'bad asset: {name}')
    with Image.open(p) as im:
        im.verify()
PY
