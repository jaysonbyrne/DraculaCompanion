"""Build the 'Of the Vampyre' ancient-book front-matter section.

Adapts to one missing woodcut (the vampire plate could not be generated):
the bat ornament opens page 1 and closes the section, the village plate
stands on page 2.
"""
import glob
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/dracula-companion/lib")
from packet import Packet, INK, RED, FAINT

BASE = "/home/hatch/workspace/dracula-companion/ancient"
FONTS = "/home/hatch/workspace/dracula-companion/fonts"

TEXT_PARAS = [
    "Herein is writ of the Strigoi, which dieth not. When the sun is set and "
    "the cock croweth no more, he riseth from the grave wherein he was laid "
    "unshriven, and walketh the night in the shape of a mist, or of a great "
    "hound, or of a bat that drinketh.",
    "He cometh to the chamber of them that sleep, and layeth his cold mouth "
    "upon them, and drinketh their life in their sleep; and they that are so "
    "drunk of grow pale and pine, and die, and themselves become Strigoi, "
    "and so the curse multiplieth.",
    "Yet is he not without law. He may not enter where he is not bidden. The "
    "garlic flower offendeth him, and the crucifix driveth him back, and the "
    "sacred Host consumeth him as fire. He casteth no shadow in the glass, "
    "neither doth his image appear therein.",
    "In the daylight he must rest him in the earth of his own grave; and if "
    "a stake of wood be driven through his heart whilst he sleepeth, then is "
    "he truly dead, and his soul is loosed.",
    "These things are known to the shepherds of the mountains, who set the "
    "garlic at their doors on the Eve of St. George, when all evil things "
    "hold their sabbath.",
]


def find(slug):
    hits = glob.glob(os.path.join(BASE, f"*{slug}*.png"))
    if not hits:
        raise FileNotFoundError(f"no image for slug {slug}")
    return sorted(hits)[0]


pdf = Packet()
pdf.set_title("Of the Vampyre")
pdf.add_font("goth", "", os.path.join(FONTS, "Blackletter.ttf"))
pdf.add_font("fell", "", os.path.join(FONTS, "Fell.ttf"))
pdf.add_font("fell", "I", os.path.join(FONTS, "Fell-Italic.ttf"))
pdf.set_auto_page_break(False)
BOTTOM = 210 - 18  # honour the 18mm bottom margin manually


def img_aspect(path):
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    return iw / ih


def ensure(h):
    if pdf.get_y() + h > BOTTOM:
        pdf.add_page()
        pdf.paint_bg()


def para_height(text, size=11, lh=5.8):
    pdf.set_font("goth", "", size)
    try:
        lines = pdf.multi_cell(0, lh, text, align="J",
                               dry_run=True, output="LINES")
        return len(lines) * lh
    except Exception:
        return (len(text) // 55 + 1) * lh


def para(text, size=11, lh=5.8, after=4):
    ensure(para_height(text, size, lh) + after)
    pdf.set_font("goth", "", size)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, lh, text, align="J")
    pdf.ln(after)


def centered_image(path, w, gap_before=5, gap_after=6):
    h = w / img_aspect(path)
    ensure(h + gap_before + gap_after)
    pdf.ln(gap_before)
    x = (148 - w) / 2
    pdf.image(path, x=x, y=pdf.get_y(), w=w)
    pdf.set_y(pdf.get_y() + h + gap_after)


# ---- page 1: title, ornament, text begins ----
pdf.add_page()
pdf.paint_bg()
pdf.set_text_color(*INK)
pdf.set_font("goth", "", 28)
pdf.cell(0, 14, "Of the Vampyre", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.set_text_color(*FAINT)
pdf.set_font("fell", "I", 10.5)
pdf.multi_cell(0, 6,
               "Being an extract from a very old book of Transylvania, "
               "concerning the Strigoi, here faithfully translated.",
               align="C")
centered_image(find("bat-woodcut"), 70)
para(TEXT_PARAS[0])
para(TEXT_PARAS[1])

# ---- page 2: village plate, text continues ----
pdf.add_page()
pdf.paint_bg()
centered_image(find("village-woodcut"), 100, gap_before=2)
para(TEXT_PARAS[2])
para(TEXT_PARAS[3])

# ---- page 3: text concludes, ornament colophon ----
pdf.add_page()
pdf.paint_bg()
para(TEXT_PARAS[4])
pdf.ln(4)
centered_image(find("bat-woodcut"), 45, gap_before=2, gap_after=0)

out = os.path.join(BASE, "_ancient.pdf")
pdf.output(out)
print("wrote", out, pdf.page_no(), "pages")
