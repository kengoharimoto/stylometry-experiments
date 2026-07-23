#!/usr/bin/env node
/* Build the chronology-presentation deck from the approved slide draft
 * (materials/presentation_2026/slides_draft.md, commit-reviewed 2026-07-13).
 *
 * Run from the repo root with pptxgenjs on NODE_PATH, e.g.:
 *   NODE_PATH=<dir with node_modules> node scripts/presentation/build_deck.js
 *
 * Prerequisites: figures in materials/presentation_2026/figures/ and
 * corpus_labels.json (python3 scripts/presentation/export_labels.py).
 * Output: materials/presentation_2026/chronology_stratification.pptx
 */
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(__dirname, "../..");
const MAT = path.join(ROOT, "materials/presentation_2026");
const FIG = path.join(MAT, "figures");
const fig = (name) => path.join(FIG, name + ".png");

// ── Palette (matches the figures' stratum palette) ───────────────────────────
const NAVY = "16324F";        // dark slide background
const BLUE = "1F5FA8";        // accent = epic-core blue
const INK = "222222";
const MUTED = "555555";
const FAINT = "777777";
const ICE = "CADCFC";
const CARD_EDGE = "C8C8C8";
const STRATUM = ["1F5FA8", "7BA7D4", "1A7A3A", "8FBF3F", "7A4BA8",
                 "E08A1E", "C23B3B", "E0BF1E", "7F7F7F", "3BBFBF"];
const HEAD = "SF Pro Display";   // Apple system font — titles/headings
const BODY = "SF Pro Text";      // Apple system font — body/bullets (Text optimises small sizes)

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";           // 13.3 × 7.5 in — figures are 13.33 × 7.5
pres.author = "Kengo Harimoto";
pres.title = "Chronological Stratification in the Epics and Purāṇas";
const W = 13.3, H = 7.5;

// ── Helpers ───────────────────────────────────────────────────────────────────
function dotRow(slide, y, cx = W / 2, gap = 0.34, r = 0.13) {
  const x0 = cx - (STRATUM.length - 1) * gap / 2 - r / 2;
  STRATUM.forEach((c, i) =>
    slide.addShape(pres.shapes.OVAL,
      { x: x0 + i * gap, y, w: r, h: r, fill: { color: c } }));
}

function kicker(slide, text, dark = false) {
  slide.addText(text.toUpperCase(), {
    x: 0.6, y: 0.32, w: 9, h: 0.32, fontFace: BODY, fontSize: 12,
    charSpacing: 3, color: dark ? ICE : BLUE, bold: true, margin: 0,
  });
}

function title(slide, text, opts = {}) {
  slide.addText(text, {
    x: 0.6, y: 0.62, w: W - 1.2, h: 0.9, fontFace: HEAD, fontSize: 30,
    bold: true, color: opts.dark ? "FFFFFF" : INK, margin: 0, valign: "top",
    ...opts.box,
  });
}

function fullFigure(slide, name, notes) {
  slide.background = { color: "FFFFFF" };
  slide.addImage({ path: fig(name), x: 0, y: 0, w: W, h: H });
  if (notes) slide.addNotes(notes);
}

// Act 3 tour: title strip + figure + bullet card over the map's empty
// bottom-left corner (verified point-free in all five highlight variants).
function tourSlide(kick, heading, figName, cardRuns, notes) {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, kick);
  s.addText(heading, {
    x: 0.6, y: 0.56, w: W - 1.2, h: 0.55, fontFace: HEAD, fontSize: 24,
    bold: true, color: INK, margin: 0,
  });
  const fw = 6.3 / 7.5 * 13.33, fx = (W - fw) / 2;
  s.addImage({ path: fig(figName), x: fx, y: 1.2, w: fw, h: 6.3 });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.62, y: 5.02, w: 3.55, h: 2.1, fill: { color: "FFFFFF", transparency: 5 },
    line: { color: CARD_EDGE, width: 0.75 },
  });
  s.addText(cardRuns, {
    x: 0.62, y: 5.02, w: 3.55, h: 2.1, fontFace: BODY, fontSize: 11,
    color: INK, valign: "middle", margin: 8, paraSpaceAfter: 4,
  });
  s.addNotes(notes);
  return s;
}

const bullet = (text, opts = {}) =>
  ({ text, options: { bullet: { code: "2022", indent: 12 }, breakLine: true, ...opts } });
