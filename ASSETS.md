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

The three reading volumes (`novel/dracula_text.pdf`,
`novel/dracula_illustrated.pdf`, `novel/dracula_pocket.pdf`) are likewise
build artifacts — rebuild with the `novel/` scripts (see README). Listing
metadata for their Internet Archive uploads lives in
`novel/archive-org-listing-{text,illustrated,pocket}.txt`.

## Reading-volume cover art (binary, not tracked)

- **Vampire painting** — the illustrated edition's cover: a gothic oil
  painting of the Count on a castle terrace under a bat-filled moonlit
  sky. Regenerate prompt: "Spooky gothic oil painting, tall portrait
  composition: a pale vampire count with dark slicked hair and a
  high-collared black cloak standing on a castle terrace, a moonlit
  gothic castle looming behind him, bats wheeling in a stormy night sky,
  mist coiling around stone balustrades, dramatic chiaroscuro, Victorian
  horror book illustration style. Dark shadowy tones in the upper third
  with space for a title. No text, no watermark." The white title is
  composited by `novel/bind_novel_cover.py`.
- **Brown leather texture** — the pocket edition's Moleskine cover base:
  "Close-up photograph of a plain brown leather notebook cover,
  moleskine style, smooth cognac-brown leather with fine natural grain
  texture, soft even studio lighting, completely blank with no text and
  no logos, tall portrait orientation, no watermark."
  `novel/moleskine_cover.jpg` is composed from it by
  `novel/make_moleskine_cover.py` (debossed title) and is also untracked.
