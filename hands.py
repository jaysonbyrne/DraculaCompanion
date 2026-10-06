"""Alternate handwriting faces for Lucy's letters: same excerpt, four hands."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from packet import Packet, INK, RED, FAINT

BASE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(BASE, "fonts")

TEXT = ("My dearest Mina,\u2014\nI must tell you my news. Mr. Holmwood was "
        "here yesterday and proposed to me! I felt very sad, for I do so love "
        "him, and yet I could not love him as a husband ought to be loved\u2026\n"
        "Your loving\nLucy")

HANDS = [
    ("hand1", "Caveat.ttf", "Caveat -- a quick natural pen, easy to read"),
    ("hand2", "HomemadeApple.ttf", "Homemade Apple -- uneven and human, real ink"),
    ("hand3", "BelleAurore.ttf", "La Belle Aurore -- a hurried cursive hand"),
    ("hand4", "ShadowsIntoLight.ttf", "Shadows Into Light -- neat, plain handwriting"),
]

pdf = Packet()
for fam, ttf, label in HANDS:
    pdf.add_font(fam, "", os.path.join(F, ttf))

for i, (fam, ttf, label) in enumerate(HANDS):
    if i % 2 == 0:
        pdf.add_page()
        pdf.paint_bg()
        pdf.set_text_color(*FAINT)
    pdf.set_text_color(*RED)
    pdf.set_font("Times", "I", 10)
    pdf.cell(0, 6, label, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_text_color(*INK)
    pdf.set_font(fam, "", 15)
    pdf.multi_cell(0, 8.5, TEXT, align="L")
    pdf.ln(4)
    if i % 2 == 0:
        pdf.rule(width=50)
        pdf.ln(6)

out = os.path.join(BASE, "_hands.pdf")
pdf.output(out)
print("wrote", out, pdf.page_no(), "pages")