const plain = (text, opts = {}) => ({ text, options: { breakLine: true, ...opts } });

// ══ Act 1 — The picture ═══════════════════════════════════════════════════════

// 1 · Title
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText("Chronological Stratification\nin the Epics and Purāṇas", {
    x: 1.0, y: 1.7, w: W - 2, h: 1.9, fontFace: HEAD, fontSize: 40, bold: true,
    color: "FFFFFF", align: "center", valign: "middle",
  });
  s.addText("Evidence from Stylometric Seriation", {
    x: 1.0, y: 3.7, w: W - 2, h: 0.6, fontFace: HEAD, fontSize: 22,
    italic: true, color: ICE, align: "center",
  });
  dotRow(s, 4.75);
  s.addText("Kengo Harimoto\n[venue · date]", {
    x: 1.0, y: 5.3, w: W - 2, h: 0.9, fontFace: BODY, fontSize: 16,
    color: "D8E4F5", align: "center",
  });
  s.addNotes("Thirty seconds; straight into the picture.");
}

// 2 · The map (hero)
fullFigure(pres.addSlide(), "hero_W1_delta_MDS",
  "Let the audience find their texts. Epics left, old purāṇic core upper " +
  "middle, sectarian digests right, Bhāgavata below. One color = one stratum " +
  "of the RECEIVED chronology, not of the computation.");

// 3 · The claim
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "The picture");
  title(s, "This map was drawn by counting linguistic habits — nothing else");
  const items = ["no dates", "no chronology", "no philological judgment"];
  items.forEach((t, i) => {
    const y = 2.2 + i * 0.95;
    s.addShape(pres.shapes.RECTANGLE,
      { x: 1.0, y: y + 0.12, w: 0.28, h: 0.28, fill: { color: BLUE } });
    s.addText(t, { x: 1.55, y, w: 6.5, h: 0.55, fontFace: BODY, fontSize: 24,
      color: INK, margin: 0 });
    s.addText("entered the computation", { x: 1.55, y: y + 0.42, w: 6.5, h: 0.35,
      fontFace: BODY, fontSize: 13, italic: true, color: FAINT, margin: 0 });
  });
  s.addText("The colors were painted on afterwards.", {
    x: 8.0, y: 2.5, w: 4.6, h: 0.9, fontFace: HEAD, fontSize: 20, italic: true,
    color: MUTED, margin: 0,
  });
  s.addText("Yet the familiar relative chronology reads left to right.", {
    x: 0.9, y: 5.7, w: W - 1.8, h: 0.8, fontFace: HEAD, fontSize: 26, bold: true,
    color: BLUE, align: "center",
  });
  s.addNotes("The coloring is the only place received scholarship touches the " +
    "plot; the geometry is blind.");
}

// 4 · The question
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "The picture");
  title(s, "Two questions worth thirty minutes");
  const qs = [
    ["1", "What exactly was counted?"],
    ["2", "Can the left–right axis be trusted —\nor is it an artifact of one method?"],
  ];
  qs.forEach(([n, q], i) => {
    const y = 2.4 + i * 1.9;
    s.addShape(pres.shapes.OVAL,
      { x: 1.2, y, w: 0.85, h: 0.85, fill: { color: BLUE } });
    s.addText(n, { x: 1.2, y, w: 0.85, h: 0.85, fontFace: HEAD, fontSize: 28,
      bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0 });
    s.addText(q, { x: 2.45, y: y - 0.12, w: 9.6, h: 1.35, fontFace: BODY,
      fontSize: 24, color: INK, valign: "middle", margin: 0 });
  });
  s.addNotes("Roadmap: first how the map is made, then a guided tour, then the " +
    "robustness case, then honest caveats.");
}

// ══ Act 2 — How the map was made ══════════════════════════════════════════════

