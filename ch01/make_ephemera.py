#!/usr/bin/env python3
"""Build a PDF packet of period-style ephemera for Dracula Chapter 1."""
import os
from fpdf import FPDF

PAPER = (253, 251, 244)
INK = (28, 22, 20)
RED = (158, 24, 32)
GOLD = (172, 134, 44)
GOLD_LT = (214, 178, 90)
CREAM = (232, 205, 130)
FAINT = (120, 105, 85)
CLOTH = (126, 17, 23)

FONTS_DIR = "/home/hatch/workspace/dracula-companion/fonts"
_FONT_FILES = {
    "fell": {"": "Fell.ttf", "I": "Fell-Italic.ttf"},
    "fellsc": {"": "FellSC.ttf"},
    "goth": {"": "Blackletter.ttf"},
    "hand": {"": "BelleAurore.ttf"},
    "pf": {"": "Playfair.ttf", "B": "Playfair-Bold.ttf", "I": "Playfair-Italic.ttf"},
    "pfblack": {"": "Playfair-Black.ttf"},
}

class Packet(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A5")
        self.set_margins(16, 16, 16)
        self.set_auto_page_break(True, margin=18)
        self.no_footer = False
        for fam, styles in _FONT_FILES.items():
            for style, fn in styles.items():
                self.add_font(fam, style, os.path.join(FONTS_DIR, fn))

    def header(self):
        self.set_fill_color(*PAPER)
        self.rect(0, 0, 148, 210, "F")

    def footer(self):
        if self.no_footer or self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_font("fell", "I", 9)
        self.set_text_color(*GOLD)
        self.cell(0, 6, f"· {self.page_no()} ·", align="C")

    def paint_bg(self):
        self.set_fill_color(*PAPER)
        self.rect(0, 0, 148, 210, "F")

    def paint_cloth(self):
        self.set_fill_color(*CLOTH)
        self.rect(0, 0, 148, 210, "F")

    def rule(self, width=88, gap=2.2, double=True):
        x1 = (148 - width) / 2
        y = self.get_y()
        self.set_draw_color(*RED)
        self.set_line_width(0.5)
        self.line(x1, y, x1 + width, y)
        if double:
            self.set_draw_color(*GOLD)
            self.set_line_width(0.25)
            self.line(x1, y + gap, x1 + width, y + gap)
        self.set_y(y + gap + 3.5)

    def plate(self, numeral, img_path, title, caption):
        from PIL import Image as PILImage
        self.add_page()
        self.paint_bg()
        self.set_text_color(*RED)
        self.set_font("fellsc", "", 10)
        self.cell(0, 6, numeral, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.rule(width=50)
        iw, ih = PILImage.open(img_path).size
        aspect = iw / ih
        header_used = self.get_y() - 16
        caption_h = 24
        avail_h = 210 - 16 - 18 - header_used - caption_h
        w = min(116, avail_h * aspect)
        h = w / aspect
        x = (148 - w) / 2
        y = self.get_y() + max(0, (avail_h - h) / 2)
        self.image(img_path, x=x, y=y, w=w, h=h)
        self.set_y(self.get_y() + avail_h + 2)
        self.set_font("fell", "", 11.5)
        self.set_text_color(*INK)
        self.cell(0, 6, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("fell", "I", 9.5)
        self.set_text_color(*FAINT)
        self.multi_cell(0, 5, caption, align="C")

    def doc_head(self, number, title, subtitle=None):
        self.add_page()
        self.paint_bg()
        self.set_text_color(*RED)
        self.set_font("fellsc", "", 10)
        self.cell(0, 6, number, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.rule()
        self.set_text_color(*INK)
        self.set_font("fell", "", 15)
        self.multi_cell(0, 7, title, align="C")
        if subtitle:
            self.ln(1)
            self.set_font("fell", "I", 10.5)
            self.multi_cell(0, 5.5, subtitle, align="C")
        self.ln(2)
        self.rule()
        self.ln(1)

    def para(self, text, size=11, style="", align="J", after=3.5, color=INK):
        self.set_font("fell", style, size)
        self.set_text_color(*color)
        self.multi_cell(0, 5.8, text, align=align)
        self.ln(after)

    def center(self, text, size=11, style="", after=3.5):
        self.para(text, size=size, style=style, align="C", after=after)


pdf = Packet()
pdf.set_title("Side-Papers & Ephemera pertaining to Chapter I of Dracula")
pdf.set_author("Collected for the reader's amusement")

# ---------------- Cloth cover ----------------
pdf.add_page()
pdf.paint_cloth()
pdf.no_footer = True
pdf.set_draw_color(*GOLD_LT)
pdf.set_line_width(1.1)
pdf.rect(9, 9, 130, 192)
pdf.set_line_width(0.35)
pdf.rect(13, 13, 122, 184)
pdf.set_text_color(*GOLD_LT)
pdf.ln(32)
pdf.set_font("fellsc", "", 12)
pdf.cell(0, 7, "Side-Papers  &  Ephemera", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
pdf.set_font("fell", "I", 11)
pdf.set_text_color(*CREAM)
pdf.cell(0, 6, "pertaining to Chapter the First of", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.set_font("goth", "", 40)
pdf.set_text_color(*GOLD_LT)
pdf.cell(0, 18, 'Dracula', align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font("fell", "I", 11)
pdf.set_text_color(*CREAM)
pdf.cell(0, 6, "by Bram Stoker", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)
y = pdf.get_y()
pdf.set_draw_color(*GOLD_LT)
pdf.set_line_width(0.5)
pdf.line(59, y, 89, y)
pdf.set_y(y + 6)
pdf.set_font("fell", "I", 10)
pdf.set_text_color(*CREAM)
pdf.multi_cell(
    0, 5.8,
    "Being a packet of Traveller's Notices, Handbills, Extracts,\nTime-Bills, Accounts & Plates, such as Mr. Jonathan Harker,\nSolicitor, of Exeter, might have picked up, been handed,\nor had pressed upon him, upon the road from Bistritz\nto the Borgo Pass, 3rd -- 5th May, 1893.",
    align="C",
)
pdf.ln(6)
y = pdf.get_y()
pdf.line(59, y, 89, y)
pdf.set_y(y + 8)
pdf.set_font("fell", "I", 11)
pdf.set_text_color(*GOLD_LT)
pdf.multi_cell(0, 6, '"Welcome to the Carpathians."\n-- Count Dracula, to Mr. Harker', align="C")
pdf.no_footer = False

# ---------------- Chapter cover ----------------
pdf.add_page()
pdf.paint_bg()
_cover = "/home/hatch/workspace/dracula-companion/ch01/cover.jpg"
if os.path.exists(_cover):
    from PIL import Image as _PI
    _iw, _ih = _PI.open(_cover).size
    _a = _iw / _ih
    _w = min(116, 118 * _a)
    _h = _w / _a
    _x = (148 - _w) / 2
    pdf.image(_cover, x=_x, y=12, w=_w, h=_h)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.4)
    pdf.rect(_x - 1.5, 10.5, _w + 3, _h + 3)
    pdf.set_y(12 + _h + 5)
else:
    pdf.ln(34)
pdf.set_text_color(*RED)
pdf.set_font("fellsc", "", 10.5)
pdf.cell(0, 5.5, "Chapter One", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
pdf.rule(width=44)
pdf.ln(1)
pdf.set_text_color(*INK)
pdf.set_font("fell", "", 14)
pdf.cell(0, 7, "JONATHAN HARKER'S JOURNAL", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
pdf.set_font("fell", "I", 10)
pdf.set_text_color(*FAINT)
pdf.cell(0, 5.5, "3rd -- 5th May -- Bistritz to the Borgo Pass", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.set_font("fell", "I", 9.5)
pdf.multi_cell(0, 5.5, '"Welcome to the Carpathians."\n-- Count Dracula, to Mr. Harker', align="C")

PL = "/home/hatch/workspace/dracula-companion/ch01/plates"
pdf.plate("Frontispiece.", f"{PL}/frontispiece.jpg",
          "THE TRAVELLER'S PAPERS, AS THEY SURVIVE.",
          "Mr. Harker's journal, the Count's letter, the landlady's crucifix,\nthe diligence notice, the inn bill, and the map of the Borgo road.")
pdf.plate("Plate I.", f"{PL}/journey.jpg",
          "MR. HARKER'S JOURNEY, APRIL -- MAY 1893.",
          "From London by Munich, Vienna, Buda-Pesth and Klausenburg to Bistritz;\nthence by diligence to the Borgo Pass. (Mr. Harker notes that no\nOrdnance Survey of these parts exists; this will have to do.)")
pdf.plate("Watercolour I.", f"{PL}/wc_munich.png",
          "MUNICH -- 1ST MAY, 8:35 P.M.",
          "The train for Vienna; the journey begins at dusk.")
pdf.plate("Watercolour II.", f"{PL}/wc_vienna.png",
          "VIENNA -- 2ND MAY, DAWN.",
          "St. Stephen's in the morning light; already an hour late.")
pdf.plate("Watercolour III.", f"{PL}/wc_budapest.png",
          "BUDA-PESTH -- THE DANUBE.",
          "\"A wonderful place\" -- and here the Count's warning letter finds him.")
pdf.plate("Watercolour IV.", f"{PL}/wc_klausenburg.png",
          "KLAUSENBURG -- THE MOUNTAIN HALT.",
          "Sheepskin coats on the platform; the pines close in.")
pdf.plate("Watercolour V.", f"{PL}/wc_bistritz.png",
          "BISTRITZ -- 3RD MAY.",
          "Market morning; the Golden Crown; paprika hendl.")
pdf.plate("Watercolour VI.", f"{PL}/wc_borgo.png",
          "THE BORGO PASS -- 4TH MAY, DUSK.",
          "The diligence climbs toward the appointed meeting.")
pdf.plate("Plate II.", f"{PL}/map.jpg",
          "THE ROAD FROM BISTRITZ TO THE BORGO PASS.",
          "After the manner of the old hand-drawn charts;\nBistritz west, Bukovina east, the Castle beyond the Pass.")

# ---------------- No. II : Hotel notice ----------------
pdf.doc_head("No. II.", "THE GOLDEN CROWN HOTEL",
             "(Goldene Krone) -- Bistritz, Transylvania")
pdf.set_font("pf", "B", 11)
pdf.set_text_color(*INK)
pdf.multi_cell(0, 5.8, "NOTICE TO TRAVELLERS BOUND FOR THE BORGO ROAD.", align="C")
pdf.ln(3.5)
pdf.para(
    "The Diligence for Bukovina departs from the courtyard of this house punctually "
    "at THREE o'clock in the afternoon. Travellers are entreated to take their seats "
    "a full quarter of an hour before the time."
)
pdf.para(
    "The road over the Borgo Pass is NOT to be attempted after nightfall. No carriage "
    "is despatched from this house after sunset, and none is received after midnight. "
    "Gentlemen proceeding to the Castle are advised to provide themselves with warm "
    "clothing, and to carry their papers upon their persons."
)
pdf.para(
    "N.B. -- The Eve of St. George (kept this year upon the 4th of May) is observed in "
    "these parts with certain old customs. Visitors are earnestly requested to remain "
    "within doors after dark, and to take no notice of lights seen moving upon the hills."
)
pdf.ln(2)
pdf.center("By order,", size=11, style="I", after=1)
pdf.set_font("pf", "B", 11)
pdf.set_text_color(*INK)
pdf.multi_cell(0, 5.8, "THE PROPRIETOR.", align="C")
pdf.ln(3.5)
pdf.plate("Plate III.", f"{PL}/inn.jpg",
          "THE GOLDEN CROWN, BISTRITZ.",
          "The diligence waits in the yard; the landlady watches from the door.")

# ---------------- No. III : Handbook extract ----------------
pdf.doc_head("No. III.", "BISTRITZ AND THE BORGO PASS.",
             'Extract from "A Handbook for Travellers in Transylvania\nand the Carpathian Highlands" (London, 1891).')
pdf.para(
    "BISTRITZ (Hung. Beszterce). -- A clean, well-built Saxon town of some 8,000 souls, "
    "with a fine Gothic church and a good inn, the Golden Crown; one of the pleasantest "
    "halting-places between Klausenburg and the Bukovina frontier. The surrounding hills "
    "are richly wooded, and the air is accounted most salubrious."
)
pdf.para(
    "The BORGO PASS (about 1,200 metres). -- The post-road climbs hence through unbroken "
    "pine forest to the summit, which marks the old frontier; beyond it lies Bukovina. "
    "The country is thinly peopled by Wallach shepherds and Slovak woodcutters; wolves "
    "are still numerous in the winter months, and the traveller will do well to keep to "
    "the diligence and to make the crossing by daylight."
)
pdf.para(
    "Inns beyond Bistritz are few and of the humblest description. Let the traveller see "
    "that his business at the Castle, or elsewhere in those parts, is concluded in good "
    "time to return by the afternoon coach.",
    color=FAINT, style="I", size=10,
)
pdf.plate("Plate IV.", f"{PL}/bistritz.jpg",
          "BISTRITZ, MARKET MORNING.",
          "The Gothic church, the gabled houses, and the foothills beyond.")

# ---------------- No. IV : St. George's Eve pamphlet ----------------
pdf.doc_head("No. IV.", "ST. GEORGE'S EVE IN TRANSYLVANIA.",
             "Being a short account of the customs observed upon that night;\nprinted for the information of travellers.")
pdf.para(
    "St. George's Day falls upon the 23rd of April by the Old Style, which is the 5th of "
    "May by the New; and its Eve is kept through all Transylvania with more earnestness "
    "than any night of the year, Christmas alone excepted."
)
pdf.para(
    "After sunset no prudent householder suffers his door to stand open. Garlic is hung "
    "at the lintel, the sign of the Cross is chalked upon the door-post, and a crucifix "
    "or a rosary is carried by all who must go abroad -- which the wise do not."
)
pdf.para(
    "For upon this one night, it is said, all the evil things in the world have full sway: "
    "the dead walk abroad, and lights are seen moving in lonely places where no living "
    "foot should tread. The stranger who laughs at these customs will find no company "
    "for his laughter after dark."
)
pdf.para(
    "The peasant will further tell you that upon St. George's Eve, and upon that Eve "
    "alone, treasures buried in the earth since the days of the Romans betray themselves "
    "by a pale blue flame, which burns where the gold lies hid. (See No. V.)"
)

# ---------------- No. V : Blue flames broadside ----------------
pdf.doc_head("No. V.", "THE BLUE FLAMES.",
             "A Word to Treasure-Seekers. -- Posted at Bistritz.")
pdf.ln(2)
pdf.center("Upon St. George's Eve, and upon that Eve alone,", size=12, after=2)
pdf.center("the gold and silver hidden in the earth", size=12, after=2)
pdf.center("since the days of the Romans and the Turks", size=12, after=2)
pdf.center("give up their secret, and burn with a blue flame", size=12, after=2)
pdf.center("where they lie.", size=12, after=6)
pdf.rule(width=40)
pdf.ln(2)
pdf.para(
    "But let the seeker mark this well. The flame moves as you move, and stands only "
    "while you stand still. Speak but one word, and it is gone. Many a man has followed "
    "these lights into the pines, lantern in hand, and been found at morning wandering "
    "and witless -- or not found at all."
)
pdf.para(
    "Dig only where the flame has burned steadfast, and dig in silence; and be within "
    "doors, and your door barred, before the clock strikes twelve."
)
pdf.ln(2)
pdf.center("-- old saying of the Borgo road --", size=10, style="I")
pdf.plate("Plate V.", f"{PL}/blue_flames.jpg",
          "THE BLUE FLAMES.",
          "Where the gold lies hid, the flame burns blue --\ndig in silence, and speak no word.")

# ---------------- No. VI : Timetable ----------------
pdf.doc_head("No. VI.", "IMPERIAL-ROYAL PRIVILEGED POST-DILIGENCE.",
             "Bistritz -- Borgo Prund -- Vatra Dornei (Bukovina).")
pdf.para("Departures daily, Sundays excepted. Times are approximate, the state of the roads permitting.",
         size=10, style="I", color=FAINT)
pdf.ln(1)
rows = [
    ("Bistritz (yard of the Golden Crown)", "dep.", "3.00 p.m."),
    ("Borgo Prund", "arr.", "6.30 p.m."),
    ("Borgo Prund", "dep.", "7.00 p.m."),
    ("Summit of the Borgo Pass", "arr.", "9.15 p.m."),
    ("Vatra Dornei, Bukovina", "arr.", "11.40 p.m."),
]
pdf.set_font("pf", "B", 10.5)
pdf.set_text_color(*INK)
pdf.set_draw_color(*RED)
cw = [72, 16, 28]
for st, kind, t in rows:
    x0 = pdf.get_x()
    pdf.cell(cw[0], 7, st, border="B")
    pdf.cell(cw[1], 7, kind, border="B", align="C")
    pdf.cell(cw[2], 7, t, border="B", align="R", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
pdf.para("FARES. -- Inside, 2 fl. 40 kr.; Outside, 1 fl. 80 kr. Luggage above 20 kilos "
         "charged extra. The Company accepts no responsibility for delays occasioned by "
         "weather, wolves, or the condition of the roads.", size=10.5)
pdf.para("Passengers for the Castle of Count Dracula are met at the Borgo Pass by private "
         "carriage, by prior arrangement with his lordship.",
         size=10.5, style="I", color=FAINT)
pdf.plate("Plate VI.", f"{PL}/diligence.jpg",
          "THE DILIGENCE ON THE BORGO ROAD.",
          "Climbing through the pines at dusk; the wolves are not yet heard.")

# ---------------- No. VII : The Count's letter ----------------
pdf.doc_head("No. VII.", "COPY OF A LETTER.",
             "Received by Mr. Jonathan Harker, Solicitor, of Exeter,\nfrom Count Dracula of Transylvania; April, 1893.")
pdf.ln(2)
pdf.set_text_color(*INK)
pdf.set_font("hand", "", 14)
_x0, _w = 26, 96
pdf.set_x(_x0)
pdf.multi_cell(_w, 8, '"My Friend. --', new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_x(_x0)
pdf.multi_cell(_w, 8,
    "Welcome to the Carpathians. I am anxiously expecting you. Sleep well to-night. "
    "At three to-morrow the diligence will start for Bukovina; a place on it is kept "
    "for you. At the Borgo Pass my carriage will await you and will bring you to me. "
    "I trust that your journey from London has been a happy one, and that you will "
    "enjoy your stay in my beautiful land.",
    align="J", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2.5)
pdf.set_x(_x0)
pdf.multi_cell(_w, 8, "-- Your friend,", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
pdf.set_font("hand", "", 16)
pdf.set_x(_x0)
pdf.multi_cell(_w, 8.5, "DRACULA.", align="R", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
pdf.para("(Transcribed literatim from the original, the English of which, though quaint, "
         "is perfectly intelligible.)", size=10, style="I", color=FAINT)
pdf.plate("Plate VII.", f"{PL}/castle.jpg",
          "THE CASTLE, BY MOONLIGHT.",
          "One window lit. The Count is expecting you.")

# ---------------- No. VIII : Peoples note ----------------
pdf.doc_head("No. VIII.", "OF THE PEOPLES OF THE CARPATHIANS.",
             "A traveller's note, for those who ride the Borgo road.")
pdf.para(
    "Four nations divide Transylvania among them, and the traveller will meet them all "
    "before he is two days out of Bistritz. The SAXONS, in the south, are thrifty townsfolk "
    "of German speech, builders of the walled churches. The WALLACHS, in the west and "
    "south, are shepherds and tillers of the soil. The SZEKELYS, in the east, are a hardy "
    "frontier people, and account themselves the noblest stock of all."
)
pdf.para(
    "Upon the road itself you will see SLOVAKS -- tall, broad-shouldered fellows in "
    "broad-brimmed hats, baggy white trousers, and great leather belts -- going up into "
    "the hills with their axes; and, camped by the wayside, the SZGANY, the wandering "
    "tinkers and horse-dealers, whose fires you will smell long before you see their tents."
)
pdf.para(
    "They are a picturesque company, and civil enough to the civil traveller; but keep "
    "to the diligence, keep your papers about you, and be civil in return.",
    style="I", color=FAINT, size=10.5,
)

# ---------------- No. IX : Inn bill ----------------
pdf.add_page()
pdf.paint_bg()
pdf.set_text_color(*INK)
pdf.set_font("fell", "I", 10)
pdf.cell(0, 6, "No. IX.", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
pdf.rule()
pdf.set_font("pfblack", "", 13)
pdf.set_text_color(*RED)
pdf.cell(0, 8, "THE GOLDEN CROWN, BISTRITZ.", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(*INK)
pdf.set_font("fell", "", 10.5)
pdf.cell(0, 6, "Bill rendered to Mr. J. Harker -- 4th May, 1893.", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.rule()
pdf.ln(2)
items = [
    ("Supper -- paprika hendl", "60 kr."),
    ("Bottle of Tokay, best", "1 fl. 20 kr."),
    ("Bed, best chamber, one night", "80 kr."),
    ("Breakfast, coffee & rolls", "30 kr."),
    ("Ostler -- diligence booked to Borgo", "20 kr."),
    ("One crucifix, pressed upon the guest", "gratis"),
]
pdf.set_font("fell", "", 10.5)
_space_w = pdf.get_string_width(" ")
_dot_w = pdf.get_string_width(".")
_price_col_w = max(pdf.get_string_width(p) for _, p in items) + 3
_desc_avail = 116 - _price_col_w
for desc, price in items:
    _n_dots = int((_desc_avail - pdf.get_string_width(desc) - _space_w) / _dot_w)
    if _n_dots >= 2:
        pdf.cell(_desc_avail, 6.5, desc + " " + "." * _n_dots,
                 new_x="RIGHT", new_y="TOP")
        pdf.cell(_price_col_w, 6.5, " " + price, align="R",
                 new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.multi_cell(0, 6.5, desc, new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6.5, price, align="R", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.rule()
pdf.ln(1)
pdf.set_font("pf", "B", 11)
pdf.set_text_color(*RED)
_t_space_w = pdf.get_string_width(" ")
_t_dot_w = pdf.get_string_width(".")
_tleft, _tright = "TOTAL", "3 fl. 10 kr. -- Paid with thanks."
_t_n_dots = int((116 - pdf.get_string_width(_tleft)
                 - pdf.get_string_width(_tright) - 2 * _t_space_w) / _t_dot_w)
pdf.cell(0, 7, f"{_tleft} " + "." * max(2, _t_n_dots) + f" {_tright}",
         align="R", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)
pdf.set_font("fell", "I", 10)
pdf.set_text_color(*FAINT)
pdf.multi_cell(0, 5.5, "(The landlady begs the gentleman will wear the crucifix without "
               "fail upon the road, and will on no account remove it from about his neck.)",
               align="C")

# ---------------- Colophon ----------------
pdf.add_page()
pdf.paint_bg()
pdf.ln(60)
pdf.rule(width=60)
pdf.ln(2)
pdf.set_text_color(*FAINT)
pdf.set_font("fell", "I", 10)
pdf.multi_cell(0, 6,
               "End of the packet.\nSet by hand, as it were, and printed for private "
               "amusement to accompany a reading of Bram Stoker's Dracula, Chapter I.\n\n"
               "Bistritz -- Borgo Pass -- the Castle.\nOctober, 2026.",
               align="C")

out = "/home/hatch/workspace/dracula-companion/ch01/dracula_chapter1_ephemera.pdf"
pdf.output(out)
print("wrote", out)
