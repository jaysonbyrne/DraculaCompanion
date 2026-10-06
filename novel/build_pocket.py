#!/usr/bin/env python3
"""Pocket edition of Dracula for iPhone 14: moleskine-style notebook.
Page 104 x 225 mm matches the iPhone 14 screen ratio (1170:2532).
Full novel text + companion references + figures as portrait pages.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_novel as B
from fpdf import FPDF
from PIL import Image
from pypdf import PdfReader, PdfWriter

PW, PH = 104, 225
CREAM = (250, 244, 230)
CW = PW - 22  # content width


class Pocket(B.Novel):
    def __init__(self):
        FPDF.__init__(self, orientation='P', unit='mm', format=(PW, PH))
        self.set_margins(11, 13, 11)
        self.set_auto_page_break(True, 15)
        self.add_font('Novel', '', B.NOTO + 'NotoSerif-Regular.ttf')
        self.add_font('Novel', 'B', B.NOTO + 'NotoSerif-Bold.ttf')
        self.add_font('Novel', 'I', B.NOTO + 'NotoSerif-Italic.ttf')
        self.add_font('Novel', 'BI', B.NOTO + 'NotoSerif-BoldItalic.ttf')
        self.add_font('Sans', '', B.SANS + 'DejaVuSans.ttf')
        self.add_font('Sans', 'B', B.SANS + 'DejaVuSans-Bold.ttf')
        self.add_font('Sans', 'I', B.SANS + 'DejaVuSans.ttf')
        self.show_folio = True
        self.ch_starts = {}

    def header(self):
        self.set_fill_color(*CREAM)
        self.rect(0, 0, self.w, self.h, 'F')

    def footer(self):
        if not self.show_folio or self.page_no() == 1:
            return
        self.set_y(-11)
        self.set_font('Sans', '', 7.5)
        self.set_text_color(*B.FAINT)
        self.cell(0, 4, str(self.page_no()), align='C')
        self.set_x(self.l_margin)

    def ornament(self, y=None, width=34):
        if y is not None:
            self.set_y(y)
        self.set_draw_color(*B.GOLD)
        self.set_line_width(0.5)
        x = (PW - width) / 2
        yy = self.get_y()
        self.line(x, yy, x + width, yy)
        self.set_y(yy + 4)

    def para(self, text, style='', size=12, h=7, color=B.INK,
             after=3, align='J'):
        if self.w > self.h:
            self.add_page(orientation='P')
        self.set_x(self.l_margin)
        self.set_font('Novel', style, size)
        self.set_text_color(*color)
        self.multi_cell(0, h, text, align=align, markdown=True)
        self.ln(after)

    def ref_note(self, entry):
        label = (f"\u25c6 Companion, Ch. {entry['ref_ch']}, "
                 f"{entry['numeral']} \u2014 {entry['title']}")
        self.set_x(self.l_margin)
        self.set_font('Sans', 'I', 9)
        self.set_text_color(*B.CRIMSON)
        self.multi_cell(0, 5, label, align='L', markdown=False)
        self.set_text_color(*B.INK)
        self.ln(2)


def pk_figure(pdf, entry):
    for f in entry['fig_files']:
        with Image.open(f) as im:
            iw, ih = im.size
        if iw > ih * 1.12:
            # wide document -> landscape page of its own
            pdf.add_page(orientation='L')
            w, h = B.fit_box(iw, ih, PH - 22, PW - 40)
            x = (PH - w) / 2
            y = max(12, (PW - h) / 2 - 4)
            pdf.image(str(f), x=x, y=y, w=w, h=h)
            pdf.set_y(y + h + 4)
            cap_w = w
        else:
            pdf.add_page()
            w, h = B.fit_box(iw, ih, 82, 168)
            x = (PW - w) / 2
            y = max(16, (198 - h) / 2)
            pdf.image(str(f), x=x, y=y, w=w, h=h)
            pdf.set_y(y + h + 5)
            cap_w = w
        pdf.set_font('Sans', 'I', 8)
        pdf.set_text_color(*B.FAINT)
        if entry['fig_kind'] == 'art':
            cap = (f"Companion, Ch. {entry['ref_ch']} \u2014 "
                   f"{entry['numeral']} {entry['title']}")
        else:
            cap = f"Companion, Ch. {entry['ref_ch']}, {entry['numeral']}"
        pdf.multi_cell(0, 4.4, cap, align='C', markdown=False)
        pdf.set_text_color(*B.INK)


def ref_card(pdf, entry):
    """A reference that looks like the document itself: a small facsimile
    card slipped into the text where the story mentions it."""
    if pdf.w > pdf.h:
        pdf.add_page(orientation='P')
    f = entry['fig_files'][0]
    with Image.open(f) as im:
        iw, ih = im.size
    tw, th = B.fit_box(iw, ih, 42, 46)
    if pdf.get_y() + th + 24 > PH - 15:
        pdf.add_page()
    x = (PW - tw) / 2
    y = pdf.get_y() + 3
    pdf.set_fill_color(253, 250, 242)
    pdf.set_draw_color(168, 148, 118)
    pdf.set_line_width(0.4)
    pdf.rect(x - 2.5, y - 2.5, tw + 5, th + 5, 'DF')
    pdf.image(str(f), x=x, y=y, w=tw, h=th)
    pdf.set_y(y + th + 6)
    pdf.set_x(pdf.l_margin)
    pdf.set_font('Sans', 'I', 7.5)
    pdf.set_text_color(*B.CRIMSON)
    label = (f"\u25c6 Companion, Ch. {entry['ref_ch']}, "
             f"{entry['numeral']} \u2014 {entry['title']}")
    pdf.multi_cell(0, 4.2, label, align='C', markdown=False)
    pdf.set_text_color(*B.INK)
    pdf.ln(3)


def pk_render_chapter(pdf, n, raw, entries, cover):
    flavor, paras = B.chapter_paras(raw)
    attached, unmatched = B.attach_anchors(paras, entries)
    for e in unmatched:
        print(f'  anchor fallback to chapter end: ch{n} {e["numeral"]} {e["title"]!r}')
        attached[-1].append((10 ** 9, e))
    attached[-1].sort(key=lambda t: t[0])
    pdf.ch_starts[n] = pdf.page_no() + 1
    if cover:
        pdf.show_folio = False
        if pdf.page_no() == 0 or pdf.w > pdf.h or pdf.get_y() > pdf.t_margin + 2:
            pdf.add_page(orientation='P')
        with Image.open(cover) as im:
            iw, ih = im.size
        w, h = B.fit_box(iw, ih, PW, PH)
        pdf.image(str(cover), x=(PW - w) / 2, y=(PH - h) / 2, w=w, h=h)
        pdf.show_folio = True
    pdf.add_page()
    pdf.ln(26)
    pdf.set_font('Sans', '', 9)
    pdf.set_text_color(*B.FAINT)
    pdf.cell(0, 6, f'C H A P T E R  {B.WORDS[n-1].upper()}', align='C',
             new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)
    pdf.ornament(width=40)
    if flavor:
        pdf.set_font('Novel', 'BI', 12.5)
        pdf.set_text_color(*B.INK)
        pdf.multi_cell(0, 7, B.em(flavor), align='C', markdown=True)
        pdf.ln(5)
    for i, p in enumerate(paras):
        head, rest = B.split_head(p)
        if head and rest:
            pdf.set_x(pdf.l_margin)
            pdf.set_font('Novel', 'BI', 12.5)
            pdf.set_text_color(*B.INK)
            pdf.multi_cell(0, 7, B.em(head), align='L', markdown=True)
            pdf.ln(1.2)
            pdf.para(B.em(rest))
        elif B.is_display_head(p) and len(p) < 64:
            pdf.set_x(pdf.l_margin)
            pdf.set_font('Sans', 'B', 9.5)
            pdf.set_text_color(*B.CRIMSON)
            pdf.multi_cell(0, 6, p.strip(), align='C', markdown=False)
            pdf.set_text_color(*B.INK)
            pdf.ln(3)
        else:
            pdf.para(B.em(p))
        for _, e in attached[i]:
            if e['fig_files']:
                ref_card(pdf, e)
                pk_figure(pdf, e)
                pdf.add_page(orientation='P')  # fresh portrait for following text
            else:
                pdf.ref_note(e)


def pk_front(numbers, flavors):
    f = Pocket()
    f.show_folio = False
    # moleskine cover
    f.add_page()
    f.image(str(B.TXTD / 'moleskine_cover.jpg'), x=0, y=0, w=PW, h=PH)
    # title page
    f.add_page()
    f.ln(52)
    f.ornament(width=44)
    f.ln(6)
    f.set_font('Novel', 'B', 34)
    f.set_text_color(*B.INK)
    f.cell(0, 15, 'DRACULA', align='C', new_x='LMARGIN', new_y='NEXT')
    f.ln(3)
    f.set_font('Sans', '', 9)
    f.set_text_color(*B.CRIMSON)
    f.cell(0, 6, 'POCKET EDITION', align='C', new_x='LMARGIN', new_y='NEXT')
    f.set_font('Sans', '', 8)
    f.set_text_color(*B.FAINT)
    f.cell(0, 5, 'for the iPhone \u00b7 with the papers & plates of the Companion',
           align='C', new_x='LMARGIN', new_y='NEXT')
    f.ln(12)
    f.ornament(width=34)
    f.ln(8)
    f.set_font('Novel', '', 12)
    f.set_text_color(*B.INK)
    f.cell(0, 7, 'Bram Stoker', align='C', new_x='LMARGIN', new_y='NEXT')
    f.set_font('Sans', '', 8)
    f.set_text_color(*B.FAINT)
    f.cell(0, 5, '1897', align='C', new_x='LMARGIN', new_y='NEXT')
    # note
    f.add_page()
    f.ln(22)
    f.set_font('Sans', 'B', 9)
    f.set_text_color(*B.CRIMSON)
    f.cell(0, 6, 'A NOTE ON THIS EDITION', align='C', new_x='LMARGIN', new_y='NEXT')
    f.ln(2)
    f.ornament(width=34)
    f.ln(4)
    f.set_font('Sans', '', 10)
    f.set_text_color(*B.INK)
    f.multi_cell(0, 6.4, B.NOTE_TEXT.format(
        figure_sentence=B.FIGURE_SENTENCE['illustrated']), align='J', markdown=False)
    # contents
    f.add_page()
    f.set_font('Sans', 'B', 9)
    f.set_text_color(*B.CRIMSON)
    f.cell(0, 6, 'CONTENTS', align='C', new_x='LMARGIN', new_y='NEXT')
    f.ln(2)
    f.ornament(width=34)
    f.ln(5)
    for n in range(1, 28):
        label = f'{n}. {B.WORDS[n-1]}'
        if flavors[n]:
            label += f' \u2014 {flavors[n]}'
        pg = numbers[n]
        f.set_font('Novel', '', 10)
        f.set_text_color(*B.INK)
        lw = f.get_string_width(' ' + label + ' ')
        pw = f.get_string_width(' ' + str(pg) + ' ')
        dots_w = CW - lw - pw
        ndots = max(2, int(dots_w / f.get_string_width('. ')))
        f.cell(lw, 6.4, ' ' + label)
        f.set_text_color(*B.FAINT)
        f.cell(dots_w, 6.4, '. ' * ndots)
        f.set_text_color(*B.INK)
        f.cell(pw, 6.4, ' ' + str(pg) + ' ', align='R',
               new_x='LMARGIN', new_y='NEXT')
    return f


def main():
    chapters, anchors, inv_by_ch = B.load_all()
    print('wiring anchors & preparing figures...', flush=True)
    by_ch, warnings = B.wire_anchors(chapters, anchors, inv_by_ch)
    for w in warnings[:20]:
        print(' ', w)
    print(f'{sum(len(v) for v in by_ch.values())} anchors wired, '
          f'{len(warnings)} warnings', flush=True)

    flavors = {}
    for n in range(1, 28):
        fl, _ = B.chapter_paras(chapters[n])
        flavors[n] = fl

    pdf = Pocket()
    for n in range(1, 28):
        ch = f'ch{n:02d}'
        print(f'  chapter {n}...', flush=True)
        pk_render_chapter(pdf, n, chapters[n], by_ch.get(n, []), B.cover_path(ch))
    body_tmp = B.TXTD / '_body_pocket.pdf'
    pdf.output(str(body_tmp))

    draft = pk_front({n: 0 for n in range(1, 28)}, flavors)
    n_front = len(draft.pages)
    numbers = {n: pdf.ch_starts[n] + n_front for n in range(1, 28)}
    front = pk_front(numbers, flavors)
    front_tmp = B.TXTD / '_front_pocket.pdf'
    front.output(str(front_tmp))

    writer = PdfWriter()
    for p in PdfReader(str(front_tmp)).pages:
        writer.add_page(p)
    base = len(writer.pages)
    for p in PdfReader(str(body_tmp)).pages:
        writer.add_page(p)
    for n in range(1, 28):
        writer.add_outline_item(f'Chapter {B.WORDS[n-1]}', base + pdf.ch_starts[n] - 1)
    writer.add_metadata({'/Title': 'Dracula \u2014 Pocket Edition',
                         '/Author': 'Bram Stoker'})
    out = B.TXTD / 'dracula_pocket.pdf'
    with open(out, 'wb') as fh:
        writer.write(fh)
    body_tmp.unlink()
    front_tmp.unlink()
    print(f'wrote {out} ({len(writer.pages)} pages)')


if __name__ == '__main__':
    main()
