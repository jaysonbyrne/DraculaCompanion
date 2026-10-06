"""Type specimen: the proposed new typographic system for the Companion."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from packet import Packet, INK, RED, FAINT

BASE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(BASE, "fonts")


def register(pdf):
    pdf.add_font("fell", "", os.path.join(F, "Fell.ttf"))
    pdf.add_font("fell", "I", os.path.join(F, "Fell-Italic.ttf"))
    pdf.add_font("fellsc", "", os.path.join(F, "FellSC.ttf"))
    pdf.add_font("pinyon", "", os.path.join(F, "Pinyon.ttf"))
    pdf.add_font("elite", "", os.path.join(F, "SpecialElite.ttf"))
    pdf.add_font("playfair", "", os.path.join(F, "Playfair.ttf"))
    pdf.add_font("playfair", "B", os.path.join(F, "Playfair-Bold.ttf"))
    pdf.add_font("playfair", "I", os.path.join(F, "Playfair-Italic.ttf"))
    pdf.add_font("black", "", os.path.join(F, "Playfair-Black.ttf"))
    pdf.add_font("goth", "", os.path.join(F, "Blackletter.ttf"))


pdf = Packet()
register(pdf)
pdf.set_title("A Proof of New Types")

# ---------------- page 1: display faces ----------------
pdf.add_page()
pdf.paint_bg()
pdf.set_text_color(*FAINT)
pdf.set_font("fell", "I", 10)
pdf.cell(0, 6, "A proof of new types for the Companion", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.rule(width=50)
pdf.ln(6)
pdf.set_text_color(*INK)
pdf.set_font("goth", "", 30)
pdf.multi_cell(0, 14, "The Complete\nDracula Companion", align="C")
pdf.ln(4)
pdf.set_font("fell", "I", 11)
pdf.set_text_color(*FAINT)
pdf.multi_cell(0, 6, "Being the ephemera of all twenty-eight chapters,\nin period types", align="C")
pdf.ln(8)
pdf.rule(width=50)
pdf.ln(6)
pdf.set_text_color(*RED)
pdf.set_font("fellsc", "", 15)
pdf.cell(0, 8, "Of the Papers", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_text_color(*INK)
pdf.set_font("fell", "", 11)
pdf.multi_cell(0, 5.8,
               "The body of the book would be set in IM Fell English \u2014 a "
               "face cut in the seventeenth century and still perfectly legible, "
               "with all the ink and irregularity of the hand-press. Chapter "
               "labels and running heads in Fell Small Caps; the great title "
               "and part-heads in blackletter, as a Victorian binder would "
               "have lettered them in gold.",
               align="J")

# ---------------- page 2: the documents ----------------
pdf.add_page()
pdf.paint_bg()
pdf.set_text_color(*FAINT)
pdf.set_font("fell", "I", 10)
pdf.cell(0, 6, "The documents, in their own hands", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
pdf.rule(width=50)
pdf.ln(5)
pdf.set_text_color(*INK)
pdf.set_font("pinyon", "", 15)
pdf.multi_cell(0, 8,
               "My dearest Mina,\u2014\nI must tell you my news. Mr. Holmwood "
               "was here yesterday and proposed to me! I felt very sad, for "
               "I do so love him, and yet I could not love him as a husband "
               "ought to be loved\u2026\nYour loving\nLucy",
               align="L")
pdf.ln(4)
pdf.rule(width=50)
pdf.ln(5)
pdf.set_font("elite", "", 11)
pdf.multi_cell(0, 6,
               "WESTERN UNION TELEGRAM\n\nTO HAWKINS, EXETER.\nCOUNT DETAINED "
               "ME STOP LEAVE THURSDAY MORNING STOP MEET ME AT EXETER "
               "STOP \u2014 JONATHAN",
               align="L")
pdf.ln(4)
pdf.rule(width=50)
pdf.ln(5)
pdf.set_font("black", "", 17)
pdf.cell(0, 8, "THE HAMPSTEAD MYSTERY", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_font("fell", "", 10.5)
pdf.multi_cell(0, 5.6,
               "The neighbourhood of Hampstead is just at present exercised "
               "with a series of events which seem to run on lines parallel "
               "to those of what was known to the writers of headlines as "
               "\u201cThe Kensington Horror.\u201d",
               align="J")

# ---------------- page 3: a chapter opening ----------------
pdf.add_page()
pdf.paint_bg()
pdf.set_text_color(*RED)
pdf.set_font("fellsc", "", 12)
pdf.cell(0, 7, "Chapter the First", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
pdf.rule(width=50)
pdf.ln(3)
pdf.set_text_color(*INK)
pdf.set_font("fell", "", 19)
pdf.multi_cell(0, 9, "JONATHAN HARKER\u2019S JOURNAL", align="C")
pdf.ln(1)
pdf.set_font("fell", "I", 10.5)
pdf.set_text_color(*FAINT)
pdf.cell(0, 6, "3rd \u2013 5th May \u2014 Bistritz to the Borgo Pass",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)
# drop cap + opening lines
pdf.set_text_color(*INK)
pdf.set_font("fell", "", 34)
x0 = pdf.l_margin
y0 = pdf.get_y()
pdf.text(x0, y0 + 11, "3")
pdf.set_xy(x0 + 13, y0)
pdf.set_font("fell", "", 11)
pdf.multi_cell(103, 5.8,
               "May. Bistritz.\u2014Left Munich at 8:35 P.M., on 1st May, "
               "arriving at Vienna early next morning; should have arrived "
               "at 6:46, but train was an hour late. The impression I had "
               "was that we were leaving the West and entering the East.",
               align="J")
pdf.ln(2)
pdf.multi_cell(0, 5.8,
               "The most western of splendid bridges over the Danube, which "
               "is here of noble width and depth, took us among the traditions "
               "of Turkish rule.", align="J")

out = os.path.join(BASE, "_specimen.pdf")
pdf.output(out)
print("wrote", out, pdf.page_no(), "pages")
