#!/usr/bin/env python3
"""Prepend the dust-jacket cover PNG as page 1 of the complete companion PDF."""
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/book/.venv/lib/python3.12/site-packages")

BASE = "/home/hatch/workspace/dracula-companion"
COVER_PNG = os.path.join(BASE, "dracula-companion-cover.png")
MASTER = os.path.join(BASE, "dracula_companion_complete.pdf")

import fitz
from PIL import Image

src = fitz.open(MASTER)
r = src[0].rect
cw, ch = r.width, r.height

cover = Image.open(COVER_PNG)
target_ratio = ch / cw
img_ratio = cover.height / cover.width
if img_ratio > target_ratio:
    new_h = int(cover.width * target_ratio)
    y0 = (cover.height - new_h) // 2
    cover = cover.crop((0, y0, cover.width, y0 + new_h))
elif img_ratio < target_ratio:
    new_w = int(cover.height / target_ratio)
    x0 = (cover.width - new_w) // 2
    cover = cover.crop((x0, 0, x0 + new_w, cover.height))
cover.save("/tmp/cover_page.png")

doc = fitz.open()
page = doc.new_page(width=cw, height=ch)
page.insert_image(page.rect, filename="/tmp/cover_page.png")
doc.save("/tmp/cover_only.pdf")

out = fitz.open()
out.insert_pdf(fitz.open("/tmp/cover_only.pdf"))
out.insert_pdf(src)
out.save(MASTER, garbage=4, deflate=True)
print(f"bound cover: {len(out)} pages")