// 5 · The corpus
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "How the map was made");
  title(s, "The corpus");
  const stats = [["101", "texts and sections"], ["≈ 4.6 M", "running words"],
                 ["× 2", "parallel versions:\nsandhied · unsandhied"]];
  stats.forEach(([n, l], i) => {
    const x = 0.9 + i * 4.05;
    s.addText(n, { x, y: 1.9, w: 3.7, h: 1.1, fontFace: HEAD, fontSize: 54,
      bold: true, color: BLUE, align: "center" });
    s.addText(l, { x, y: 3.0, w: 3.7, h: 0.8, fontFace: BODY, fontSize: 15,
      color: MUTED, align: "center" });
  });
  s.addText([
    bullet("Mahābhārata by parvan (18)  ·  Rāmāyaṇa by kāṇḍa (7)"),
    bullet("purāṇas whole, or by khaṇḍa / saṃhitā where transmission demands it"),
    bullet("machine-readable editions, cleaned", { breakLine: false }),
  ], { x: 1.6, y: 4.15, w: 10.5, h: 1.5, fontFace: BODY, fontSize: 17,
       color: INK, paraSpaceAfter: 8 });
  s.addText("Caveat kept in view: sections differ enormously in length; " +
    "short fragments are marked with smaller dots on every map.", {
    x: 1.6, y: 5.9, w: 10.5, h: 0.8, fontFace: BODY, fontSize: 13, italic: true,
    color: FAINT });
  s.addNotes("One line on e-text provenance; don't linger.");
}

// 6 · Countable habits (figure)
fullFigure(pres.addSlide(), "mfw_habits",
  "Left: the features are ca, tu, eva, na, sa, tathā — grammatical glue, not " +
  "content. Nobody composes with their rate of 'tu' in mind. Right: the old " +
  "purāṇic core uses tu/eva/tathā/vai about 1.5–3× as often as the " +
  "Mahābhārata; the Bhāgavata suppresses all four. These boring words carry " +
  "the signal.");

// 7 · From counts to distances
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "How the map was made");
  title(s, "From counts to distances");
  s.addText([
    plain("For each pair of texts:", { fontSize: 20 }),
    plain("how differently do they use their most common words?",
      { bold: true, fontSize: 20 }),
    plain("", {}),
    bullet("similar habits  →  small number"),
    bullet("different habits  →  large number"),
    plain("", {}),
    plain("Result: a 101 × 101 table of stylistic distances", { fontSize: 18 }),
    plain("(Burrows’s Delta — stylometry’s standard workhorse since 2002)",
      { italic: true, fontSize: 13, color: FAINT, breakLine: false }),
  ], { x: 0.9, y: 2.1, w: 6.2, h: 4.4, fontFace: BODY, fontSize: 17, color: INK,
       paraSpaceAfter: 8, valign: "top" });
  const rows = [
    [{ text: "pair", options: { bold: true, color: "FFFFFF", fill: { color: BLUE } } },
     { text: "distance", options: { bold: true, color: "FFFFFF", fill: { color: BLUE }, align: "center" } }],
    ["MBh 7 (Droṇa)  ↔  MBh 8 (Karṇa)", { text: "0.28", options: { align: "center" } }],
    ["Vāyu  ↔  Brahmāṇḍa", { text: "0.29", options: { align: "center" } }],
    [{ text: "typical pair in this corpus", options: { italic: true, color: MUTED } },
     { text: "1.04", options: { align: "center", italic: true, color: MUTED } }],
    ["Rām 2 (Ayodhyā)  ↔  Agni", { text: "1.36", options: { align: "center" } }],
  ];
  s.addTable(rows, { x: 7.5, y: 2.5, w: 5.1, colW: [3.7, 1.4],
    fontFace: BODY, fontSize: 15, color: INK, rowH: 0.55, valign: "middle",
    border: { pt: 0.75, color: "DDDDDD" } });
  s.addNotes("No formulas: 'an average of disagreements in word habits, in " +
    "units of what is normal for this corpus.' Table rows preview later tour stops.");
}

// 8 · Two independent lenses
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "How the map was made");
  title(s, "The same corpus, measured twice");
  const hdr = (t) => ({ text: t, options: { bold: true, color: "FFFFFF",
    fill: { color: BLUE }, align: "center", fontSize: 16 } });
  const lbl = (t) => ({ text: t, options: { bold: true, color: MUTED,
    fill: { color: "F2F4F7" } } });
  const rows = [
    [lbl(""), hdr("Lens 1 — words"), hdr("Lens 2 — letter groups")],
    [lbl("counts"), "the 80 most frequent words",
     "the 5,000 most frequent 3-letter sequences"],
    [lbl("input"), "sandhi dissolved (segmented)", "raw sandhied text"],
    [lbl("sees"), "particles, pronouns, vocabulary habits",
     "morphology, phonology, sandhi habits"],
  ];
  s.addTable(rows, { x: 1.3, y: 2.2, w: 10.7, colW: [1.5, 4.6, 4.6],
    fontFace: BODY, fontSize: 15, color: INK, rowH: 0.75, valign: "middle",
    border: { pt: 0.75, color: "DDDDDD" } });
  s.addText("Nearly orthogonal measurements — almost no shared failure modes.", {
    x: 0.9, y: 5.8, w: 11.5, h: 0.7, fontFace: HEAD, fontSize: 20, bold: true,
    color: BLUE, align: "center" });
  s.addNotes("Flag now, cash in at Act 4: any segmentation-pipeline artifact " +
    "could only touch Lens 1; any orthographic/sandhi artifact only Lens 2.");
}

