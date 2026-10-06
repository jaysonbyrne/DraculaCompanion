#!/usr/bin/env python3
"""Insert full-page diorama inserts at spread-out random positions
in the master volume. Re-runnable: inserts are placed fresh each run
from the current master (run once per new set of dioramas).

Usage (from ~/workspace/dracula-companion):
    python3 build_inserts.py
"""
import glob
import os
import random

from PIL import Image, ImageOps
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter

BASE = os.path.dirname(os.path.abspath(__file__))
DIOR = os.path.join(BASE, "dioramas")
MASTER = os.path.join(BASE, "dracula_companion_complete.pdf")


def main():
    imgs = sorted(glob.glob(os.path.join(DIOR, "*.jpg")) +
                  glob.glob(os.path.join(DIOR, "*.png")))
    # skip working files
    imgs = [p for p in imgs if ".bleed." not in p]
    assert imgs, "no diorama images found"

    pdf = FPDF(orientation="P", unit="mm", format="A5")
    for p in imgs:
        im = ImageOps.fit(Image.open(p).convert("RGB"), (1480, 2100))
        tmp = p + ".bleed.jpg"
        im.save(tmp, quality=90)
        pdf.add_page()
        pdf.image(tmp, x=0, y=0, w=148, h=210)
    inserts_pdf = os.path.join(BASE, "_inserts.pdf")
    pdf.output(inserts_pdf)

    reader = PdfReader(MASTER)
    n = len(reader.pages)
    k = len(imgs)
    random.seed(1893)
    positions = sorted(
        random.randint(int(n * i / k) + 2, int(n * (i + 1) / k) - 1)
        for i in range(k)
    )

    ins = PdfReader(inserts_pdf)
    writer = PdfWriter()
    ins_idx = 0
    pos_set = set(positions)
    for i, page in enumerate(reader.pages):
        if i in pos_set:
            writer.add_page(ins.pages[ins_idx])
            ins_idx += 1
        writer.add_page(page)
    while ins_idx < len(ins.pages):
        writer.add_page(ins.pages[ins_idx])
        ins_idx += 1
    with open(MASTER, "wb") as f:
        writer.write(f)
    print(f"inserted {k} dioramas at master pages {positions}; "
          f"total {len(writer.pages)} pages")

    os.remove(inserts_pdf)
    for p in glob.glob(os.path.join(DIOR, "*.bleed.jpg")):
        os.remove(p)


if __name__ == "__main__":
    main()
