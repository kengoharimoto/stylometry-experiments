# Outline B — Digital humanities venue

**Candidate venues:** Digital Scholarship in the Humanities (OUP); Journal
of Cultural Analytics (methods-friendly, open); Digital Humanities
Quarterly. **Audience assumption:** knows Delta, MDS, Eder/Evert/Rybicki;
does NOT know sandhi, the purāṇas, or why this corpus is hostile terrain.
**Length budget:** 8,000–11,000 words. **Register:** the corpus is taught;
the methods are *contributed*. The paper's identity: what it takes to make
stylometry yield relative chronology in an authorless, formulaic,
heavily-reused, editorially-mediated corpus — and a mechanistic account of
*why* it works when it does.

**Working title idea:** "Losses are the clock: recovering relative
chronology from stylometric drift in the Sanskrit epics and purāṇas."

> **REFRAME 2026-08-19 (Kengo): no-reuse precedence — supersedes the
> section flow below where they conflict.** The chronology argument now
> runs: (i) with-reuse maps = the tradition as transmitted (language
> mixture of all layers present); (ii) reuse-stripped maps = the
> compilers' own diction; (iii) consequences of the difference (order
> stable at ρ 0.91 W1 / 0.98 C3; the great compilations move early-ward;
> old-core carriers dissolve into sub-3k uncertainty; Viṣṇu–Bhāgavata
> affinity revealed); (iv) why no-reuse is the better estimate of the
> chronology of *original composition* (upgraded-purāṇa argument);
> (v) 3-D structure: axis 3 = the Bhāgavata dimension; 2-D flattening
> guardrail. "Language age ≠ book age" sharpens into *transmitted*
> vs *composed* language. Evidence + work queue (R1–R4, A6):
> `notes/2026-08-19_noreuse_precedence_reframe.md`, claims map §0 gate.
> Draft surgery on `draft_dh.md` waits for R1/R2 numbers and Kengo's
> answer on R4 (Śivadharma example direction).

---

## 1. Introduction (≈1,200 w)
Stylometry's home turf is authorship; chronology is the harder, rarer
target (brief lit: intra-author chronometry, stylochronometry). This
corpus inverts every usual assumption: no authors, centuries of accretion,
massive verbatim reuse, orthography and word division that belong to
editors. Claim preview: a two-lens design + a battery of controls yields a
stable one-dimensional ordering; null models show such an axis is the
signature of autocorrelated change; a retention decomposition explains it.

## 2. A hostile corpus, and the preprocessing it forces (≈1,500 w)
Sanskrit for stylometrists in two pages: sandhi, scriptio continua,
editorial word division. The design answer: **W1** on neural unsandhied
text (ByT5) vs **C3 on the whitespace-stripped stream** — two lenses with
largely disjoint linguistic material (bridge table: closed classes 38% of
W1 signal, 12% of C3). War stories as method: the U+1E00 tokenizer bug;
the Nīlamata episode (raw cosine as a preprocessing-inconsistency
detector); colophon paratext bias (ρ −0.58) and its cleanup. Each is a
generalizable caution for non-Latin-script stylometry.
*Figures: pipeline diagram; class signal-share table.*

## 3. The ordering and its robustness (≈2,000 w)
Hero maps; the convergence result (ρ 0.953 at 500×500, ridge heatmap);
MFW/metric sweeps compressed to one table + the two instructive failures
(W1 cliff = content takeover; "robustness by deafness" of unstandardized
metrics); reuse removal (cross-build 0.98–0.99); names struck; exact
independent replication in stylo; length limits stated as a shared failure
mode. *Figures: map pair; heatmap; robustness table; length panel.*

## 4. Why a drift axis emerges: null and generative models (≈1,500 w)
**The paper's methodological centerpiece.** Exchangeable null → 13.1%
axis-1 share that is pure length artifact (the cautionary result: share
alone misleads); heterogeneity without covariance → 3.3%; Brownian drift →
43% and recovers the latent order at 0.99. A dominant, ordering-shaped,
length-independent first axis = autocorrelated change. B3: the gradient
is in every global method's top-2 plane (PCA 0.995); TSP's failure proves
the second dimension; why t-SNE/UMAP are excluded. *Figures: null-model
table; convergent-orderings table.*

## 5. What the axis counts (≈1,200 w)
A1 distributed loadings; A2 decomposition — no class necessary, nearly
every class sufficient (redundancy as the signature of drift); the
boundary-phonology exception. *Figures: decomposition tables.*

## 6. Losses are the clock (≈1,200 w)
B2b as the explanatory payoff and the bridge to historical linguistics:
split-half retention decomposition; loss alone ρ 0.939, gains 0.72,
presence/absence 0.47; the Swadesh/stochastic-Dollo lineage stated
precisely; what this predicts for other corpora. *Figure: loss/gain table.*

## 7. Validation against known relative order + case results (≈1,500 w)
The corpus pays the method back: E1 apparatus layers (known-later material
measures later, both lenses); PPL stratum inside host purāṇas; Kirfel's
Textgruppen sorted to his own grouping; genre control bounded. Then the
headline case findings in one page each, guardrails intact: closing
parvans block; PPL → SP → Mārk; the BhP posed as open (symmetric wording,
one paragraph, pointer to the Indological companion/literature).
*Figures: E1 table; stratigraphy dot-strip.*

## 8. The second dimension (≈600 w)
No horseshoe (R² ≤ 0.02) — worth a DH audience's attention since the arch
is folklore; cross-lens y 0.82; named as register (catalogue ↔ devotion);
covariates explain about half; never a second chronology.

## 9. Conclusion (≈600 w)
A recipe: two orthogonal lenses + fixed-map projection for layers + null
models + retention decomposition = chronology-capable stylometry in
authorless corpora. Limits and transfer conditions.

---

**What this variant cuts:** the external-attestation philology (purāṇa
witnesses, Rām sweep, BhP quotation channels) → one summarizing paragraph
+ citations; most per-text argumentation; appendix-level CI tables.
**Dependencies:** none blocking — A5 optional here, A4 dropped
2026-08-17 (a strength: this variant can be drafted first). **Risks:** a referee asking for ground-truth
dates — answered by the known-relative-order validation framing; corpus
availability questions — answered by repo + derived-frequency release.