// 9 · MDS explainer (figure)
fullFigure(pres.addSlide(), "mds_explainer",
  "Mileage-chart analogy: given only road distances between cities you can " +
  "redraw the map of India. MDS does exactly that with stylistic distances. " +
  "The opening map is this with the full 101×101 table. Axes mean nothing by " +
  "themselves; only nearness does.");

// ══ Act 3 — Reading the map ═══════════════════════════════════════════════════

tourSlide("Reading the map · 1", "The epic zone", "hero_W1_delta_MDS_hl-epic", [
  bullet("battle books MBh 6–9 tight; Droṇa ↔ Karṇa the tightest pair (0.28 ≈ ¼ of typical)"),
  bullet("MBh 12–13: mutual nearest neighbours — drifted toward purāṇa-space"),
  bullet("Rām 2–6 hold together; Bāla ↔ Uttara are each other’s nearest neighbour"),
  plain("Structure recovered blind — without assuming any of it.", { italic: true, color: MUTED, breakLine: false }),
],
  "The machine has read no Hopkins and no Brockington, yet the battle books " +
  "cluster, the didactic parvans MBh 12–13 drift toward purāṇa-space, and the " +
  "two framing khaṇḍas resemble each other. Note (no chronology assumed): " +
  "coloring is by text — Mahābhārata vs Rāmāyaṇa — not by supposed date; the " +
  "closing parvans’ extreme position is a finding, not an input. Precision " +
  "for Q&A: Bāla↔Uttara mutual in the word lens; in the 3-gram lens both are " +
  "nearest to MBh 3.");

tourSlide("Reading the map · 2", "The old purāṇic core?", "hero_W1_delta_MDS_hl-oldcore", [
  bullet("Vāyu ↔ Brahmāṇḍa: 0.29 — Kirfel’s Vāyuproktaṃ Purāṇam, as a number"),
  bullet("Viṣṇu ↔ Mārkaṇḍeya: mutual nearest neighbours, in both lenses"),
  bullet("Matsya’s cosmogonic chapters sit with them", { breakLine: false }),
],
  "Kirfel (1927) predicted this cluster a century ago; the counting confirms " +
  "it without being told. The Vāyu∩Brahmāṇḍa common-material extract (V×B) " +
  "sits closest of all to both.");

tourSlide("Reading the map · 3", "The old Skandapurāṇa: mostly old but Pāśupata yoga added later", "hero_W1_delta_MDS_hl-oldsp", [
  bullet("the old SP (Nepal/Bengal recension, oldest MS 811 CE) sits between the epics and the old purāṇic core"),
  bullet("word lens: its nearest neighbours are MBh 1, MBh 10 and Rām 6 — it keeps epic diction"),
  bullet("but its Pāśupata section jumps far right, out among the sectarian digests", { breakLine: false }),
],
  "A single work, stratified in front of you: the narrative body reads as a " +
  "bridge between epic and purāṇa (in the 3-gram lens it shifts toward " +
  "Matsya/Brahma, the old core), while the Pāśupata doctrinal chapters (SP2) " +
  "land at the far right with the Śivapurāṇa (Umā, Sanatkumāra) as their " +
  "word-lens neighbours. The Vāyupurāṇa has its own Pāśupata-yoga section " +
  "(V2 on the map) that makes the very same jump to the far right — and the " +
  "two Pāśupata sections share virtually no text (word-trigram overlap ≈ " +
  "0.002, no higher than with an unrelated control; longest shared run four " +
  "words), so their convergence is doctrinal register, not borrowing. Caveat " +
  "for Q&A: SP2 is a short excerpt, so its exact spot is soft — but the " +
  "direction of the jump is unmistakable. LIVE: mention the forthcoming " +
  "edition of the Pāśupata-yoga chapters — the lenses flag exactly what its " +
  "editors suspected.");

