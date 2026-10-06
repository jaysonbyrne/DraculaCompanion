# Assets

Binary assets are **not** tracked in this repo (GitHub file limits and the
MCP push channel cap out well below the plates' ~60MB). Everything needed to
rebuild the book is documented here; the full asset set lives with the build
environment.

## Fonts (`fonts/`)

All freely licensed, all on Google Fonts:

| File | Typeface | Used for |
|---|---|---|
| `Fell.ttf` | IM Fell English | body prose, drop caps |
| `Fell-Italic.ttf` | IM Fell English Italic | datelines, notes |
| `FellSC.ttf` | IM Fell English SC | small-caps labels |
| `Blackletter.ttf` | UnifrakturMaguntia | titles, part-heads, "Of the Vampyre" |
| `BelleAurore.ttf` | La Belle Aurore | handwritten letters |
| `SpecialElite.ttf` | Special Elite | telegrams |
| `Playfair.ttf` / `Playfair-Bold.ttf` / `Playfair-Italic.ttf` / `Playfair-Black.ttf` | Playfair Display | newspaper & notice headlines |
| `Pinyon.ttf` / `Caveat.ttf` / `HomemadeApple.ttf` / `ShadowsIntoLight.ttf` | (various) | handwriting candidates, not used in the final build |

## Plates (`ch*/plates/`, `ancient/`)

101 finished plate images (~60MB). Every plate's generation prompt is stored
in its chapter's `content.py` (`plates: [{file, title, caption, prompt}]`),
so any plate can be regenerated from its prompt. The ancient woodcuts live
in `ancient/` (`village-woodcut`, `bat-woodcut`, `strigoi-frontispiece`).

## Built PDFs

`dracula_companion_complete.pdf` and per-chapter PDFs are build artifacts —
rebuild with `python3 build_master.py && python3 bind_cover.py`. The
published master is uploaded to the Internet Archive (see
`archive-org-listing.txt`).
