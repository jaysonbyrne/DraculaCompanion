# The Dracula Companion

Period ephemera & painted plates for Bram Stoker's *Dracula* — a 415-page
companion volume built chapter by chapter: every in-world document of the
novel (letters, journals, telegrams, newspaper cuttings, notices, bills,
timetables) reset as a facsimile of the paper itself, interleaved with
oil-painting-style plates.

Opens with "Of the Papers" (a catalogue of the novel's source documents,
each with a mock artifact photograph) and a large numbered journey map with
notes keyed to chapters. Chapter 18 carries "Of the Vampyre," an archaic
blackletter extract with its own cover and woodcut title page.

## The book

- A5, gothic dust-jacket cover bound in front
- Ivory paper, crimson-and-gold design language throughout
- Period typography: IM Fell English body (with drop caps), Fell Small Caps
  labels, blackletter titles, La Belle Aurore handwritten letters,
  Special Elite typewriter telegrams, Playfair Black headlines
- Built PDFs are **not** tracked here (they exceed GitHub's file limits);
  the current master is published to the Internet Archive —
  see `archive-org-listing.txt` for the listing metadata.

## Build

Requires Python 3 with `fpdf2`, `Pillow`, and `pymupdf`:

```sh
python3 build_master.py      # builds any missing chapter PDFs, binds the volume
python3 bind_cover.py        # binds the dust-jacket cover in front
```

Chapter PDFs are cached per chapter — `build_master.py` only rebuilds
chapters whose PDF is missing, so after changing anything in `lib/`
(fonts, renderers, backgrounds) delete the `ch*/dracula_ch*.pdf` files
first or stale pages silently survive.

Chapter 1 uses its own builder (`ch01/make_ephemera.py`); chapters 2–28
use `lib/build_chapter.py`.

## Layout

- `lib/` — shared design system: `packet.py` (page, fonts, backgrounds),
  `render.py` (document renderers: letter, notice, telegram, cutting,
  broadside, timetable, bill, ancient), `build_chapter.py`
- `ch01/` … `ch28/` — one folder per chapter: `content.py` (all text and
  plate prompts), `plates/` (finished plate art)
- `works/` — "Of the Papers" catalogue data and the journey-map notes
- `ancient/` — the "Of the Vampyre" woodcuts
- `fonts/` — the period typefaces (IM Fell, blackletter, La Belle Aurore, …)
- `archive-org-listing.txt` — title/description metadata for the
  Internet Archive upload

## Lessons

- Deliver rebuilt PDFs to readers under a **unique filename per build** —
  clients cache attachments by path.
- fpdf2 automatic page breaks don't run renderer code: the paper background
  is painted in `Packet.header()`, which fires on every page.
- Letters auto-shrink (14→13→12pt) when that's all it takes to hold a
  letter on one page — no widowed sign-offs.