tourSlide("Reading the map · 4", "The sectarian & encyclopedic mass", "hero_W1_delta_MDS_hl-late", [
  bullet("one broad, continuous stratum — no clean line between “middle” and “late”"),
  bullet("Agni · Garuḍa · Nārada: the encyclopedic digests, crowded on the far right"),
  bullet("internally blurry — exactly what compilation literature should look like", { breakLine: false }),
],
  "Folded into one group on purpose: on the map the old boundary between " +
  "‘middle purāṇic’ and ‘late sectarian/encyclopedic’ does not survive — the " +
  "two overlap heavily on axis 1 (medians +0.05 vs +0.21, ranges swamping the " +
  "gap) and the split rested on external dating and genre, not on the counts. " +
  "The stratum shades from texts still close to the old core (Kūrma, Liṅga, " +
  "Viṣṇudharmottara) out to the self-quoting digests at the right, where its " +
  "style is simply the style of the digest.");

tourSlide("Reading the map · 5", "A purāṇa that refuses to unify", "hero_W1_delta_MDS_hl-skmp", [
  bullet("the Skāndamahāpurāṇa: 0 of 4 khaṇḍas with an internal nearest neighbour, in either lens"),
  bullet("they share no text; all full-sized — no length caveat"),
  bullet("what connects them: the colophon phrase (śrī)skānde mahāpurāṇe"),
  plain("ŚiP: same story (3/8, 4/8 internal). Cohesion is measurable — next slide.", { italic: true, color: MUTED, breakLine: false }),
],
  "The compilation model, confirmed from word counts alone; contrast with " +
  "the Bhāgavata set up deliberately. Nothing connects the khaṇḍas but the " +
  "colophon phrase: Kāśīkhaṇḍa’s word-lens NN is Bhaviṣya, Himavat’s is ŚiP " +
  "Dharma, Sūtasaṃhitā’s is Garuḍa 1. Best detail if time allows: the " +
  "Revākhaṇḍa’s NN (both lenses) is the OTHER Revākhaṇḍa, the distinct one " +
  "transmitted with the Vāyu — the two share ~5% of their lines verbatim " +
  "while each shares only stock formulae with its own host. A khaṇḍa can be " +
  "closer to its namesake in another purāṇa than to its own compilation.");

tourSlide("Reading the map · 6", "The Bhāgavata", "hero_W1_delta_MDS_hl-bhp", [
  bullet("all twelve skandhas’ nearest neighbours are internal — in both lenses"),
  bullet("archaic features noticed for over a century (Michelson 1909; Meier 1931; van Buitenen 1966) — and a date that has never stopped being disputed"),
  bullet("the counts find two layers that do not match: bulk habits that are epic, not purāṇic — and a thin, even layer of Vedic particles (aṅga, bata, vāva) found nowhere else in the corpus"),
  plain("The numbers do not settle its date; they deepen its puzzle.", { italic: true, color: MUTED, breakLine: false }),
],
  "The date of the purāṇa has always been in dispute. What we have here " +
  "adds more data points.");

// ══ Act 4 — Why believe the axis? ═════════════════════════════════════════════

// 15 · Robustness grid (figure)
fullFigure(pres.addSlide(), "robustness_grid",
  "Walk the grid: top row words/unsandhied, bottom row 3-grams/sandhied, " +
  "three distance metrics each — six independent pipelines, one geometry. " +
  "Layout agreement with the opening map: 0.95–0.96 (words), 0.82–0.89 " +
  "(3-grams). The epic→purāṇic axis survives every change of lens.");

