# -*- coding: latin-1 -*-
"""Chapter 15 content for the Dracula companion.

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
    "number": 15,
    "label": "CHAPTER FIFTEEN",
    "title": "DR. SEWARD'S DIARY",
    "subtitle": "27th -- 29th September -- the bloofer lady",
    "epigraph": '"I drew near and looked. The coffin was empty."',
    "docs": [
        {
            "num": "No. I.",
            "title": "A SUMMONS.",
            "subtitle": "From Professor Van Helsing to Dr. Seward; 27th September.",
            "style": "letter",
            "opening": [
                "Friend John, --",
            ],
            "paras": [
                "To-night I go to prove it. Dare you come with me? The logic is simple, no madman's logic this time: if it be not true, then proof will be relief; at worst it will not harm.",
                "First, we go off now and see that child in the hospital. Dr. Vincent, of the North Hospital, where the papers say the child is, is a friend of mine, and I think of yours since you were in class at Amsterdam. He will let two scientists see his case, if he will not let two friends. We shall tell him nothing, but only that we wish to learn. And then --",
                "And then we spend the night, you and I, in the churchyard where Lucy lies. This is the key that locks the tomb. I had it from the coffin-man to give to Arthur.",
                "Hasten, then. The afternoon is passing, and the sun will not wait for our courage.",
            ],
            "signoff": "-- Your friend,",
            "signature": "ABRAHAM VAN HELSING.",
        },
        {
            "num": "No. II.",
            "title": "AT THE NORTH HOSPITAL.",
            "subtitle": "Memorandum of the visit; the child with the wounded throat.",
            "style": "prose",
            "paras": [
                "We found the child awake. It had had a sleep and taken some food, and altogether was going on well. Dr. Vincent took the bandage from its throat, and showed us the punctures. There was no mistaking the similarity to those which had been on Lucy's throat. They were smaller, and the edges looked fresher; that was all.",
                "We asked Vincent to what he attributed them, and he replied that it must have been a bite of some animal, perhaps a rat; but, for his own part, he was inclined to think that it was one of the bats which are so numerous on the northern heights of London. \"Out of so many harmless ones,\" he said, \"there may be some wild specimen from the South of a more malignant species.\"",
                "Only ten days ago, he told us, a wolf got out of the Zoological Gardens, and was traced up in this direction. For a week after, the children were playing nothing but Red Riding Hood on the Heath and in every alley in the place -- until this \"bloofer lady\" scare came along, since when it has been quite a gala-time with them.",
                "Even this poor little mite, when he woke up to-day, asked the nurse if he might go away. When she asked him why he wanted to go, he said he wanted to play with the \"bloofer lady.\"",
            ],
        },
        {
            "num": "No. III.",
            "title": "CAUTION TO PARENTS.",
            "subtitle": "Posted about Hampstead Heath, by order of the hospital authorities.",
            "style": "notice",
            "lead": "PARENTS ARE ENTREATED TO KEEP STRICT WATCH OVER THEIR CHILDREN.",
            "paras": [
                "Children of the Heath and its neighbourhood are forbidden to stray after dark, or to follow any stranger who may call to them.",
                "These fancies to stray are most dangerous; and if a child were to remain out another night, it would probably be fatal.",
                "No child will be sent home from the hospital for a week at least -- longer if the wound is not healed.",
            ],
        },
        {
            "num": "No. IV.",
            "title": "JACK STRAW'S CASTLE.",
            "subtitle": "Supper on the Heath, before the night's work.",
            "style": "bill",
            "bill_title": "JACK STRAW'S CASTLE, HAMPSTEAD HEATH.",
            "bill_sub": "Supper for two gentlemen -- 27th September, 1893.",
            "items": [
                ("Supper for two, in the company of a little crowd of bicyclists", "--"),
                ("Ale, in liberal measure", "--"),
                ("Bread and cheese, to follow", "--"),
                ("Genial noise, provided gratis", "nothing"),
            ],
            "total": "TOTAL ............ settled in full.",
            "note": "(The Professor was in good spirits, and ate heartily. At ten o'clock we started from the inn for the churchyard.)",
        },
        {
            "num": "No. V.",
            "title": "THE EMPTY COFFIN.",
            "subtitle": "The night visit to the Westenra tomb; 27th September.",
            "style": "prose",
            "paras": [
                "About ten o'clock we started from the inn. It was then very dark, and the scattered lamps made the darkness greater when we were once outside their individual radius. At last we reached the wall of the churchyard, which we climbed over, and with some little difficulty -- for it was very dark -- we found the Westenra tomb.",
                "The Professor took the key, opened the creaky door, and standing back, politely, but quite unconsciously, motioned me to precede him. There was a delicious irony in the offer, in the courtliness of giving preference on such a ghastly occasion.",
                "He took out a turnscrew, and straightway began taking out the screws, and finally lifted off the lid, showing the casing of lead beneath. Then with a tiny fret-saw he cut down a couple of feet along one side of the lead coffin, and across, and down the other; and bending back the loose flange, he held up the candle into the aperture, and motioned to me to look.",
                "I drew near and looked. The coffin was empty.",
                "We watched then, he at one side of the churchyard and I behind a yew-tree at the other. Just after the distant clock struck twelve, and in time one and two, I thought I saw something like a white streak moving between two dark yew-trees; and coming over, found the Professor holding in his arms a tiny child.",
                "We looked at the child's throat by match-light. It was without a scratch or scar of any kind. \"We were just in time,\" said the Professor thankfully.",
                "We decided we would take it to the Heath, and when we heard a policeman coming, would leave it where he could not fail to find it. All fell out well. By good chance we got a cab near the \"Spaniards,\" and drove to town.",
            ],
        },
        {
            "num": "No. VI.",
            "title": "NOTE LEFT BY VAN HELSING IN HIS PORTMANTEAU.",
            "subtitle": "Berkeley Hotel; directed to John Seward, M.D. (Not delivered.) 27th September.",
            "style": "letter",
            "opening": [
                "Friend John, --",
            ],
            "paras": [
                "I write this in case anything should happen. I go alone to watch in that churchyard. It pleases me that the Un-Dead, Miss Lucy, shall not leave to-night, that so on the morrow night she may be more eager. Therefore I shall fix some things she like not -- garlic and a crucifix -- and so seal up the door of the tomb. She is young as Un-Dead, and will heed. Moreover, these are only to prevent her coming out; they may not prevail on her wanting to get in; for then the Un-Dead is desperate, and must find the line of least resistance, whatsoever it may be. I shall be at hand all the night from sunset till after the sunrise, and if there be aught that may be learned I shall learn it. For Miss Lucy or from her, I have no fear; but that other to whom is there that she is Un-Dead, he have now the power to seek her tomb and find shelter. He is cunning, as I know from Mr. Jonathan and from the way that all along he have fooled us when he played with us for Miss Lucy's life, and we lost; and in many ways the Un-Dead are strong. He have always the strength in his hand of twenty men; even we four who gave our strength to Miss Lucy it also is all to him. Besides, he can summon his wolf and I know not what. So if it be that he come thither on this night he shall find me; but none other shall -- until it be too late. But it may be that he will not attempt the place. There is no reason why he should; his hunting ground is more full of game than the churchyard where the Un-Dead woman sleep, and the one old man watch.",
                "Therefore I write this in case.... Take the papers that are with this, the diaries of Harker and the rest, and read them, and then find this great Un-Dead, and cut off his head and burn his heart or drive a stake through it, so that the world may rest from him.",
                "If it be so, farewell.",
            ],
            "signoff": "",
            "signature": "VAN HELSING.",
        },
        {
            "num": "No. VII.",
            "title": "A SUMMONS TO THE BERKELEY.",
            "subtitle": "The Professor sends for Arthur and Mr. Morris.",
            "style": "telegram",
            "tfrom": "Professor Van Helsing, Berkeley Hotel, Piccadilly",
            "tto": "Lord Godalming",
            "tdated": "29th September, 1893",
            "body": "MUST SEE YOU THIS MORNING ON MATTER OF GRAVEST IMPORT CONCERNING MISS LUCY STOP COME IN SECRET AND BRING THAT FINE YOUNG MAN OF AMERICA THAT GAVE HIS BLOOD STOP PROMISE ME NOTHING TILL YOU HAVE SEEN STOP VAN HELSING",
        },
    ],
    "plates": [
        {
            "after_doc": 1,
            "file": "plates/hospital.jpg",
            "numeral": "Plate I.",
            "title": "THE CHILD AT THE NORTH HOSPITAL.",
            "caption": "Dr. Vincent shows the punctures on the child's throat; Van Helsing and Seward look on.",
            "prompt": "19th century oil painting, vertical portrait composition: a lamplit Victorian hospital ward at night, a doctor gently unwinding a bandage from a small sleeping child's throat while two grave gentlemen in dark coats watch intently from the doorway. Somber, atmospheric Victorian book-illustration style. No text, no watermark.",
        },
        {
            "after_doc": 3,
            "file": "plates/churchyard.jpg",
            "numeral": "Plate II.",
            "title": "THE WHITE STREAK.",
            "caption": "Something like a white streak, moving between two dark yew-trees.",
            "prompt": "19th century oil painting, vertical portrait composition: a moonlit Victorian churchyard at midnight, a pale spectral white figure flitting between dark yew trees toward a stone tomb, two men watching from behind gravestones in the foreground. Eerie, atmospheric Victorian book-illustration style. No text, no watermark.",
        },
        {
            "after_doc": 5,
            "file": "plates/watch.jpg",
            "numeral": "Plate III.",
            "title": "THE SOLITARY WATCH.",
            "caption": "\"He shall find me; but none other shall -- until it be too late.\"",
            "prompt": "19th century oil painting, vertical portrait composition: an elderly bearded professor in a long coat keeping a solitary night watch inside a Victorian cemetery vault, a single candle burning beside him, strings of garlic flowers laid across a stone tomb door, moonlight through a barred window. Solemn, atmospheric Victorian book-illustration style. No text, no watermark.",
        },
    ],
}
