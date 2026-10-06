# -*- coding: latin-1 -*-
"""Chapter 16 content for the Dracula companion.

TEMPLATE NOTES (from ch02, followed throughout):
- All text is latin-1 only: -- for dashes, straight quotes, no bullets,
  no em dashes, no curly quotes, no special symbols.
- CHAPTER dict keys: number, label, title, subtitle, epigraph, docs, plates.
- Styles: prose (paras), notice (lead + paras), letter (opening + paras
  italic + signoff + signature), bill (bill_title, bill_sub, items, total,
  note), telegram (tfrom, tto, tdated, body with STOP), broadside (paras
  centered), timetable (rows, note, paras).
- Exactly 3 plates per chapter; after_doc is the 0-based index of the doc
  AFTER which the plate appears.
"""
CHAPTER = {
    "number": 16,
    "label": "CHAPTER SIXTEEN",
    "title": "DR. SEWARD'S DIARY",
    "subtitle": "29th -- 30th September -- the staking of Lucy",
    "epigraph": '"She is God\'s true dead, whose soul is with Him!"',
    "docs": [
        {
            "num": "No. I.",
            "title": "THE SEALING OF THE TOMB.",
            "subtitle": "29th September, a quarter before midnight.",
            "style": "prose",
            "paras": [
                "It was just a quarter before twelve o'clock when we got into the churchyard over the low wall. The night was dark with occasional gleams of moonlight between the rents of the heavy clouds that scudded across the sky.",
                "The Professor unlocked the door, and seeing a natural hesitation amongst us for various reasons, solved the difficulty by entering first himself. He then lit a dark lantern and pointed to the coffin. When the lid was removed and the leaden flange forced back, we all looked in and recoiled. The coffin was empty!",
                "\"Professor, I answered for you. Your word is all I want,\" said Quincey Morris. \"Is this your doing?\" \"I swear to you by all that I hold sacred that I have not removed nor touched her,\" said Van Helsing.",
                "First he took from his bag a mass of what looked like thin, wafer-like biscuit, carefully rolled up in a white napkin; next a double-handful of some whitish stuff, like dough or putty. He crumbled the wafer up fine and worked it into the mass between his hands, and rolling it into thin strips, began to lay them into the crevices between the door and its setting in the tomb. \"I am closing the tomb, so that the Un-Dead may not enter.\" \"What is that which you are using?\" asked Arthur. Van Helsing reverently lifted his hat as he answered: \"The Host. I brought it from Amsterdam. I have an Indulgence.\"",
            ],
        },
        {
            "num": "No. II.",
            "title": "HER WORDS.",
            "subtitle": "Heard in the churchyard, by moonlight.",
            "style": "broadside",
            "paras": [
                "\"Come to me, Arthur.\"",
                "\"Leave these others and come to me.\"",
                "\"My arms are hungry for you.\"",
                "\"Come, and we can rest together.\"",
                "\"Come, my husband, come!\"",
            ],
        },
        {
            "num": "No. III.",
            "title": "THE DEED.",
            "subtitle": "30th September, afternoon; within the Westenra tomb.",
            "style": "prose",
            "paras": [
                "A little before twelve o'clock we three -- Arthur, Quincey Morris, and myself -- called for the Professor. By common consent we had all put on black clothes. We got to the churchyard by half-past one, and strolled about, keeping out of official observation, so that when the sexton, under the belief that every one had gone, had locked the gate, we had the place all to ourselves.",
                "Van Helsing, instead of his little black bag, had with him a long leather one, something like a cricketing bag; it was manifestly of fair weight. He lit the lantern, and stuck two wax candles, by melting their own ends, on other coffins, so that they might give light sufficient to work by.",
                "When he again lifted the lid off Lucy's coffin we all looked -- Arthur trembling like an aspen -- and saw that the body lay there in all its death-beauty. But there was no love in my own heart, nothing but loathing for the foul Thing which had taken Lucy's shape without her soul.",
                "Then Van Helsing spoke out of the lore of the ancients: that when the Un-Dead be made to rest as true dead, then the soul of the poor lady whom we love shall again be free; and that it will be a blessed hand for her that shall strike the blow that sets her free. \"Will it be no joy to think of hereafter: 'It was my hand that sent her to the stars; it was the hand of him that loved her best?'\"",
                "Arthur took the stake and the hammer, and when once his mind was set on action his hands never trembled nor even quivered. He looked like a figure of Thor as his untrembling arm rose and fell, driving deeper and deeper the mercy-bearing stake.",
                "And then the writhing and quivering of the body became less. Finally it lay still. The terrible task was over.",
                "When we looked again, a murmur of startled surprise ran from one to the other of us. There, in the coffin, lay no longer the foul Thing that we had so dreaded, but Lucy as we had seen her in her life, with her face of unequalled sweetness and purity.",
                "Then we cut off the head and filled the mouth with garlic. We soldered up the leaden coffin, screwed on the coffin-lid, and came away. When the Professor locked the door he gave the key to Arthur.",
            ],
        },
        {
            "num": "No. IV.",
            "title": "THE PROFESSOR'S BAG.",
            "subtitle": "An account of its contents, as unpacked in the tomb.",
            "style": "bill",
            "bill_title": "CONTENTS OF THE PROFESSOR'S BAG.",
            "bill_sub": "As unpacked in the Westenra tomb -- 30th September, 1893.",
            "items": [
                ("A dark lantern", "--"),
                ("Two wax candles", "--"),
                ("A soldering iron, with plumbing solder", "--"),
                ("A small oil-lamp, burning with a blue flame", "--"),
                ("Operating knives, laid ready to hand", "--"),
                ("A round wooden stake, charred and sharpened to a fine point", "--"),
                ("A heavy hammer, such as is used in the coal-cellar", "--"),
                ("Garlic flowers, a quantity", "--"),
                ("A little golden crucifix", "not for sale"),
                ("A missal, for the prayer for the dead", "not for sale"),
            ],
            "total": "TOTAL ............ the price is paid in courage.",
            "note": "(The bag itself was a long leather one, something like a cricketing bag, and manifestly of fair weight.)",
        },
        {
            "num": "No. V.",
            "title": "FORGIVEN.",
            "subtitle": "From Lord Godalming to Dr. Seward.",
            "style": "letter",
            "opening": [
                "My dear John, --",
            ],
            "paras": [
                "Forgiven! God bless you that you have given my dear one her soul again, and me peace.",
                "I kissed her dead lips, as she would have had me do, if it had been for her to choose. For she is not a grinning devil now -- not any more a foul Thing for all eternity. No longer is she the devil's Un-Dead. She is God's true dead, whose soul is with Him.",
                "I cannot write more. You know what my heart was, and what it is now.",
            ],
            "signoff": "-- Yours, in grief and in gratitude,",
            "signature": "ARTHUR.",
        },
        {
            "num": "No. VI.",
            "title": "AMSTERDAM.",
            "subtitle": "The Professor departs; the greater task is named.",
            "style": "telegram",
            "tfrom": "Professor Van Helsing, Berkeley Hotel",
            "tto": "Dr. J. Seward",
            "tdated": "30th September, 1893",
            "body": "LEAVE FOR AMSTERDAM TO NIGHT STOP RETURN TO MORROW NIGHT STOP THEN BEGINS OUR GREAT QUEST STOP TWO NIGHTS HENCE DINE WITH ME AT SEVEN OF THE CLOCK STOP BRING FRIENDS STOP KEEP FAITH STOP VAN HELSING",
        },
    ],
    "plates": [
        {
            "after_doc": 1,
            "file": "plates/sealing.jpg",
            "numeral": "Plate I.",
            "title": "THE SEALING.",
            "caption": "The Host, worked into putty, laid in the crevices of the tomb door.",
            "prompt": "19th century oil painting, vertical portrait composition: an elderly professor in a long coat kneeling at night pressing thin strips of pale putty into the crevices of a stone tomb door in a moonlit Victorian cemetery, a dark lantern glowing beside him, three men watching from the shadows among yew trees. Solemn, atmospheric Victorian book-illustration style. No text, no watermark.",
        },
        {
            "after_doc": 3,
            "file": "plates/deed.jpg",
            "numeral": "Plate II.",
            "title": "THE MERCY-BEARING STAKE.",
            "caption": "He looked like a figure of Thor as his untrembling arm rose and fell.",
            "prompt": "19th century oil painting, vertical portrait composition: inside a candlelit Victorian tomb, a young nobleman dressed in black raising a wooden stake and heavy hammer above an open coffin while three grave men stand praying around him and an elderly professor reads from a book. Solemn and restrained, no gore, atmospheric Victorian book-illustration style. No text, no watermark.",
        },
        {
            "after_doc": 5,
            "file": "plates/peace.jpg",
            "numeral": "Plate III.",
            "title": "PEACE AT LAST.",
            "caption": "Outside the air was sweet, the sun shone, and the birds sang.",
            "prompt": "19th century oil painting, vertical portrait composition: a peaceful Victorian cemetery at dawn, morning sunlight streaming over a stone tomb whose door stands open, white lilies and roses laid at its threshold, birds singing in a soft golden sky above yew trees. Serene, hopeful, reverent mood. Atmospheric Victorian book-illustration style. No text, no watermark.",
        },
    ],
}
