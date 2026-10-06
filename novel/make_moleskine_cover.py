#!/usr/bin/env python3
"""Compose the pocket edition's moleskine cover.

Usage:  python3 make_moleskine_cover.py <leather-texture.png> [out.jpg]

Debosses "DRACULA / AN ILLUSTRATED EDITION" onto a brown leather texture
and saves a 1040x2250 cover image (default: moleskine_cover.jpg next to
build_pocket.py). The leather texture is a binary asset and is NOT
tracked in git (see ASSETS.md); pass the local PNG path.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def _font_dir(*cands):
    for c in cands:
        if Path(c).is_dir():
            return c
    return cands[0]


NOTO = _font_dir('/usr/share/fonts/truetype/noto', '/usr/share/fonts/noto')


def main():
    texture = Path(sys.argv[1])
    out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 \
        else Path(__file__).resolve().parent / 'moleskine_cover.jpg'

    im = ImageOps.fit(Image.open(texture).convert('RGB'), (1040, 2250))
    d = ImageDraw.Draw(im)
    f_t = ImageFont.truetype(str(Path(NOTO) / 'NotoSerif-Bold.ttf'), 132)
    f_s = ImageFont.truetype(str(Path(NOTO) / 'NotoSerif-Regular.ttf'), 34)

    def spaced(text, font, cx, y, tracking, dark, light):
        ws = [d.textlength(ch, font=font) for ch in text]
        x = cx - (sum(ws) + tracking * (len(text) - 1)) / 2
        for ch, w in zip(text, ws):
            d.text((x, y + 3), ch, font=font, fill=light)  # deboss highlight
            d.text((x, y), ch, font=font, fill=dark)
            x += w + tracking

    spaced('DRACULA', f_t, 520, 640, 44, (52, 30, 16), (205, 160, 118))
    spaced('AN ILLUSTRATED EDITION', f_s, 520, 900, 12,
           (74, 46, 26), (205, 160, 118))
    im.save(out, quality=92)
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
