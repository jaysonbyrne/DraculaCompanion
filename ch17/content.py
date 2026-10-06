# -*- coding: latin-1 -*-
"""Chapter 17 content for the Dracula companion.

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
    "number": 17,
    "label": "CHAPTER SEVENTEEN",
    "title": "DR. SEWARD'S DIARY",
    "subtitle": "29th -- 30th September -- the papers in order",
    "epigraph": '"In this matter dates are everything."',
    "docs": [
        {
            "num": "No. I.",
            "title": "FROM MRS. HARKER.",
            "subtitle": "The telegram that sets all in motion.",
            "style": "telegram",
            "tfrom": "Mina Harker",
            "tto": "Professor Van Helsing, Berkeley Hotel",
            "tdated": "29th September, 1893",
            "body": "AM COMING UP BY TRAIN STOP JONATHAN AT WHITBY STOP IMPORTANT NEWS STOP MINA HARKER",
        },
        {
            "num": "No. II.",
            "title": "TO THE HOUSEKEEPER.",
            "subtitle": "Despatched from Paddington Station.",
            "style": "telegram",
            "tfrom": "Dr. J. Seward, Paddington Station",
            "tto": "The Housekeeper",
            "tdated": "29th September, 1893",
            "body": "HAVE SITTING ROOM AND BEDROOM PREPARED AT ONCE STOP EXPECTING MRS HARKER THIS EVENING STOP SHE BRINGS HER TYPEWRITER STOP SEWARD",
        },
        {
            "num": "No. III.",
            "title": "THE PHONOGRAPH DIARY.",
            "subtitle": "Mina Harker copies the wax cylinders; 29th September.",
            "style": "prose",
            "paras": [
                "On the table opposite him was what I knew at once from the description to be a phonograph. I had never seen one, and was much interested. \"Why, this beats even shorthand! May I hear it say something?\"",
                "\"Then, Dr. Seward, you had better let me copy it out for you on my typewriter.\" He grew to a positively deathly pallor as he said: \"No! no! no! For all the world, I wouldn't let you know that terrible story!\"",
                "He stood up and opened a large drawer, in which were arranged in order a number of hollow cylinders of metal covered with dark wax. \"Take the cylinders and hear them -- the first half-dozen of them are personal to me, and they will not horrify you; then you will know me better.\"",
                "When the terrible story of Lucy's death, and -- and all that followed, was done, I lay back in my chair powerless. My brain was all in a whirl, and only that there came through all the multitude of horrors the holy ray of light that my dear, dear Lucy was at last at peace, I do not think I could have borne it.",
                "I took the cover off my typewriter, and said to Dr. Seward: \"Let me write this all out now. We must be ready for Dr. Van Helsing when he comes.\" I used manifold, and so took three copies of the diary, just as I had done with all the rest.",
            ],
        },
        {
            "num": "No. IV.",
            "title": "THE FIFTY BOXES.",
            "subtitle": "The journey of the Count's earth, traced by Mr. Harker.",
            "style": "timetable",
            "note": "\"Fifty cases of common earth, to be used for experimental purposes.\" -- the invoice seen at Billington's, Whitby. Their tally was exact with the list, and the boxes were \"main and mortal heavy.\"",
            "rows": [
                ("Varna, Roumania", "ship", "the Demeter"),
                ("Whitby", "rail", "to King's Cross"),
                ("King's Cross", "Carter Paterson", "to Carfax"),
                ("Carfax, Purfleet", "chapel", "all fifty"),
            ],
            "paras": [
                "Of one thing I am now satisfied: that all the boxes which arrived at Whitby from Varna in the Demeter were safely deposited in the old chapel at Carfax. There should be fifty of them there, unless any have since been removed -- as from Dr. Seward's diary I fear.",
                "\"That 'ere 'ouse, guv'nor, is the rummiest I ever was in,\" said one of Carter Paterson's men. \"Blyme! but it ain't been touched sence a hundred years. But the ole chapel -- that took the cike, that did!\"",
                "I shall try to see the carter who took away the boxes from Carfax when Renfield attacked them. By following up this clue we may learn a good deal.",
            ],
        },
        {
            "num": "No. V.",
            "title": "NOTICE TO THE ATTENDANTS.",
            "subtitle": "By order of Dr. Seward; respecting the patient Renfield.",
            "style": "notice",
            "lead": "THE ATTENDANT ON DUTY WILL LOOK CLOSELY AFTER THE PATIENT RENFIELD.",
            "paras": [
                "He is at present placid, and smiles benignly; he speaks quite confidently of going home, and of getting his discharge at once.",
                "I mistrust these quiet moods of his. All those outbreaks were in some way linked with the proximity of the Count.",
                "Have a strait-waistcoat ready in case of need. He is just a little too sane at present to make it safe to probe him too deep with questions.",
            ],
        },
        {
            "num": "No. VI.",
            "title": "THE BROTHERHOOD.",
            "subtitle": "Lord Godalming and Mr. Morris come to the asylum; 30th September.",
            "style": "prose",
            "paras": [
                "Lord Godalming and Mr. Morris arrived earlier than we expected. It was to me a painful meeting, for it brought back all poor dear Lucy's hopes of only a few months ago. I told them, as well as I could, that I had read all the papers and diaries, and that my husband and I, having typewritten them, had just finished putting them in order. I gave them each a copy to read in the library.",
                "\"Did you write all this, Mrs. Harker?\" said Lord Godalming, turning over the pile. I nodded, and he went on: \"I don't quite see the drift of it; but you people are all so good and kind, and have been working so earnestly and so energetically, that all I can do is to accept your ideas blindfold and try to help you.\"",
                "When he found himself alone with me he sat down on the sofa and gave way utterly and openly. I said to him: \"I loved dear Lucy, and I know what she was to you, and what you were to her. She and I were like sisters; and now she is gone, will you not let me be like a sister to you in your trouble?\"",
                "\"For dear Lucy's sake,\" I said as we clasped hands. \"Ay, and for your own sake,\" he added, \"for if a man's esteem and gratitude are ever worth the winning, you have won mine to-day.\"",
                "\"Little girl!\" -- the very words he had used to Lucy, said Mr. Morris, stooping to kiss my hand; and impulsively I bent over and kissed him -- and oh, but he proved himself a friend!",
            ],
        },
        {
            "num": "No. VII.",
            "title": "ALL IN ORDER.",
            "subtitle": "From Mrs. Harker to Professor Van Helsing; 30th September.",
            "style": "letter",
            "opening": [
                "Dear Professor Van Helsing, --",
            ],
            "paras": [
                "Jonathan is home from Whitby, full of life and hope and determination, and we have got everything in order for to-night. I feel myself quite wild with excitement.",
                "We have knitted together in chronological order every scrap of evidence we have, and I have taken three copies of all, in manifold, upon my typewriter. In this matter dates are everything, and every item is now put in its place.",
                "Lord Godalming and Mr. Morris have each a copy, and are reading in the library. We need have no secrets amongst us; working together and with absolute trust, we can surely be stronger than if some of us were in the dark.",
                "Come when you will. We are ready.",
            ],
            "signoff": "-- Your affectionate pupil,",
            "signature": "MINA HARKER.",
        },
    ],
    "plates": [
        {
            "after_doc": 1,
            "file": "plates/paddington.jpg",
            "numeral": "Plate I.",
            "title": "THE MEETING AT PADDINGTON.",
            "caption": "\"Dr. Seward, is it not?\" -- \"And you are Mrs. Harker!\"",
            "prompt": "19th century oil painting, vertical portrait composition: a busy Victorian railway station arrival platform with steam, a dainty young woman carrying a typewriter case stepping forward to greet a bearded doctor in a dark frock coat, porters and luggage around them. Warm, atmospheric Victorian book-illustration style. No text, no watermark.",
        },
        {
            "after_doc": 3,
            "file": "plates/boxes.jpg",
            "numeral": "Plate II.",
            "title": "THE VOYAGE OF THE BOXES.",
            "caption": "From Varna to Whitby in the Demeter; from King's Cross to Carfax by Carter Paterson.",
            "prompt": "Antique hand-drawn map, 1890s cartographic style, sepia ink on aged parchment: a sailing ship's course across a chart from Varna on the Black Sea to Whitby on the English coast, then dotted railway lines south to London with a mark at Carfax near Purfleet, small sketches of wooden crates in the corners. Text labels are fine, no watermark.",
        },
        {
            "after_doc": 5,
            "file": "plates/typewriter.jpg",
            "numeral": "Plate III.",
            "title": "THE CHRONICLE IN MANIFOLD.",
            "caption": "Three copies of all, typed in manifold, and every item put in chronological order.",
            "prompt": "19th century oil painting, vertical portrait composition: a young Victorian woman typing at an early typewriter in a lamplit study at night, tall stacks of typed manuscript pages beside her, a phonograph with dark wax cylinders on the desk. Diligent and atmospheric, Victorian book-illustration style. No text, no watermark.",
        },
    ],
}