// 16 · Convergence argument
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "Why believe the axis?");
  title(s, "Suppose the axis were an artifact…");
  const rows = [
    ["a flaw in sandhi segmentation", "could distort the word lens only"],
    ["an orthographic / sandhi convention", "could distort the 3-gram lens only"],
    ["a quirk of one distance formula", "fails to explain the other five"],
  ];
  rows.forEach(([a, b], i) => {
    const y = 2.0 + i * 0.95;
    s.addText(a, { x: 0.9, y, w: 5.1, h: 0.7, fontFace: BODY, fontSize: 18,
      color: INK, valign: "middle", margin: 0 });
    s.addText("→", { x: 6.1, y, w: 0.6, h: 0.7, fontFace: BODY, fontSize: 20,
      color: BLUE, bold: true, align: "center", valign: "middle", margin: 0 });
    s.addText(b, { x: 6.9, y, w: 5.6, h: 0.7, fontFace: BODY, fontSize: 18,
      italic: true, color: MUTED, valign: "middle", margin: 0 });
  });
  s.addText("The lenses share almost no assumptions — yet draw the same axis.", {
    x: 0.9, y: 5.1, w: W - 1.8, h: 0.6, fontFace: BODY, fontSize: 18,
    color: INK, align: "center" });
  s.addText("The signal is in the texts.", {
    x: 0.9, y: 5.8, w: W - 1.8, h: 0.9, fontFace: HEAD, fontSize: 30, bold: true,
    color: BLUE, align: "center" });
  s.addNotes("The abstract's core argument; deliver slowly.");
}

// 17 · The second axis
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "Why believe the axis?");
  title(s, "What the second axis is not");
  s.addText([
    plain("The vertical axis is unstable across configurations.", { fontSize: 22 }),
    plain("", {}),
    plain("Depending on features and metric it separates by something like " +
      "genre, region, or sectarian register — no labeling survives all six " +
      "panels.", { fontSize: 18, color: MUTED, breakLine: false }),
  ], { x: 0.9, y: 2.1, w: 11.4, h: 2.4, fontFace: BODY, color: INK,
       paraSpaceAfter: 10 });
  s.addText([
    { text: "Honest conclusion:  ", options: { bold: true } },
    { text: "one axis is chronology-like and robust; the second resists a stable name." },
  ], { x: 0.9, y: 5.0, w: 11.4, h: 1.1, fontFace: HEAD, fontSize: 22,
       color: BLUE, align: "center", valign: "middle" });
  s.addNotes("Promised in the abstract; agnosticism as a feature, not a " +
    "weakness. The Bhāgavata's vertical displacement is the clearest case.");
}

// ══ Act 5 — Caveats and implications ══════════════════════════════════════════

// 18 · Confounds
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "Caveats");
  title(s, "What the axis is made of");
  s.addText("“Diachronic linguistic drift” — but confounded:", {
    x: 0.9, y: 1.75, w: 11, h: 0.5, fontFace: BODY, fontSize: 19, italic: true,
    color: MUTED, margin: 0 });
  const rows = [
    ["metre", "the favourite particles are anuṣṭubh fillers; particle habits are partly versification habits"],
    ["borrowing", "the tightest links ride on shared ślokas — Delta cannot tell “same school” from “copied the same 2,000 verses”"],
    ["genre", "narrative vs. didactic vs. digest"],
  ];
  rows.forEach(([a, b], i) => {
    const y = 2.5 + i * 1.15;
    s.addText(a, { x: 1.0, y, w: 2.3, h: 1.0, fontFace: HEAD, fontSize: 21,
      bold: true, color: BLUE, margin: 0 });
    s.addText(b, { x: 3.6, y, w: 8.9, h: 1.0, fontFace: BODY, fontSize: 17,
      color: INK, margin: 0 });
  });
  s.addText("So the epic pole marks low expository overlay, which tracks — but " +
    "is not — early date: late-but-unexpanded books (MBh 16–18) land there too.", {
    x: 1.0, y: 6.15, w: 11.5, h: 0.9, fontFace: BODY, fontSize: 16, italic: true,
    color: MUTED, margin: 0 });
  s.addNotes("Drift, metre, borrowing and genre are entangled in the texts " +
    "themselves; the axis is real but not purely temporal. The closing parvans " +
    "(backup) are the sharp case: at 1–3k words their individual positions are " +
    "unreliable, but merged they stay at the pole — register, not length.");
}

// 19 · What this is — and is not
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "Implications");
  title(s, "What this is — and is not");
  s.addText([
    bullet("purāṇas have no authors  →  this is stratum and textual-family " +
      "detection, not authorship attribution"),
    bullet("stylometry offers an independent, replicable check on relative " +
      "chronology — a third witness beside content criteria and testimonia"),
    bullet("it will not date your text; it will tell you whose company it keeps",
      { breakLine: false }),
  ], { x: 1.0, y: 2.1, w: 11.3, h: 3.6, fontFace: BODY, fontSize: 20,
       color: INK, paraSpaceAfter: 18 });
  s.addNotes("Position the method modestly; invite collaboration on specific " +
    "text-historical problems.");
}

