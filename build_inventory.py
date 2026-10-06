#!/usr/bin/env python3
"""Extract a full inventory of every content item in the Dracula companion,
in document order, from each chapter's build script."""
import importlib.util
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def load_chapter(num):
    nn = f"{num:02d}"
    path = os.path.join(BASE, f"ch{nn}", "content.py")
    spec = importlib.util.spec_from_file_location(f"ch{nn}_content", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTER


def plate_kind(pl):
    f = pl.get("file", "").lower()
    prompt = pl.get("prompt", "").lower()
    if "map" in f or prompt.startswith("antique hand-drawn map"):
        return "map"
    return "plate"


def chapter_from_content(num):
    nn = f"{num:02d}"
    ch = load_chapter(num)
    items = [
        {"kind": "cover", "numeral": "Chapter cover",
         "title": f"{ch['label']} -- {ch['title']}", "image": "cover.jpg"}
    ]
    docs = ch.get("docs", [])
    plates = ch.get("plates", [])
    placed = [False] * len(plates)
    for i, doc in enumerate(docs):
        items.append({"kind": "doc", "numeral": doc["num"],
                      "title": doc["title"], "image": None})
        for j, pl in enumerate(plates):
            if pl.get("after_doc") == i:
                items.append({"kind": plate_kind(pl),
                              "numeral": pl.get("numeral", "Plate."),
                              "title": pl["title"],
                              "image": os.path.basename(pl["file"])})
                placed[j] = True
    for j, pl in enumerate(plates):  # any plates past the last doc
        if not placed[j]:
            items.append({"kind": plate_kind(pl),
                          "numeral": pl.get("numeral", "Plate."),
                          "title": pl["title"],
                          "image": os.path.basename(pl["file"])})
    return {"ch": f"ch{nn}", "label": ch.get("label"),
            "title": ch.get("title"), "subtitle": ch.get("subtitle"),
            "items": items}


def chapter_01():
    # Bespoke script; order verified by reading make_ephemera.py directly.
    items = [
        {"kind": "cover", "numeral": "Cloth cover",
         "title": "SIDE-PAPERS & EPHEMERA pertaining to Chapter the First of \"DRACULA\"",
         "image": None},
        {"kind": "cover", "numeral": "Chapter cover",
         "title": "CHAPTER ONE -- JONATHAN HARKER'S JOURNAL", "image": "cover.jpg"},
        {"kind": "frontispiece", "numeral": "Frontispiece.",
         "title": "THE TRAVELLER'S PAPERS, AS THEY SURVIVE.", "image": "frontispiece.jpg"},
        {"kind": "map", "numeral": "Plate I.",
         "title": "MR. HARKER'S JOURNEY, APRIL -- MAY 1893.", "image": "journey.jpg"},
        {"kind": "watercolour", "numeral": "Watercolour I.",
         "title": "MUNICH -- 1ST MAY, 8:35 P.M.", "image": "wc_munich.png"},
        {"kind": "watercolour", "numeral": "Watercolour II.",
         "title": "VIENNA -- 2ND MAY, DAWN.", "image": "wc_vienna.png"},
        {"kind": "watercolour", "numeral": "Watercolour III.",
         "title": "BUDA-PESTH -- THE DANUBE.", "image": "wc_budapest.png"},
        {"kind": "watercolour", "numeral": "Watercolour IV.",
         "title": "KLAUSENBURG -- THE MOUNTAIN HALT.", "image": "wc_klausenburg.png"},
        {"kind": "watercolour", "numeral": "Watercolour V.",
         "title": "BISTRITZ -- 3RD MAY.", "image": "wc_bistritz.png"},
        {"kind": "watercolour", "numeral": "Watercolour VI.",
         "title": "THE BORGO PASS -- 4TH MAY, DUSK.", "image": "wc_borgo.png"},
        {"kind": "map", "numeral": "Plate II.",
         "title": "THE ROAD FROM BISTRITZ TO THE BORGO PASS.", "image": "map.jpg"},
        {"kind": "doc", "numeral": "No. II.", "title": "THE GOLDEN CROWN HOTEL", "image": None},
        {"kind": "plate", "numeral": "Plate III.",
         "title": "THE GOLDEN CROWN, BISTRITZ.", "image": "inn.jpg"},
        {"kind": "doc", "numeral": "No. III.",
         "title": "BISTRITZ AND THE BORGO PASS.", "image": None},
        {"kind": "plate", "numeral": "Plate IV.",
         "title": "BISTRITZ, MARKET MORNING.", "image": "bistritz.jpg"},
        {"kind": "doc", "numeral": "No. IV.",
         "title": "ST. GEORGE'S EVE IN TRANSYLVANIA.", "image": None},
        {"kind": "doc", "numeral": "No. V.", "title": "THE BLUE FLAMES.", "image": None},
        {"kind": "plate", "numeral": "Plate V.",
         "title": "THE BLUE FLAMES.", "image": "blue_flames.jpg"},
        {"kind": "doc", "numeral": "No. VI.",
         "title": "IMPERIAL-ROYAL PRIVILEGED POST-DILIGENCE.", "image": None},
        {"kind": "plate", "numeral": "Plate VI.",
         "title": "THE DILIGENCE ON THE BORGO ROAD.", "image": "diligence.jpg"},
        {"kind": "doc", "numeral": "No. VII.", "title": "COPY OF A LETTER.", "image": None},
        {"kind": "plate", "numeral": "Plate VII.",
         "title": "THE CASTLE, BY MOONLIGHT.", "image": "castle.jpg"},
        {"kind": "doc", "numeral": "No. VIII.",
         "title": "OF THE PEOPLES OF THE CARPATHIANS.", "image": None},
        {"kind": "doc", "numeral": "No. IX.",
         "title": "THE GOLDEN CROWN, BISTRITZ.", "image": None},
    ]
    return {"ch": "ch01", "label": "CHAPTER ONE",
            "title": "JONATHAN HARKER'S JOURNAL",
            "subtitle": "3rd -- 5th May -- Bistritz to the Borgo Pass",
            "items": items}


def main():
    chapters = [chapter_01()]
    for n in range(2, 29):
        chapters.append(chapter_from_content(n))
    out = os.path.join(BASE, "inventory.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"chapters": chapters}, f, ensure_ascii=True, indent=1)
    print("wrote", out)
    # totals
    totals = {}
    for ch in chapters:
        for it in ch["items"]:
            totals[it["kind"]] = totals.get(it["kind"], 0) + 1
    print("chapters:", len(chapters))
    for k in sorted(totals):
        print(f"  {k}: {totals[k]}")
    print("total items:", sum(totals.values()))
    # sanity: list map-kind plates
    print("maps:")
    for ch in chapters:
        for it in ch["items"]:
            if it["kind"] == "map":
                print(f"  {ch['ch']} {it['numeral']} {it['title']} [{it['image']}]")


if __name__ == "__main__":
    main()
