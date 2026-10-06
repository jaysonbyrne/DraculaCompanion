"""Build the frontispiece gallery: the 'Of the Papers' works-cited catalogue
and the numbered journey map with its notes. Outputs _works.pdf and _map.pdf
for build_master.py to merge in."""
import glob
import os
import sys
from PIL import Image as PILImage

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from packet import Packet, INK, RED, FAINT
from works.works_cited import WORKS, MAP_NOTES

BASE = os.path.dirname(os.path.abspath(__file__))


def roman(n):
    vals = [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


def clean(t):
    """House style is latin-1 Times: straighten quotes, ASCII dashes."""
    return (t.replace("\u201c", '"').replace("\u201d", '"')
             .replace("\u2018", "'").replace("\u2019", "'")
             .replace("\u2014", "--").replace("\u2013", "-"))


def resolve(slug):
    hits = glob.glob(os.path.join(BASE, f"*{slug}*.png"))
    if not hits:
        raise FileNotFoundError(f"no image for slug {slug}")
    return sorted(hits)[0]


def build_works():
    pdf = Packet()
    pdf.set_title("Of the Papers")
    # ---- section title page ----
    pdf.add_page()
    pdf.paint_bg()
    pdf.set_text_color(*RED)
    pdf.set_font("fellsc", "", 11)
    pdf.cell(0, 8, "A Catalogue of the Sources", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.rule()
    pdf.ln(4)
    pdf.set_text_color(*INK)
    pdf.set_font("goth", "", 26)
    pdf.cell(0, 14, "Of the Papers", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("fell", "I", 11)
    pdf.set_text_color(*FAINT)
    pdf.multi_cell(0, 6,
                   clean("Being a catalogue of the documents gathered in this "
                   "companion, with an account of each, and of the hands "
                   "that wrote them."),
                   align="C")
    pdf.ln(4)
    pdf.rule()
    # ---- one plate per work ----
    for i, w in enumerate(WORKS):
        img = resolve(w["slug"])
        pdf.add_page()
        pdf.paint_bg()
        pdf.set_text_color(*RED)
        pdf.set_font("fellsc", "", 10)
        pdf.cell(0, 6, f"Of the Papers \u00b7 {roman(i + 1)}", align="C",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        pdf.rule(width=50)
        iw, ih = PILImage.open(img).size
        aspect = iw / ih
        wmm = min(116, 82 * aspect)
        hmm = wmm / aspect
        x = (148 - wmm) / 2
        y = pdf.get_y() + 4
        pdf.image(img, x=x, y=y, w=wmm, h=hmm)
        pdf.set_y(y + hmm + 6)
        pdf.set_text_color(*INK)
        pdf.set_font("fell", "", 12.5)
        pdf.multi_cell(0, 6.5, w["title"], align="C")
        pdf.ln(2)
        pdf.para(clean(w["desc"]), size=10.5, align="J")
    out = os.path.join(BASE, "_works.pdf")
    pdf.output(out)
    return out


def build_map():
    pdf = Packet()
    pdf.set_title("The Journey")
    # ---- map page ----
    pdf.add_page()
    pdf.paint_bg()
    pdf.set_text_color(*RED)
    pdf.set_font("fellsc", "", 10)
    pdf.cell(0, 6, "Frontispiece", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.rule(width=50)
    pdf.ln(2)
    pdf.set_text_color(*INK)
    pdf.set_font("goth", "", 24)
    pdf.cell(0, 12, "The Journey", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("fell", "I", 10)
    pdf.set_text_color(*FAINT)
    pdf.cell(0, 6, clean("All the roads in this book, numbered for reference."),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    img = os.path.join(BASE, "journey_map_numbered.png")
    iw, ih = PILImage.open(img).size
    wmm = 128
    hmm = wmm * ih / iw
    x = (148 - wmm) / 2
    y = pdf.get_y()
    if y + hmm > 192:
        pdf.add_page()
        pdf.paint_bg()
        y = 20
    pdf.image(img, x=x, y=y, w=wmm, h=hmm)
    pdf.set_y(y + hmm + 4)
    pdf.set_font("fell", "I", 9)
    pdf.set_text_color(*FAINT)
    pdf.multi_cell(
        0, 4.8,
        clean("The dotted line marks the Count's road east; the sea-line, the "
        "Demeter's crossing; the return line, the hunt. The notes following "
        "give the story of each number."),
        align="C")
    # ---- map notes ----
    pdf.add_page()
    pdf.paint_bg()
    pdf.set_text_color(*RED)
    pdf.set_font("goth", "", 18)
    pdf.cell(0, 9, "Map Notes", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.rule(width=50)
    pdf.ln(4)
    for n, (place, note) in enumerate(MAP_NOTES, start=1):
        if pdf.get_y() > 178:
            pdf.add_page()
            pdf.paint_bg()
        pdf.set_text_color(*RED)
        pdf.set_font("pf", "B", 10.5)
        pdf.cell(0, 5.5, f"{n}. {place}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*INK)
        pdf.set_font("fell", "", 10)
        pdf.multi_cell(0, 5.4, clean(note))
        pdf.ln(2.5)
    out = os.path.join(BASE, "_map.pdf")
    pdf.output(out)
    return out


if __name__ == "__main__":
    print("works:", build_works())
    print("map:", build_map())