// 20 · Closing
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText("Counted habits, familiar history.", {
    x: 1.0, y: 0.55, w: W - 2, h: 0.8, fontFace: HEAD, fontSize: 30,
    italic: true, color: "FFFFFF", align: "center" });
  const iw = 9.6, ih = iw * 7.5 / 13.33;
  s.addImage({ path: fig("hero_W1_delta_MDS"), x: (W - iw) / 2, y: 1.55,
    w: iw, h: ih });
  dotRow(s, 7.12);
  s.addNotes("End where we began — now everyone can read the map. Thanks; " +
    "over to questions.");
}

// ══ Backup slides ═════════════════════════════════════════════════════════════

{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText("Backup slides", { x: 1, y: 3.0, w: W - 2, h: 1.0, fontFace: HEAD,
    fontSize: 36, bold: true, color: "FFFFFF", align: "center" });
  dotRow(s, 4.35);
}

// B1 · Delta one level deeper
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "Backup");
  title(s, "Burrows’s Delta, one level deeper");
  s.addText([
    bullet("for each of the top-80 words: how far is each text from the " +
      "corpus-average rate, in standard deviations (a z-score)?"),
    bullet("Delta(A, B) = the average disagreement of A and B across those words"),
    bullet("variants in the grid: Cosine Delta (angle instead of average); " +
      "min-max and Manhattan (raw-frequency geometry)", { breakLine: false }),
  ], { x: 1.0, y: 2.05, w: 11.3, h: 3.4, fontFace: BODY, fontSize: 19,
       color: INK, paraSpaceAfter: 16 });
}

// B2 · Full corpus with strata (from corpus_labels.json)
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "Backup");
  title(s, "The 101 texts and their strata");
  const data = JSON.parse(fs.readFileSync(path.join(MAT, "corpus_labels.json"), "utf8"));
  const byStratum = new Map();
  data.forEach((d) => {
    if (!byStratum.has(d.stratum)) byStratum.set(d.stratum, []);
    byStratum.get(d.stratum).push(d);
  });
  const lines = [];
  [...byStratum.keys()].sort((a, b) => a - b).forEach((st) => {
    const g = byStratum.get(st).sort((a, b) => a.code.localeCompare(b.code, "en", { numeric: true }));
    lines.push({ text: g[0].label, options: { bold: true, color: STRATUM[st - 1],
      breakLine: true, fontSize: 9.5 } });
    g.forEach((d) => lines.push({ text: `${d.code}  ${d.display}`,
      options: { breakLine: true, fontSize: 9, color: INK } }));
  });
  // split into columns, never leaving a group header orphaned at a column end
  const nCols = 4, per = Math.ceil(lines.length / nCols);
  const cols = [];
  let pos = 0;
  for (let c = 0; c < nCols; c++) {
    let end = Math.min(pos + per, lines.length);
    if (c === nCols - 1) end = lines.length;
    else if (end < lines.length && lines[end - 1].options.bold) end -= 1;
    cols.push(lines.slice(pos, end));
    pos = end;
  }
  for (let c = 0; c < nCols; c++) {
    const chunk = cols[c];
    if (!chunk.length) continue;
    chunk[chunk.length - 1] = { ...chunk[chunk.length - 1],
      options: { ...chunk[chunk.length - 1].options, breakLine: false } };
    s.addText(chunk, { x: 0.65 + c * 3.1, y: 1.65, w: 3.0, h: 5.7,
      fontFace: BODY, valign: "top", margin: 0, paraSpaceAfter: 1.2 });
  }
}

// B3 · Length caveat
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "Backup");
  title(s, "The length caveat");
  s.addText([
    bullet("sections range from a few thousand to hundreds of thousands of words"),
    bullet("sub-5k-word fragments have noisy profiles → inflated distances, " +
      "unreliable positions"),
    bullet("marked as small dots on every map; none of the argument rests on them",
      { breakLine: false }),
  ], { x: 1.0, y: 2.05, w: 11.3, h: 3.4, fontFace: BODY, fontSize: 19,
       color: INK, paraSpaceAfter: 16 });
}

