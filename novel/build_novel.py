#!/usr/bin/env python3
"""Build the two Dracula reading volumes:
   - dracula_text.pdf        (full text + references to the Companion)
   - dracula_illustrated.pdf (full text + references + embedded figures)

Run from anywhere:  python3 build_novel.py [text|illustrated|both]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter

# Portable paths: this file lives in novel/ (repo checkout) or
# dracula-text/ (dev workspace). The companion sources live in the repo
# root, or in dracula-companion/ next to dracula-text/ in dev.
TXTD = Path(__file__).resolve().parent
COMP = (TXTD.parent if (TXTD.parent / 'inventory.json').is_file()
        else TXTD.parent / 'dracula-companion')
CACHE = TXTD / 'fig_cache'
CACHE.mkdir(exist_ok=True)

IVORY = (248, 240, 222)
INK = (26, 22, 20)
CRIMSON = (150, 30, 40)
FAINT = (120, 100, 80)
GOLD = (176, 141, 79)
def _font_dir(*cands):
    for c in cands:
        if Path(c).is_dir():
            return c
    return cands[0]

NOTO = _font_dir('/usr/share/fonts/truetype/noto', '/usr/share/fonts/noto')
SANS = _font_dir('/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/dejavu')

WORDS = ("One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve "
         "Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen "
         "Twenty Twenty-One Twenty-Two Twenty-Three Twenty-Four "
         "Twenty-Five Twenty-Six Twenty-Seven").split()


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


# ---------------------------------------------------------------- load ---
def load_all():
    chapters = {}
    for n in range(1, 28):
        chapters[n] = (TXTD / f'ch{n:02d}.txt').read_text(encoding='utf-8')
    anchors = []
    for f in ('anchors_01_09.json', 'anchors_10_18.json', 'anchors_19_28.json'):
        anchors.extend(json.loads((TXTD / f).read_text(encoding='utf-8')))
    inv = json.loads((COMP / 'inventory.json').read_text(encoding='utf-8'))
    inv_by_ch = {c['ch']: c for c in inv['chapters']}
    return chapters, anchors, inv_by_ch


def chapter_pdf_path(ch):
    if ch == 'ch01':
        return COMP / 'ch01' / 'dracula_chapter1_ephemera.pdf'
    return COMP / ch / f'dracula_{ch}_ephemera.pdf'


def cover_path(ch):
    p = COMP / ch / 'cover.jpg'
    return p if p.exists() else None


# ------------------------------------------------- figure page mapping ---
_page_text_cache = {}


def page_texts(ch):
    if ch not in _page_text_cache:
        reader = PdfReader(str(chapter_pdf_path(ch)))
        _page_text_cache[ch] = [(pg.extract_text() or '') for pg in reader.pages]
        _page_text_cache[ch + '_n'] = len(reader.pages)
    return _page_text_cache[ch]


def map_items_to_pages(ch, items):
    """Return {id(item_index): (start0, end0)} page spans in the chapter PDF."""
    texts = page_texts(ch)
    spans = {}
    pos = 0
    order = []
    for idx, it in enumerate(items):
        title = it['title']
        key = title.rstrip('.')
        found = None
        if len(key) >= 4:
            for p in range(pos, len(texts)):
                if key in texts[p]:
                    found = p
                    break
        if found is None:  # fallback: numeral
            for p in range(pos, len(texts)):
                if it['numeral'] in texts[p]:
                    found = p
                    break
        if found is None:
            print(f'  WARN: no page for {ch} {it["numeral"]} {title!r}')
            continue
        spans[idx] = [found, found]
        order.append(idx)
        pos = found
    for k, idx in enumerate(order):
        if k + 1 < len(order):
            spans[idx][1] = spans[order[k + 1]][0] - 1
        else:
            spans[idx][1] = len(texts) - 1
        if spans[idx][1] < spans[idx][0]:
            spans[idx][1] = spans[idx][0]
    return spans


def chapter_page_images(ch):
    """Render every page of the chapter PDF once; return sorted PNG paths."""
    pdf_path = chapter_pdf_path(ch)
    n = len(PdfReader(str(pdf_path)).pages)
    prefix = CACHE / f'{ch}_pg'
    have = sorted(CACHE.glob(f'{ch}_pg-*.png'),
                  key=lambda p: int(p.stem.rsplit('-', 1)[-1]))
    if len(have) < n:
        subprocess.run(['pdftoppm', '-png', '-r', '110', str(pdf_path),
                        str(prefix)], check=True, capture_output=True)
        have = sorted(CACHE.glob(f'{ch}_pg-*.png'),
                      key=lambda p: int(p.stem.rsplit('-', 1)[-1]))
    return have


def plate_image_path(ch, image):
    p = COMP / ch / 'plates' / image
    return p if p.exists() else None


def _tq(s):
    return (s.replace('\u2019', "'").replace('\u2018', "'")
             .replace('\u201c', '"').replace('\u201d', '"'))


# ------------------------------------------------------- anchor wiring ---
def wire_anchors(chapters, anchors, inv_by_ch):
    """Attach figure info to anchors; group by novel chapter.
    Returns {novel_ch: [entry,...]} with entry = dict(anchor, ref_label,
    kind, numeral, title, fig_files, cover...) and a list of warnings."""
    by_ch = {}
    warnings = []
    # group inventory items per chapter for page mapping
    for a in anchors:
        ch = a['ch']
        nch = a['novel_ch']
        items = [it for it in inv_by_ch[ch]['items']
                 if it['kind'] in ('doc', 'plate', 'map', 'watercolour')]
        # find this anchor's item
        match = [it for it in items
                 if it['numeral'].rstrip('.') == a['numeral'].rstrip('.')
                 and _tq(it['title']) == _tq(a['title'])]
        if not match:
            warnings.append(f"no inventory item for {ch} {a['numeral']} {a['title']!r}")
            continue
        it = match[0]
        entry = dict(a)
        entry['numeral'] = it['numeral']  # canonical companion numeral
        entry['kind'] = it['kind']
        entry['ref_ch'] = int(ch[2:])  # companion chapter number
        entry['fig_files'] = []
        entry['fig_kind'] = None
        if it['kind'] in ('plate', 'map', 'watercolour'):
            img = plate_image_path(ch, it['image']) if it.get('image') else None
            if img is None:
                warnings.append(f"missing image {ch} {a['numeral']} {it.get('image')}")
            else:
                entry['fig_files'] = [img]
                entry['fig_kind'] = 'art'
        else:  # doc -> facsimile pages
            spans = map_items_to_pages(ch, items)
            idx = items.index(it)
            if idx not in spans:
                warnings.append(f"no page span {ch} {a['numeral']}")
            else:
                s0, e0 = spans[idx]
                try:
                    imgs = chapter_page_images(ch)
                    entry['fig_files'] = imgs[s0:e0 + 1]
                    entry['fig_kind'] = 'doc'
                except subprocess.CalledProcessError as e:
                    warnings.append(f"render failed {ch} {a['numeral']}: {e}")
        by_ch.setdefault(nch, []).append(entry)
    return by_ch, warnings

# ------------------------------------------------------------ renderer ---
class Novel(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A5')
        self.set_margins(18, 20, 18)
        self.set_auto_page_break(True, 22)
        self.add_font('Novel', '', NOTO + 'NotoSerif-Regular.ttf')
        self.add_font('Novel', 'B', NOTO + 'NotoSerif-Bold.ttf')
        self.add_font('Novel', 'I', NOTO + 'NotoSerif-Italic.ttf')
        self.add_font('Novel', 'BI', NOTO + 'NotoSerif-BoldItalic.ttf')
        self.add_font('Sans', '', SANS + 'DejaVuSans.ttf')
        self.add_font('Sans', 'B', SANS + 'DejaVuSans-Bold.ttf')
        self.add_font('Sans', 'I', SANS + 'DejaVuSans.ttf')
        self.show_folio = True
        self.ch_starts = {}

    def header(self):
        self.set_fill_color(*IVORY)
        self.rect(0, 0, 148, 210, 'F')

    def footer(self):
        if not self.show_folio or self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_font('Sans', '', 8)
        self.set_text_color(*FAINT)
        self.cell(0, 5, str(self.page_no()), align='C')
        self.set_x(self.l_margin)

    # -- primitives ------------------------------------------------------
    def ornament(self, y=None, width=44):
        if y is not None:
            self.set_y(y)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        x = (148 - width) / 2
        yy = self.get_y()
        self.line(x, yy, x + width, yy)
        self.set_y(yy + 4)

    def para(self, text, style='', size=10.5, h=5.6, color=INK,
             after=2.4, align='J'):
        self.set_x(self.l_margin)
        self.set_font('Novel', style, size)
        self.set_text_color(*color)
        self.multi_cell(0, h, text, align=align, markdown=True)
        self.ln(after)

    def ref_note(self, entry):
        label = (f"\u25c6 Companion, Ch. {entry['ref_ch']}, "
                 f"{entry['numeral']} \u2014 {entry['title']}")
        self.set_x(self.l_margin)
        self.set_font('Sans', 'I', 8.2)
        self.set_text_color(*CRIMSON)
        self.multi_cell(0, 4.6, label, align='L', markdown=False)
        self.set_text_color(*INK)
        self.ln(1.6)


def em(text):
    """_italics_ -> __italics__ for fpdf2 markdown; -- -> em dash."""
    text = re.sub(r'_([^_\n]+)_', r'__\1__', text)
    return text.replace('--', '\u2014')


def split_head(p):
    """Leading _..._ span -> (head, rest) if short."""
    m = re.match(r'_([^_\n]{2,72})_', p)
    if m:
        return m.group(1), p[m.end():].lstrip()
    return None, p


def is_display_head(p):
    s = p.strip()
    return (3 <= len(s) <= 64 and s == s.upper()
            and re.fullmatch(r'[A-Z0-9\s\.\,\;:\'\"\u2014\u2013\-\!\?\(\)]+', s)
            is not None)


def chapter_paras(raw):
    lines = raw.split('\n')
    while lines and re.match(r'\s*CHAPTER\s+[IVXLC]+\s*$', lines[0]):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    flavor = ''
    if lines and is_display_head(lines[0]):
        flavor = lines.pop(0).strip()
        while lines and not lines[0].strip():
            lines.pop(0)
    text = '\n'.join(lines)
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    return flavor, paras


def attach_anchors(paras, entries):
    """Return (attached, unmatched). attached[i] = [(pos, entry)]."""
    np_list = [norm(p) for p in paras]
    full = ' '.join(np_list)
    offs = []
    o = 0
    for np_ in np_list:
        offs.append(o)
        o += len(np_) + 1
    import bisect
    attached = [[] for _ in paras]
    unmatched = []
    for e in entries:
        na = norm(e['anchor'])
        occ = e.get('occurrence', 1)
        idx = -1
        for _ in range(occ):
            idx = full.find(na, idx + 1)
            if idx < 0:
                break
        if idx < 0:
            unmatched.append(e)
            continue
        pi = bisect.bisect_right(offs, idx) - 1
        attached[pi].append((idx - offs[pi], e))
    for lst in attached:
        lst.sort(key=lambda t: t[0])
    return attached, unmatched


def fit_box(iw, ih, max_w, max_h):
    s = min(max_w / iw, max_h / ih)
    return iw * s, ih * s


def figure_art(pdf, entry):
    for f in entry['fig_files']:
        pdf.add_page()
        with Image.open(f) as im:
            iw, ih = im.size
        w, h = fit_box(iw, ih, 112, 148)
        x = (148 - w) / 2
        y = max(24, (178 - h) / 2)
        pdf.image(str(f), x=x, y=y, w=w, h=h)
        pdf.set_y(y + h + 6)
        pdf.set_font('Sans', 'I', 8.2)
        pdf.set_text_color(*FAINT)
        pdf.multi_cell(0, 4.6,
                       f"Companion, Ch. {entry['ref_ch']} \u2014 "
                       f"{entry['numeral']} {entry['title']}",
                       align='C', markdown=False)
        pdf.set_text_color(*INK)


def figure_doc(pdf, entry):
    for f in entry['fig_files']:
        pdf.add_page()
        with Image.open(f) as im:
            iw, ih = im.size
        w, h = fit_box(iw, ih, 120, 150)
        x = (148 - w) / 2
        y = max(20, (182 - h) / 2)
        pdf.image(str(f), x=x, y=y, w=w, h=h)
        pdf.set_y(y + h + 5)
        pdf.set_font('Sans', 'I', 8.2)
        pdf.set_text_color(*FAINT)
        pdf.cell(0, 4.6,
                 f"Companion, Ch. {entry['ref_ch']}, {entry['numeral']}",
                 align='C', markdown=False,
                 new_x='LMARGIN', new_y='NEXT')
        pdf.set_x(pdf.l_margin)
        pdf.set_text_color(*INK)


def render_chapter(pdf, n, raw, entries, cover, illustrated):
    flavor, paras = chapter_paras(raw)
    attached, unmatched = attach_anchors(paras, entries)
    for e in unmatched:
        print(f'  anchor fallback to chapter end: ch{n} {e["numeral"]} {e["title"]!r}')
        attached[-1].append((10 ** 9, e))
    attached[-1].sort(key=lambda t: t[0])
    pdf.ch_starts[n] = pdf.page_no() + 1
    if cover:
        pdf.add_page()
        pdf.image(str(cover), x=0, y=0, w=148, h=210)
    # chapter head
    pdf.add_page()
    pdf.ln(34)
    pdf.set_font('Sans', '', 10)
    pdf.set_text_color(*FAINT)
    pdf.cell(0, 6, f'C H A P T E R  {WORDS[n-1].upper()}', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)
    pdf.ornament(width=52)
    if flavor:
        pdf.set_font('Novel', 'BI', 12)
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, 6.5, em(flavor), align='C', markdown=True)
        pdf.ln(6)
    # body
    for i, p in enumerate(paras):
        head, rest = split_head(p)
        if head and rest:
            pdf.set_font('Novel', 'BI', 11)
            pdf.set_text_color(*INK)
            pdf.multi_cell(0, 6, em(head), align='L', markdown=True)
            pdf.ln(1)
            pdf.para(em(rest), after=2.4)
        elif is_display_head(p) and len(p) < 64:
            pdf.set_font('Sans', 'B', 9)
            pdf.set_text_color(*CRIMSON)
            pdf.multi_cell(0, 5.5, p.strip(), align='C', markdown=False)
            pdf.set_text_color(*INK)
            pdf.ln(2.5)
        else:
            pdf.para(em(p), after=2.4)
        for _, e in attached[i]:
            pdf.ref_note(e)
            if illustrated and e['fig_files']:
                if e['fig_kind'] == 'art':
                    figure_art(pdf, e)
                else:
                    figure_doc(pdf, e)
    return unmatched

# ------------------------------------------------------------------ main ---
NOTE_TEXT = (
    "This book is the first of a set of two. The second volume, the Companion, "
    "gathers the very papers this story is made of \u2014 letters and telegrams, "
    "newspaper cuttings, bills and timetables, maps and painted plates \u2014 "
    "chapter by chapter, as period documents you can hold in your hands.\n\n"
    "Every \u25c6 in these pages points to one of those papers, naming its place "
    "in the Companion: chapter, number and title. {figure_sentence}\n\n"
    "Read straight through, or follow the marks and read the papers as they "
    "come. Either way, you are reading the story the way its tellers lived it: "
    "one document at a time."
)
FIGURE_SENTENCE = {
    'text': ("In this volume the papers themselves live in the Companion; "
             "turn to it whenever a mark catches your eye."),
    'illustrated': ("In this Illustrated Edition each paper is also set into "
                    "the narrative as a figure, exactly where the story speaks "
                    "of it \u2014 so the letter, the cutting, the map appears "
                    "in your hands as it appears in theirs."),
}


def render_front(mode, flavors, numbers):
    f = Novel()
    f.show_folio = False
    # title page
    f.add_page()
    f.ln(40)
    f.ornament(width=60)
    f.ln(6)
    f.set_font('Novel', 'B', 46)
    f.set_text_color(*INK)
    f.cell(0, 18, 'DRACULA', align='C', new_x='LMARGIN', new_y='NEXT')
    f.ln(4)
    f.set_font('Sans', '', 11)
    f.set_text_color(*CRIMSON)
    f.cell(0, 7, 'AN ILLUSTRATED EDITION' if mode == 'illustrated' else 'THE TEXT',
           align='C', new_x='LMARGIN', new_y='NEXT')
    f.set_font('Sans', '', 9)
    f.set_text_color(*FAINT)
    f.cell(0, 6, 'with the papers & plates of the Companion'
           if mode == 'illustrated' else 'with references to the Companion',
           align='C', new_x='LMARGIN', new_y='NEXT')
    f.ln(10)
    f.ornament(width=44)
    f.ln(8)
    f.set_font('Novel', '', 13)
    f.set_text_color(*INK)
    f.cell(0, 8, 'Bram Stoker', align='C', new_x='LMARGIN', new_y='NEXT')
    f.set_font('Sans', '', 9)
    f.set_text_color(*FAINT)
    f.cell(0, 6, '1897', align='C', new_x='LMARGIN', new_y='NEXT')
    # note
    f.add_page()
    f.ln(18)
    f.set_font('Sans', 'B', 10)
    f.set_text_color(*CRIMSON)
    f.cell(0, 7, 'A NOTE ON THIS EDITION', align='C', new_x='LMARGIN', new_y='NEXT')
    f.ln(2)
    f.ornament(width=44)
    f.ln(4)
    f.set_font('Sans', '', 9.5)
    f.set_text_color(*INK)
    f.multi_cell(0, 5.8, NOTE_TEXT.format(figure_sentence=FIGURE_SENTENCE[mode]),
                 align='J', markdown=False)
    # contents
    f.add_page()
    f.set_font('Sans', 'B', 10)
    f.set_text_color(*CRIMSON)
    f.cell(0, 7, 'CONTENTS', align='C', new_x='LMARGIN', new_y='NEXT')
    f.ln(2)
    f.ornament(width=44)
    f.ln(5)
    for n in range(1, 28):
        label = f'Chapter {WORDS[n - 1]}'
        if flavors[n]:
            label += f' \u2014 {flavors[n]}'
        pg = numbers[n]
        f.set_font('Novel', '', 9.5)
        f.set_text_color(*INK)
        lw = f.get_string_width('  ' + label + ' ')
        pw = f.get_string_width(' ' + str(pg) + '  ')
        dots_w = 112 - lw - pw
        ndots = max(2, int(dots_w / f.get_string_width('. ')))
        f.cell(lw, 6, '  ' + label)
        f.set_text_color(*FAINT)
        f.cell(dots_w, 6, '. ' * ndots)
        f.set_text_color(*INK)
        f.cell(pw, 6, ' ' + str(pg) + '  ', align='R',
               new_x='LMARGIN', new_y='NEXT')
    return f


def build(mode):
    assert mode in ('text', 'illustrated')
    chapters, anchors, inv_by_ch = load_all()
    print('wiring anchors & preparing figures...', flush=True)
    by_ch, warnings = wire_anchors(chapters, anchors, inv_by_ch)
    for w in warnings[:40]:
        print(' ', w)
    total = sum(len(v) for v in by_ch.values())
    print(f'{total} anchors wired, {len(warnings)} warnings', flush=True)

    flavors = {}
    for n in range(1, 28):
        fl, _ = chapter_paras(chapters[n])
        flavors[n] = fl

    pdf = Novel()
    for n in range(1, 28):
        ch = f'ch{n:02d}'
        print(f'  chapter {n}...', flush=True)
        render_chapter(pdf, n, chapters[n], by_ch.get(n, []),
                       cover_path(ch), illustrated=(mode == 'illustrated'))
    body_tmp = TXTD / f'_body_{mode}.pdf'
    pdf.output(str(body_tmp))

    draft = render_front(mode, flavors, {n: 0 for n in range(1, 28)})
    n_front = len(draft.pages)
    numbers = {n: pdf.ch_starts[n] + n_front for n in range(1, 28)}
    front = render_front(mode, flavors, numbers)
    front_tmp = TXTD / f'_front_{mode}.pdf'
    front.output(str(front_tmp))

    writer = PdfWriter()
    for p in PdfReader(str(body_tmp)).pages:
        pass
    for p in PdfReader(str(front_tmp)).pages:
        writer.add_page(p)
    base = len(writer.pages)
    for p in PdfReader(str(body_tmp)).pages:
        writer.add_page(p)
    title = ('Dracula \u2014 An Illustrated Edition'
             if mode == 'illustrated' else 'Dracula \u2014 The Text')
    for n in range(1, 28):
        writer.add_outline_item(f'Chapter {WORDS[n - 1]}',
                                base + pdf.ch_starts[n] - 1)
    writer.add_metadata({'/Title': title, '/Author': 'Bram Stoker'})
    out = TXTD / ('dracula_illustrated.pdf' if mode == 'illustrated'
                  else 'dracula_text.pdf')
    with open(out, 'wb') as fh:
        writer.write(fh)
    body_tmp.unlink()
    front_tmp.unlink()
    print(f'wrote {out} ({len(writer.pages)} pages)')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'both'
    if which in ('text', 'both'):
        build('text')
    if which in ('illustrated', 'both'):
        build('illustrated')
