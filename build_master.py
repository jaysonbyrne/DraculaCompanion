#!/usr/bin/env python3
"""Assemble the complete Dracula companion: red-cloth cover, contents,
then all chapter PDFs merged into one master volume.

Usage (from ~/workspace/dracula-companion):
    python3 build_master.py
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from packet import Packet, INK, RED, GOLD, GOLD_LT, CREAM, FAINT
from render import load_chapter

BASE = os.path.dirname(os.path.abspath(__file__))


def roman(n):
    out = ""
    for v, s in ((20, "XX"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += s
            n -= v
    return out


def chapter_pdf(num):
    nn = f"{num:02d}"
    if num == 1:
        return os.path.join(BASE, "ch01", "dracula_chapter1_ephemera.pdf")
    return os.path.join(BASE, f"ch{nn}", f"dracula_ch{nn}_ephemera.pdf")


def short_title(title):
    """Abbreviated names for the contents page only."""
    t = title
    t = t.replace("JONATHAN HARKER'S", "HARKER'S")
    t = t.replace("DR. SEWARD'S", "SEWARD'S")
    t = t.replace("MINA MURRAY'S", "MINA'S")
    t = t.replace("MINA HARKER'S", "MINA'S")
    return t


def chapter_entry(num):
    """(title_line, subtitle) for the contents page, e.g.
    ('24: SEWARD'S PHONOGRAPH DIARY', '4th -- 6th October')."""
    try:
        ch = load_chapter(num)
        if re.match(r"(?i)^chapter\b", ch["label"]):
            head = f"{num}:"
        else:
            head = ch["label"] + ":"
        return f"{head} {short_title(ch['title'])}", ch.get("subtitle")
    except Exception:
        if num == 1:
            return ("1: HARKER'S JOURNAL",
                    "3rd -- 5th May -- Bistritz to the Borgo Pass")
        return f"{num}:", None


def main():
    # Build any chapter PDFs that don't exist yet (needs chNN/content.py).
    for n in range(2, 29):
        if not os.path.exists(chapter_pdf(n)):
            src = os.path.join(BASE, f"ch{n:02d}", "content.py")
            if os.path.exists(src):
                subprocess.run(
                    [sys.executable, os.path.join(BASE, "lib", "build_chapter.py"),
                     str(n)], check=True)
            else:
                print(f"note: ch{n:02d} has no content.py yet, skipped")

    from pypdf import PdfReader, PdfWriter

    counts = {}
    for n in range(1, 29):
        p = chapter_pdf(n)
        counts[n] = len(PdfReader(p).pages) if os.path.exists(p) else 0

    # ---- Cover ----
    pdf = Packet()
    pdf.set_title("The Dracula Companion -- Complete Ephemera")
    pdf.add_page()
    pdf.paint_cloth()
    pdf.no_footer = True
    pdf.set_draw_color(*GOLD_LT)
    pdf.set_line_width(1.1)
    pdf.rect(9, 9, 130, 192)
    pdf.set_line_width(0.35)
    pdf.rect(13, 13, 122, 184)
    pdf.set_text_color(*GOLD_LT)
    pdf.ln(40)
    pdf.set_font("goth", "", 30)
    pdf.multi_cell(0, 15, "The Complete\nDracula Companion", align="C")
    pdf.ln(6)
    y = pdf.get_y()
    pdf.set_line_width(0.5)
    pdf.line(59, y, 89, y)
    pdf.set_y(y + 6)
    pdf.set_font("fell", "I", 11)
    pdf.set_text_color(*CREAM)
    pdf.multi_cell(
        0, 6,
        "Being the ephemera of all twenty-eight chapters\nof Bram Stoker's novel --\n"
        "notices, letters, telegrams, cuttings, bills & plates --\n"
        "collected for the reader's amusement.",
        align="C",
    )
    cover_path = os.path.join(BASE, "_cover.pdf")
    pdf.output(cover_path)

    # ---- Contents (two passes: count pages, then number them) ----
    def render_toc(page_starts):
        t = Packet()
        t.set_title("Contents")
        t.add_page()
        t.paint_bg()
        t.set_text_color(*RED)
        t.set_font("goth", "", 20)
        t.cell(0, 10, "Contents", align="C", new_x="LMARGIN", new_y="NEXT")
        t.ln(1)
        t.rule(width=50)
        t.ln(3)
        t.set_font("fell", "", 8.5)
        avail = 116  # text width in mm
        dot_w = t.get_string_width(".")
        items = []
        for n in range(1, 29):
            title_line, subtitle = chapter_entry(n)
            pg = str(page_starts[n]) if page_starts.get(n) else "--"
            items.append((title_line, subtitle, pg))
        for title_line, subtitle, pg in items:
            # keep each entry's two lines together on one page
            need = 5.2 + (4.4 + 0.8 if subtitle else 0.8)
            if t.get_y() + need > 191:
                t.add_page()
                t.paint_bg()
            label = title_line
            pg_w = t.get_string_width(pg)
            while label and t.get_string_width(label) > avail - pg_w - 14:
                label = label[:-1]
            if label != title_line:
                label = label.rstrip() + "..."
            label_w = t.get_string_width(label)
            n_dots = max(3, int((avail - label_w - pg_w - 6) / dot_w))
            dots = "." * n_dots
            t.set_text_color(*INK)
            t.cell(0, 5.2, f"{label} {dots} {pg}",
                   new_x="LMARGIN", new_y="NEXT")
            if subtitle:
                head = title_line.split(" ", 1)[0]
                indent = t.get_string_width(head + " ")
                t.set_text_color(*FAINT)
                t.set_font("fell", "I", 8)
                t.cell(indent, 4.4, "")
                t.cell(0, 4.4, subtitle, new_x="LMARGIN", new_y="NEXT")
                t.set_font("fell", "", 8.5)
            t.ln(0.8)
        t.ln(4)
        t.set_font("fell", "I", 9)
        t.set_text_color(*FAINT)
        t.multi_cell(
            0, 5,
            "Folios restart with each chapter, every chapter being its own\n"
            "signature; the figures above are master pages of this volume.",
            align="C",
        )
        return t

    toc_probe = render_toc({})
    toc_pages = toc_probe.page_no()
    # frontispiece: works-cited gallery + journey map, built before the TOC
    # so chapter master pages can be counted past them
    sys.path.insert(0, os.path.join(BASE, "works"))
    import build_frontispiece
    works_path = build_frontispiece.build_works()
    map_path = build_frontispiece.build_map()
    works_pages = len(PdfReader(works_path).pages)
    map_pages = len(PdfReader(map_path).pages)
    start = 1 + works_pages + map_pages + 1 + toc_pages  # cover + frontispiece + toc
    page_starts = {}
    for n in range(1, 29):
        if counts[n]:
            page_starts[n] = start
            start += counts[n]
    toc = render_toc(page_starts)
    toc_path = os.path.join(BASE, "_toc.pdf")
    toc.output(toc_path)

    # ---- Merge ----
    writer = PdfWriter()
    for p in [works_path, map_path, cover_path, toc_path] + [
            chapter_pdf(n) for n in range(1, 29) if counts[n]]:
        writer.append(p)
    out = os.path.join(BASE, "dracula_companion_complete.pdf")
    with open(out, "wb") as f:
        writer.write(f)
    print(f"wrote {out} ({len(writer.pages)} pages)")
    for tmp in (cover_path, toc_path, works_path, map_path):
        os.remove(tmp)


if __name__ == "__main__":
    main()