// B4 · When the lenses disagree
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  kicker(s, "Backup");
  title(s, "When the lenses disagree — a diagnostic, not a failure");
  s.addText("BhP 10.29–33 transmitted with commentary (Bh10c on the maps):", {
    x: 1.0, y: 1.85, w: 11.3, h: 0.5, fontFace: BODY, fontSize: 18, bold: true,
    color: INK, margin: 0 });
  s.addText([
    bullet("word lens: nearest neighbour = Kāśīkhaṇḍa — expelled from the " +
      "Bhāgavata cluster (commentary vocabulary contaminates word counts)"),
    bullet("3-gram lens: nearest neighbour = BhP 10 — back inside the family",
      { breakLine: false }),
  ], { x: 1.0, y: 2.45, w: 11.3, h: 2.0, fontFace: BODY, fontSize: 18,
       color: INK, paraSpaceAfter: 14 });
  s.addText("Lens disagreement flags preprocessing problems — it does not hide them.", {
    x: 1.0, y: 5.3, w: 11.3, h: 0.9, fontFace: HEAD, fontSize: 21, bold: true,
    color: BLUE, align: "center" });
  s.addNotes("If asked about pipeline trust: same story with the Nīlamata, " +
    "where a raw-cosine outlier exposed an editorially dissolved source " +
    "(2026-07-09).");
}

// B5 · Consensus tree
fullFigure(pres.addSlide(), "consensus_tree",
  "If someone asks for a tree: here it is. Cosine Delta on the same 80 " +
  "words, 500 bootstrap replicates (the words are resampled with " +
  "replacement), neighbour-joining per replicate, majority-rule consensus — " +
  "so every branch on the slide is one that survived in more than half of " +
  "the replicates. Rooted arbitrarily on MBh 6. It finds the same groups " +
  "the map does: the epics, Vāyu–Brahmāṇḍa and the old purāṇic core, the " +
  "Bhāgavata, the Śivapurāṇa. But a tree asserts descent and nesting, and " +
  "our texts drift into one another instead of branching cleanly — which " +
  "is why the talk is built on the map, not on this.");

// B6 · Closing parvans / length control
fullFigure(pres.addSlide(), "closing_parvans_length",
  "The sharp question a specialist will ask: the closing parvans MBh 16–18 " +
  "sit at the extreme epic pole, ‘earlier’ than the battle books — surely " +
  "that is just their tiny length? Answer in two moves. (1) It is partly a " +
  "length effect: drawing random contiguous windows of securely-placed texts " +
  "(MBh 3/7/12, Vāyu, Agni) and running them through the identical pipeline, " +
  "at 1–2k words — the size of MBh 16–18 — the 3-gram lens drifts leftward " +
  "and the word lens scatters so wide that single short windows reach the " +
  "pole. So the individual positions of MBh 16/17/18 are unreliable; do not " +
  "build anything on them alone (they carry the small-dot / length flag). " +
  "(2) But it is not only length: concatenate 15+16+17+18 into one ~17k-word " +
  "unit and it stays at the pole, not out by MBh 11/14. The group position " +
  "is real. What it measures is register — narrative-pure text with little of " +
  "the expository-particle overlay (tu/eva/tathā/vai) that swelled MBh 12–14 " +
  "— i.e. late as books, redactionally thin as text, not early. This " +
  "reconciles the stylometry with the received ‘late epilogue’ verdict " +
  "(Brockington 1998) rather than contradicting it. Full diagnostics: " +
  "notes/2026-07-15_closing_parvans_length_diagnostics.md.");

// B7 · The Bhāgavata, book by book
fullFigure(pres.addSlide(), "bhp_skandha_mfw",
  "For the question ‘is the particle avoidance the work of one book, or of " +
  "an editor of one layer?’ No: all 48 cells (12 books × 4 particles) sit " +
  "below the old purāṇic core’s median rates (tu 17.8, eva 13.3, tathā 9.1, " +
  "vai 7.2 per 1,000). Phrase it group-relative: against the corpus at " +
  "large, vai is NOT suppressed (BhP ≈ MBh ≈ corpus median; only the old " +
  "core is vai-heavy), and eva rises to low-normal in books 5 and 12 " +
  "(8.3/7.3 — even #3 in their own top tens, visible as the red bars). " +
  "What the BhP runs on instead: ca, na, uvāca, śrī, bhagavān, api — and, " +
  "at rates unique to it in this corpus, the Vedic particles aṅga, bata, " +
  "vāva of the Bhāgavata slide.");

const OUT = path.join(MAT, "chronology_stratification.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
