# -*- coding: latin-1 -*-
"""Chapter 2 content for the Dracula companion.

TEMPLATE NOTES for later chapters (read before writing ch03-ch28):
- All text must be latin-1 only: use -- for dashes, straight quotes, no bullets,
  no em dashes, no curly quotes, no special symbols.
- CHAPTER dict keys: number, label ("CHAPTER TWO"), title, subtitle, epigraph.
- docs: list of dicts with num ("No. I."...), title, subtitle (optional), style,
  paras (list of paragraph strings).
- Styles and their extra keys:
    prose     -- paras
    notice    -- lead (bold centered line), paras
    letter    -- opening (list, e.g. salutation), paras (italic), signoff, signature
    bill      -- bill_title, bill_sub, items=[(desc, price), ...], total, note
    telegram  -- tfrom, tto, tdated, body (use STOP between sentences)
    broadside -- paras (rendered centered, large)
    timetable -- rows=[(station, kind, time), ...], note, paras
- plates: after_doc = 0-based index of the doc AFTER which the plate appears;
  numeral ("Plate I."), file (relative to chapter folder), title, caption,
  prompt (image prompt: "19th century oil painting, vertical portrait
  composition: ..." or antique-map style; no text except on maps; no watermark).
- Aim: 5-7 documents, exactly 3 plates per chapter.
- Ground every document in the chapter's actual events. Check the Project
  Gutenberg text of Dracula (https://www.gutenberg.org/cache/epub/345/pg345.txt)
  when unsure. Short quotes from the novel are fine (public domain).
- Voice: period pastiche, dry wit where apt, never modern slang.
"""
CHAPTER = {
    "number": 2,
    "label": "CHAPTER TWO",
    "title": "JONATHAN HARKER'S JOURNAL",
    "subtitle": "5th -- 7th May -- the Castle",
    "epigraph": '"Welcome to my house! Enter freely and of your own will!"',
    "docs": [
        {
            "num": "No. I.",
            "title": "COPY OF A LETTER.",
            "subtitle": "From Jonathan Harker to Mina Murray; entrusted to the Count for posting.",
            "style": "letter",
            "paras": [
                "My dearest Mina, --",
                "I am safely arrived at the Castle, after a journey which I shall tell you of one day, and which for strangeness exceeds anything I have known. The Count received me himself at the door, and made me most welcome; he is a very charming gentleman, though of a certain old-fashioned courtesy, and his house is beyond anything I had imagined.",
                "I have a beautiful room, and a library full of English books, so that I shall not want for occupation. Do not be anxious about me, my dear; the business goes well, and I hope to be home within the month.",
                "I must close now, as the Count is waiting to take this letter with his own hand. Give my love to Lucy, and keep all my love for yourself.",
            ],
            "signoff": "-- Your loving",
            "signature": "JONATHAN.",
        },
        {
            "num": "No. II.",
            "title": "THE COUNT'S LIBRARY.",
            "subtitle": "A partial catalogue, taken down by Mr. Harker from the shelves.",
            "style": "prose",
            "paras": [
                "The library is a vast and lamplit room, and the shelves are crowded in a manner I have seldom seen outside the Inns of Court. What strikes the visitor at once is the singularity of the collection: history, geography, politics, political economy, botany, geology, law --",
                "And all, without exception, relating to England and English life, and English customs and manners. There are gazetteers and directories, Whitaker's Almanack, the Army and Navy Lists, Bradshaw's Guide, and a quantity of newspapers and periodicals.",
                "One cannot but admire the industry which has gathered, in this remote fastness, so complete a picture of a country its master has never seen; nor can one altogether escape the question -- to what end?",
            ],
        },
        {
            "num": "No. III.",
            "title": "NOTICE.",
            "subtitle": "By order of the Count; pinned inside the door of the guest's chamber.",
            "style": "notice",
            "lead": "THE GUEST IS ENTREATED TO OBSERVE THE FOLLOWING.",
            "paras": [
                "You will find all doors locked, save those of your own chambers and the rooms appointed for your use. This is the custom of the house, and is not to be questioned.",
                "You are entreated not to stray from your chambers at night, nor to enter any room whose door you find shut. There are bad dreams for those who sleep unwisely.",
                "Should you require anything, you have only to ring; though I must warn you that there are no servants in the house, and your wants will be attended to -- in due course.",
            ],
        },
        {
            "num": "No. IV.",
            "title": "SUPPER.",
            "subtitle": "Bill of fare, as laid in the great dining-room; the host did not dine.",
            "style": "bill",
            "bill_title": "CASTLE DRACULA.",
            "bill_sub": "Supper laid for Mr. Harker -- 5th May, 1893.",
            "items": [
                ("Cold chicken, dressed", "--"),
                ("Cheese and salad", "--"),
                ("A bottle of Tokay", "--"),
                ("Coffee, black", "--"),
                ("Company of the host at table", "declined"),
            ],
            "total": "TOTAL ............ no charge -- the guest is most welcome.",
            "note": "(The Count excused himself from eating, saying he had dined already. He sat by me all the while, and talked most entertainingly.)",
        },
        {
            "num": "No. V.",
            "title": "OF THE HOSPITALITY OF NOBLEMEN.",
            "subtitle": 'Extract from "Customs of the Transylvanian Boyars" (Vienna, 1888).',
            "style": "prose",
            "paras": [
                "It is the immemorial custom among the great houses of Transylvania that a guest, once bidden across the threshold, is received with the words: \"Enter freely and of your own will.\" The formula is very ancient, and the peasantry attach to it a curious importance.",
                "They will tell you that no one -- not even a beggar, not even, they whisper, something worse -- may pass an unbidden threshold; and that the invitation, once given, may not be withdrawn. Whether this be mere superstition, or the relic of some older law of sanctuary, the traveller must judge for himself.",
                "The wise visitor will note the words, and remember them.",
            ],
        },
        {
            "num": "No. VI.",
            "title": "THE CHILDREN OF THE NIGHT.",
            "subtitle": "Heard from the window of the guest's chamber, after midnight.",
            "style": "broadside",
            "paras": [
                "Listen to them --",
                "the children of the night.",
                "What music they make!",
            ],
        },
    ],
    "plates": [
        {
            "after_doc": 0,
            "file": "plates/arrival.jpg",
            "numeral": "Plate I.",
            "title": "THE ARRIVAL.",
            "caption": "The carriage halts in the castle courtyard; the Count himself opens the door.",
            "prompt": "19th century oil painting, vertical portrait composition: a horse-drawn carriage halting at night in the vast stone courtyard of a ruined Carpathian castle, a tall figure in black waiting in a great arched doorway holding a lamp, moonlight on broken battlements. Deeply atmospheric, Victorian book-illustration style. No text, no watermark.",
        },
        {
            "after_doc": 2,
            "file": "plates/count.jpg",
            "numeral": "Plate II.",
            "title": "THE COUNT.",
            "caption": "A tall old man, clean shaven save for a long white moustache, clad in black.",
            "prompt": "19th century oil painting, vertical portrait composition: a very tall distinguished old man with a long white moustache and aquiline nose, dressed entirely in black, standing in a stone archway holding an antique silver lamp, his greeting hand extended. Dignified and faintly unsettling, Victorian book-illustration style. No text, no watermark.",
        },
        {
            "after_doc": 3,
            "file": "plates/library.jpg",
            "numeral": "Plate III.",
            "title": "THE LIBRARY.",
            "caption": "Shelves crowded with English books, in a castle no Englishman was meant to leave.",
            "prompt": "19th century oil painting, vertical portrait composition: a vast lamplit castle library at night, towering shelves crammed with old books, a globe and scattered maps of England on a great table, a single green-shaded lamp glowing. Rich and scholarly, faintly ominous, Victorian book-illustration style. No text, no watermark.",
        },
    ],
}
