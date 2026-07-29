#!/usr/bin/env python3
"""Split Kirfel's Purāṇa Pañcalakṣaṇa into one clean text file per Textgruppe.

Input is pages.json (from postprocess.py): per PDF page, the constituted text
(`body`) with the critical apparatus already peeled off into `apparatus`.

What this adds:
  * segmentation — walk the edition in book-page order and track the current
    Abschnitt / Kapitel / Textgruppe / letter subdivision from the in-page
    section headings. Kirfel nests these two different ways: in Abschnitt 1 the
    Textgruppe is the outer level and Kapitel run inside it; in Abschnitt 2/4 the
    Kapitel is outer and each one is split into Textgruppen. The nesting is
    derived per Abschnitt from the order the two headings appear in.
  * apparatus residue — Chandra labels most apparatus blocks Footnote, but
    continuation entries that do not start with a "15 =" key get left in the
    body. Those are stripped line by line here.
  * parallel columns — where Kirfel prints sub-recensions side by side, cell i
    of each row goes to that group's column stream i. Single-column stretches
    (and full-width rows inside a parallel passage) go to column 1, so col1 is a
    continuous text and col2+ hold only the divergent passages.
  * cleanup — variant-marker superscripts, italics and emendation asterisks are
    dropped; verse numbers (|| 15 ||) and daṇḍas are kept.

Usage: segment_textgruppen.py [outdir]      (default: ./textgruppen)
"""
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

HERE = Path("/mnt2/kengo/ocr-kirfel")
PAGES = HERE / "pages.json"
FIRST_BOOK_PAGE, LAST_BOOK_PAGE = 1, 556      # Maṅgalam .. end of 4. Abschnitt

# ------------------------------------------------------------------ headings
RE_ABSCHNITT = re.compile(r"^(\d+)\.\s*Abschnitt")
RE_KAPITEL = re.compile(r"^(\d+)\.?\s*Kapitel")
RE_GRUPPE = re.compile(r"^Textgruppe\s+([IVX]+\s*[aAB]?)\b", re.I)
RE_LETTER = re.compile(r"^([A-E])\.?\s*$")
RE_ADHY = re.compile(r"^Adhy\.\s*(\d+)")
# all division markers, so a heading block holding two of them is fully applied
RE_ANY_DIVISION = re.compile(
    r"(?P<abschnitt>\d+)\.\s*Abschnitt"
    r"|(?P<kapitel>\d+)\.?\s*Kapitel"
    r"|Textgruppe\s+(?P<gruppe>[IVX]+\s*[aAB]?)\b"
    r"|Adhy\.\s*(?P<adhy>\d+)", re.I)
ABSCHNITT_NAME = {1: "Sarga und Pratisarga", 2: "Vaṃśa",
                  3: "Manvantara", 4: "Vaṃśānucarita"}


