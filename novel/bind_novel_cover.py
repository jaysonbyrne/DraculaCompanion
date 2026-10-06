#!/usr/bin/env python3
"""Prepend the vampire-painting cover as page 1 of dracula_illustrated.pdf.

Usage:  python3 bind_novel_cover.py <painting.png> [novel_dir]

Composites the white title onto the painting, builds a one-page A5 PDF,
and prepends it to dracula_illustrated.pdf, shifting the chapter outline
by one page. Run after `python3 build_novel.py illustrated`.

The painting itself is a binary asset and is NOT tracked in git
(see ASSETS.md); pass the local PNG path.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter


def _font_dir(*cands):
    for c in cands:
        if Path(c).is_dir():
            return c
    return cands[0]


NOTO = _font_dir('/usr/share/fonts/truetype/noto', '/usr/share/fonts/noto')


def compose_cover(painting: Path, out_jpg: Path):
    im = ImageOps.fit(Image.open(painting).convert('RGB'), (1480, 2100))
    # darken the top for title legibility
    grad = Image.new('L', (1, 560))
    for y in range(560):
        grad.putpixel((0, y), int(150 * (1 - y / 560)))
    grad = grad.resize((1480, 560))
    black = Image.new('RGB', (1480, 560), (0, 0, 0))
    im.paste(Image.composite(black, im.crop((0, 0, 1480, 560)), grad), (0, 0))

    d = ImageDraw.Draw(im)
    f_t = ImageFont.truetype(str(Path(NOTO) / 'NotoSerif-Bold.ttf'), 168)
    f_s = ImageFont.truetype(str(Path(NOTO) / 'NotoSerif-Regular.ttf'), 52)

    def spaced(text, font, cx, y, tracking, fill):
        ws = [d.textlength(ch, font=font) for ch in text]
        x = cx - (sum(ws) + tracking * (len(text) - 1)) / 2
        for ch, w in zip(text, ws):
            d.text((x, y), ch, font=font, fill=fill)
            x += w + tracking

    spaced('DRACULA', f_t, 740, 150, 34, (245, 240, 230))
    d.line([440, 400, 640, 400], fill=(200, 170, 120), width=3)
    d.line([840, 400, 1040, 400], fill=(200, 170, 120), width=3)
    spaced('AN ILLUSTRATED EDITION', f_s, 740, 372, 18, (225, 215, 200))
    im.save(out_jpg, quality=92)


def main():
    painting = Path(sys.argv[1])
    noveld = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 \
        else Path(__file__).resolve().parent
    target = noveld / 'dracula_illustrated.pdf'
    if not target.is_file():
        sys.exit(f'no {target} — run build_novel.py illustrated first')

    cover_jpg = noveld / '_vampire_cover.jpg'
    compose_cover(painting, cover_jpg)

    pdf = FPDF(unit='mm', format='A5')
    pdf.add_page()
    pdf.image(str(cover_jpg), x=0, y=0, w=148, h=210)
    cover_pdf = noveld / '_cover1.pdf'
    pdf.output(str(cover_pdf))

    reader = PdfReader(str(target))
    toc = []

    def collect(items):
        for it in items:
            if isinstance(it, list):
                collect(it)
            else:
                toc.append((it.title,
                            reader.get_destination_page_number(it)))

    collect(reader.outline)

    writer = PdfWriter()
    for p in PdfReader(str(cover_pdf)).pages:
        writer.add_page(p)
    for p in reader.pages:
        writer.add_page(p)
    for title, pg0 in toc:
        writer.add_outline_item(title, pg0 + 1)
    writer.add_metadata(dict(reader.metadata or {}))
    with open(target, 'wb') as fh:
        writer.write(fh)
    cover_pdf.unlink()
    print(f'cover bound: {target} '
          f'({len(PdfReader(str(target)).pages)} pages)')


if __name__ == '__main__':
    main()