def fold(s: str) -> str:
    """Lowercase, strip diacritics and punctuation — the running heads and
    section titles are OCR'd inconsistently (Vamśa / Vaṃśa / Vāṃśanucarita)."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", s.lower())


ABSCHNITT_NAME_FOLDED = {fold(v) for v in ABSCHNITT_NAME.values()}


def norm_group(raw: str) -> str:
    """'II A' / 'IIa' / 'I a' -> canonical 'IIA' / 'Ia'."""
    g = re.sub(r"\s+", "", raw)
    m = re.fullmatch(r"([IVX]+)([aAB]?)", g)
    if not m:
        return g
    roman, suf = m.group(1).upper(), m.group(2)
    if not suf:
        return roman
    # 'Ia' is a group of its own; 'IIA'/'IIB' are subgroups of II
    return roman + ("a" if (roman == "I" and suf in "aA") else suf.upper())


# -------------------------------------------------------------- text cleanup
SIGLA = (r"Bd|Vā|Va|Br|Bh|Bhv|H|A|M|Mt|Mā|P\.\d|P|Vi|Śidh|Sidh|Kū|Ku|"
         r"Li|Ag|Kū|T|V|Śidh")
RE_APP_KEY = re.compile(r"^\s*\d{1,4}(?:[ab])?\s*=")
RE_REF = re.compile(rf"\b(?:{SIGLA})\.\s*[IVX0-9]")
RE_VARIANT = re.compile(r"\d\)")


def is_apparatus_line(line: str) -> bool:
    """Apparatus prose vs. constituted verse. Verse lines end in a daṇḍa or a
    || n || number and never carry variant-number markers once superscripts
    have been stripped, so the two are well separated."""
    t = line.strip()
    if not t:
        return False
    if RE_APP_KEY.match(t):
        return True
    if re.match(r"^\d+\.\s*\d+\s*=", t):          # "59.10 = I."
        return True
    # the apparatus cites verses as "15 =", never as "|| 15 ||": a closing
    # verse number is decisive evidence of constituted text
    if re.search(r"\|\|\s*\d+\s*\|\|", t):
        return False
    if "Cfr." in t or "cfr." in t:
        return True
    # a bare "2)" is a variant marker: after <sup> stripping the constituted
    # text carries none, so any that survive belong to an apparatus entry
    if RE_VARIANT.search(t):
        return True
    if len(RE_REF.findall(t)) >= 2:
        return True
    # variant readings are printed as truncations: "Vā. -napriyam"
    if re.search(rf"\b(?:{SIGLA})\.\s*-", t):
        return True
    # a single reference plus no verse punctuation is still apparatus
    if RE_REF.search(t) and "||" not in t and not t.endswith("|"):
        return True
    return False


# --------------------------------------------- transliteration normalization
# Kirfel prints ISO 15919; corpus/epic_puranas is pure IAST (ṁ occurs once in
# 5.15M tokens there, against 1,740 in the Kirfel text). Map the scheme over,
# and fold the handful of OCR misreads onto their base letters.
ISO_TO_IAST = {
    "ṁ": "ṃ",                       # anusvāra: dot above -> dot below
    "ē": "e", "ō": "o",             # ISO long e/o: Sanskrit e/o are always long
    "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u",   # sandhi contraction
    "ṙ": "ṛ", "ş": "ś", "í": "i", "ṽ": "v", "ũ": "u",   # OCR misreads
    "ľ": "l", "ç": "c", "ḡ": "g", "ḱ": "k", "ḃ": "b", "ó": "o",
}
RING = "̥"                      # combining ring below (ISO vocalic r / l)
VOWEL_INITIAL = set("aāiīuūṛṝḷḹeo'’")


def to_iast(text: str) -> str:
    text = text.replace("r" + RING, "ṛ").replace("l" + RING, "ḷ")
    text = text.replace(RING, "")    # any stray ring left by the OCR
    return "".join(ISO_TO_IAST.get(c, c) for c in text)


def final_m_to_anusvara(line: str) -> str:
    """Kirfel writes word-final -m throughout; GRETIL writes anusvāra except
    before a vowel, where the m is retained. Apply that rule, treating the end
    of a pāda (line end or daṇḍa) as a pause."""
    toks = line.split()
    for i, tok in enumerate(toks):
        core = tok.rstrip(".,;!?")
        if not core.endswith("m"):
            continue
        nxt = next((t for t in toks[i + 1:] if t[:1].isalpha() or t[:1] in "'’"),
                   None)
        if nxt and nxt[0] in VOWEL_INITIAL:
            continue                 # m before a vowel stays m
        toks[i] = core[:-1] + "ṃ" + tok[len(core):]
    return " ".join(toks)


def strip_markup(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["sup", "sub"]):
        tag.decompose()                       # variant markers 1) 2)
    for tag in soup.find_all(["i", "b"]):
        tag.unwrap()
    for br in soup.find_all("br"):
        br.replace_with("\n")
    return soup.get_text()


def clean_lines(html: str):
    """html block -> list of constituted-text lines, apparatus removed."""
    text = strip_markup(html)
    text = unicodedata.normalize("NFC", text)
    out, hit_app = [], False
    for raw in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", raw).strip()
        if not line:
            continue
        if hit_app or is_apparatus_line(line):
            hit_app = True                    # apparatus sits at the foot
            continue
        line = line.replace("*", "")          # emendation marks
        line = re.sub(r"\s+([.,;])", r"\1", line)
        line = re.sub(r"\s*\|\|\s*(\d+)\s*\|\|", r" || \1 ||", line)
        line = re.sub(r"(?<![|\s])\s*\|(?!\|)", r" |", line)
        line = re.sub(r"[ \t]{2,}", " ", line).strip()
        # Kirfel capitalizes proper names as a German edition would; the rest
        # of the corpus does not, and build_epic_puranas_sandhied.py drops any
        # token with a leading capital. Fold them down. (Must come after the
        # apparatus test above, which keys on capitalized sigla.)
        line = line.lower()
        line = final_m_to_anusvara(to_iast(line))
        if line:
            out.append(line)
    return out


# ------------------------------------------------------------- segmentation
class Segmenter:
    def __init__(self):
        self.abschnitt = None
        self.kapitel = None
        self.group = None
        self.letter = None
        self.adhy = None
        self.group_outer = {}                 # abschnitt -> bool
        self.refs = ""                        # "(Mt. 2.22—4.32.)" under a heading
        self._seen_in_abschnitt = []

    def heading(self, text: str):
        """Apply every division marker in a heading block. Chandra sometimes
        merges two headings printed on consecutive lines into one block
        ('2. Kapitel. / Textgruppe I.'), so scan for all of them, in order."""
        t = re.sub(r"<[^>]+>", "", text).strip()
        t = re.sub(r"\s+", " ", t)
        hits = []
        self.refs = ""
        for m in RE_ANY_DIVISION.finditer(t):
            if m.group("abschnitt"):
                self.abschnitt = int(m.group("abschnitt"))
                self.kapitel = self.group = self.letter = self.adhy = None
                self._seen_in_abschnitt = []
                hits.append("abschnitt")
            elif m.group("kapitel"):
                self.kapitel = int(m.group("kapitel"))
                self.letter = self.adhy = None
                self._seen_in_abschnitt.append("kapitel")
                # Kapitel is the outer level (Abschnitt 2/4): a new one
                # clears the group until the next Textgruppe heading
                if self.group_outer.get(self.abschnitt) is False:
                    self.group = None
                hits.append("kapitel")
            elif m.group("gruppe"):
                self.group = norm_group(m.group("gruppe"))
                self.letter = self.adhy = None
                self._seen_in_abschnitt.append("gruppe")
                if self.abschnitt not in self.group_outer:
                    # whichever of the two comes first in this Abschnitt is outer
                    self.group_outer[self.abschnitt] = (
                        "kapitel" not in self._seen_in_abschnitt[:-1])
                # where the Textgruppe is outer (Abschnitt 1) its chapters
                # restart, so the previous group's number must not carry over
                if self.group_outer.get(self.abschnitt):
                    self.kapitel = None
                hits.append("gruppe")
            elif m.group("adhy"):
                self.adhy = int(m.group("adhy"))
                hits.append("adhy")
        if hits:
            return hits[-1]
        # a bare letter subdivision is always its own heading block
        if m := RE_LETTER.match(t):
            self.letter = m.group(1)
            return "letter"
        # the Abschnitt's name printed on its own line, and the opening
        # benediction: titles, not text (OCR varies on the diacritics)
        if fold(t) in ABSCHNITT_NAME_FOLDED or fold(t) == "mangalam":
            return "title"
        return None

    def label(self):
        bits = []
        if self.abschnitt:
            bits.append(f"{self.abschnitt}. Abschnitt. "
                        f"{ABSCHNITT_NAME.get(self.abschnitt, '')}".strip())
        if self.kapitel:
            bits.append(f"{self.kapitel}. Kapitel")
        if self.letter:
            bits.append(self.letter + ".")
        if self.adhy:
            bits.append(f"Adhy. {self.adhy}")
        label = " | ".join(bits)
        return f"{label}  {self.refs}".strip() if self.refs else label


def main():
    outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "textgruppen"
    outdir.mkdir(exist_ok=True)
    for stale in outdir.glob("kirfel_ppl_*.txt"):
        stale.unlink()          # column count varies between runs; never leave stragglers
    pages = json.load(open(PAGES, encoding="utf-8"))
    edition = sorted(
        (p for p in pages
         if re.fullmatch(r"\d+", p.get("book", ""))
         and FIRST_BOOK_PAGE <= int(p["book"]) <= LAST_BOOK_PAGE),
        key=lambda p: (int(p["book"]), p["pdf"]))

    seg = Segmenter()
    streams = defaultdict(list)               # (group, col) -> [lines]
    last_head = {}                            # (group, col) -> heading written
    spans = []                                # (group, first, last) for report
    stats = defaultdict(int)

    for page in edition:
        bp = int(page["book"])
        for item in page["body"]:
            if item["t"] == "head":
                if seg.heading(item["html"]):
                    continue
                # not a recognized division heading — keep as text
                blocks = [("text", item["html"])]
            else:
                blocks = [(item["t"], item["html"])]

            for kind, html in blocks:
                # the source references Kirfel prints under a division heading
                # belong to the heading, not to the text
                if kind == "text":
                    bare = re.sub(r"\s+", " ",
                                  re.sub(r"<[^>]+>", "", html)).strip()
                    if re.fullmatch(r"\([^()]{4,120}\)\.?", bare):
                        seg.refs = bare
                        continue
                group = seg.group or "ungrouped"
                if kind == "table":
                    soup = BeautifulSoup(html, "html.parser")
                    rows = soup.find_all("tr")
                    width = max((len(r.find_all(["td", "th"])) for r in rows),
                                default=1)
                    stats["table_blocks"] += 1
                    for row in rows:
                        cells = row.find_all(["td", "th"])
                        for i, cell in enumerate(cells):
                            # a lone cell in a multi-column table is a
                            # full-width line shared by every version -> col 1
                            col = 1 if len(cells) == 1 else i + 1
                            emit(streams, last_head, seg, group, col,
                                 clean_lines(cell.decode_contents()), bp, stats)
                    if width > 1:
                        stats["parallel_tables"] += 1
                else:
                    emit(streams, last_head, seg, group, 1,
                         clean_lines(html), bp, stats)
        spans.append((seg.group or "ungrouped", bp))

    write_files(outdir, streams, spans, stats)


def emit(streams, last_head, seg, group, col, lines, bookpage, stats):
    if not lines:
        return
    key = (group, col)
    head = seg.label()
    if head and last_head.get(key) != head:
        streams[key].append(("head", head))
        last_head[key] = head
    for line in lines:
        streams[key].append(("line", line, bookpage))
        stats["lines"] += 1


def write_files(outdir, streams, spans, stats):
    # page span per group, for the file headers
    pages_of = defaultdict(list)
    for group, bp in spans:
        pages_of[group].append(bp)

    report = []
    for (group, col) in sorted(streams,
                               key=lambda k: (k[0] == "ungrouped", k[0], k[1])):
        items = streams[(group, col)]
        name = (f"kirfel_ppl_textgruppe_{group}_col{col}.txt"
                if group != "ungrouped" else f"kirfel_ppl_ungrouped_col{col}.txt")
        pp = pages_of.get(group, [])
        lines_out = [
            f"# Kirfel, Das Purāṇa Pañcalakṣaṇa (Bonn 1927)",
            f"# Textgruppe {group}" if group != "ungrouped"
            else "# sections Kirfel prints without a Textgruppe division",
            f"# column {col} of the parallel-recension layout"
            + ("  (continuous text: single-column stretches land here)"
               if col == 1 else "  (divergent parallel passages only)"),
            f"# book pages {min(pp)}–{max(pp)}" if pp else "#",
            f"# constituted text only; critical apparatus removed",
            "",
        ]
        n_lines = 0
        for it in items:
            if it[0] == "head":
                lines_out += ["", f"## {it[1]}", ""]
            else:
                lines_out.append(it[1])
                n_lines += 1
        (outdir / name).write_text("\n".join(lines_out) + "\n", encoding="utf-8")
        words = sum(len(l[1].split()) for l in items if l[0] == "line")
        report.append((name, n_lines, words))

    print(f"{stats['lines']} constituted-text lines; "
          f"{stats['parallel_tables']} parallel-column tables\n")
    print(f"{'file':52} {'lines':>7} {'words':>8}")
    for name, n, w in report:
        print(f"{name:52} {n:>7} {w:>8}")
    print(f"\n-> {outdir}")


if __name__ == "__main__":
    main()
