# Report writing guide — arXiv daily digest

Use this when converting `digests/YYYY-MM-DD.raw.json` → `digests/YYYY-MM-DD.md`.

**Audience:** Helen Shao — computational cosmology, LSS×CMB, PhD on MAPs/DESI + CMB B-mode Fisher.

**Voice:** Colleague briefing, not textbook. Lead with *why it matters to your program*, then facts. No filler ("this interesting paper explores…").

---

## Report anatomy (required sections)

```markdown
# arXiv Daily Digest — YYYY-MM-DD

**Source:** <listing url>
**Raw data:** `digests/YYYY-MM-DD.raw.json` (fetched <ISO timestamp>)
**Scanned:** N | **Relevant:** M (H high · M mod) | **Criteria:** relevance-criteria.md

## Priority reads today
1. [`id`](url) — one line: why read first
2. ...

## Themes today
- **DESI / galaxy–halo:** …
- **CMB / delensing:** …
- **PNG / primordial:** …
- **Methods (EFT / inference / ML):** …

## At a glance
| Tier | ID | Title (short) | Tags | Action |
|------|-----|---------------|------|--------|

## High relevance
<full cards — one per paper>

## Moderate relevance
<compact cards>

## Not reported
K papers omitted (exoplanets, stellar, unrelated, or Low tier).
```

Omit empty theme bullets. Omit **Priority reads** if only 1–2 relevant papers total.

---

## High-tier paper card (copy this structure)

```markdown
### [Full title](https://arxiv.org/abs/XXXX.XXXXX) · `XXXX.XXXXX`

| Field | Content |
|-------|---------|
| **Authors** | First author et al. (flag colleague names **bold**) |
| **Subjects** | From JSON `subjects` |
| **Type** | `data` · `forecast` · `simulation` · `theory` · `methods` |
| **Tags** | P1, U, π |
| **Boosts** | survey · inference · π · colleague |

**Bottom line:** One sentence — the single reason this is on-program.

**What they did:** 2–3 sentences paraphrasing the abstract (problem + method). No jargon padding.

**Main result:** One bullet with **numbers only if in abstract** (constraints, σ, % improvement, k_max, f_sky, etc.). If no numbers, state qualitative claim.

**Links to your program:**
| Anchor | Connection |
|--------|------------|
| **P1** / **P2** / **Unified** / **Prior** / **PNG-sims** | Specific file, method, or open question — not generic "relevant to DESI" |
| **Open question** | Quote or paraphrase from RESEARCH_INTERESTS.md when applicable |

**Insight:** One sentence a skim would miss — degeneracy, systematic, method transfer, or tension with your approach.

**Critical comment:** One sentence — your read on what matters most (agree/disagree, surprise, tension with another paper in today's list, or why the method choice is clever/risky). This is *your* take, not a fourth summary sentence.

**Future work:** 1–2 bullets — concrete next steps *you* could take building on this paper (analysis to run, mock to build, comparison to add, collaborator to ping). Must name a deliverable, not "could be interesting."

**Pursue timing:** `Now (tandem)` · `Near-term` · `Background` — see [Pursue timing rubric](#pursue-timing-rubric) below. **Required for every High card.** One sentence: *why this timing* and *what active thread it plugs into*.

**Caveat:** One sentence — main limitation stated or implied in abstract (foregrounds, bias model, linear theory, etc.).

**Action:** `Read now` · `Skim` · `Watch` · `Cite` — plus 5-word reason.
```

### Action rubric

| Action | When |
|--------|------|
| **Read now** | Directly affects active work (MAP validation, AbacusAurora PNG ICs, Fisher σ(r), Quijote-PNG follow-up) |
| **Skim** | Useful context; read abstract + figures if time |
| **Watch** | Moderate tier trending toward your space; check when cited or updated |
| **Cite** | Methods or results you may reference in proposal/paper soon |

---

## Moderate-tier card (compact)

```markdown
### [Title](url) · `id`
**Tags:** M, π · **Type:** theory  
**Bottom line:** One sentence.  
**Connection:** One bullet naming project anchor.  
**Action:** Watch | Skim
```

Max 4 lines body per Moderate paper. Do not use full High template.

---

## How to write each field

### Bottom line vs Summary vs Insight vs Critical comment

| Field | Question it answers |
|-------|---------------------|
| **Bottom line** | "Should Helen stop scrolling for this?" |
| **What they did** | "What is the paper?" (faithful to abstract) |
| **Main result** | "What did they find?" (evidence only) |
| **Insight** | "What does Helen do with this?" (interpretation — label as inference) |
| **Critical comment** | "What's my honest reaction?" (judgment, surprise, cross-paper tension) |
| **Future work** | "What would I actually do next?" (actionable bullets with deliverables) |
| **Pursue timing** | "Do I drop everything, queue it, or shelf it?" (tandem/near-term/background + why) |
| **Caveat** | "What could go wrong?" |

**Insight must not** repeat the abstract or state the obvious ("DESI is important for cosmology").

**Critical comment must not** be a polite restatement of Insight. It should take a position: e.g. "The universality-relation prior dominates the error budget — without HMF-based \(p\), this constraint is mostly prior-driven" or "Directly competes with your ARF-style beyond-2pt angle but uses a simpler observable."

### Links to your program — use concrete anchors

Map tags to real assets (pick the best fit):

| Tag | Good connection examples |
|-----|--------------------------|
| **P1** | MAP mock ELG×LRG validation; HOMe benchmark; AbacusAurora ICs; fiber collisions; assembly bias at r < 1 h⁻¹ Mpc |
| **P2** | Pixel Fisher F_rr; R·D·B·Y operator chain; σ(r) degradation; delensing + Π_B; IV taper / E/B mixing |
| **U** | DESI×ACT lensing; neutrino paper-style multi-probe MCMC; kSZ tomography; joint σ_8 / Σm_ν |
| **M** | DESI EFT full-shape; SBP from sims; marked stats; GNN/SBI; Zel'dovich CV covariances |
| **π** | Quijote-PNG / `2LPTPNG`; f_NL–b_φ degeneracy; parity-odd `2LPTPNG-ODD`; AbacusAurora PNG IC roadmap |
| **Prior** | CAMELS robustness; neutrino MCMC template; symbolic regression |

Bad: "Relevant to large-scale structure."  
Good: "Benchmarks multi-tracer ξ at 0.8 < z < 1.1 — direct comparison target for MAP ELG×LRG mocks."

### Cosmology field extras (when applicable)

Add to **Main result** or **Caveat** if mentioned in abstract:

- **Surveys / data:** DESI, ACT, Planck, SO, Euclid, etc.
- **Observable:** P(k), ξ, bispectrum, C_ℓ, lensing, B-modes, kSZ
- **Parameters:** σ_8, Ω_m, Σm_ν, r, f_NL, w, n_s
- **Analysis:** EFT, Fisher, MCMC, mock covariance, systematics named
- **Forward model:** N-body, HOD, hydro, IC generator

Do **not** invent priors, covariances, or constraints not in the abstract.

---

## Themes today — grouping rules

Cluster High + Moderate papers into 2–5 theme bullets. Examples:

- **DESI / multi-tracer / HOD–MAP**
- **CMB lensing / delensing / B-modes**
- **PNG / inflation / neutrinos**
- **EFT / inference / emulators**
- **Parity-violating / non-Gaussian ICs**

Format: `**Theme:** paper-id — half-line; paper-id — half-line.`

---

## Priority reads today

Top 1–3 High-tier papers only. One line each — the actionable hook, not the title repeated.

Example:
`1. [2606.xxxxx](url) — DESI DR2 ELG×LRG systematics directly overlap MAP validation plan.`

---

## Ordering

1. **Priority reads** — most actionable first  
2. **High relevance** — P1/P2 direct hits before pure methods; boosted before unboosted  
3. **Moderate** — π and survey hooks before generic theory  

Within a tier, sort by tag priority: P1, P2, U, π, M.

---

## Quality checklist (before saving .md)

- [ ] Every High card has: Bottom line, What they did, Main result, Links (≥1 concrete anchor), Insight, Critical comment, Future work (≥1 bullet), Pursue timing, Caveat, Action
- [ ] At least one High card flagged `Now (tandem)` when the day's list warrants it — do not leave all papers at Skim/Background
- [ ] Every Moderate card ≤ 4 lines + header
- [ ] No fabricated numbers, surveys, or constraints
- [ ] Colleague names **bolded** when in author list
- [ ] `Scanned` / `Relevant` counts match JSON triage
- [ ] Themes and Priority reads reflect only included papers
- [ ] Insight sentences are non-obvious

---

## Anti-patterns

| ❌ Avoid | ✅ Instead |
|----------|-----------|
| Restating the title as the summary | Say what they measured or proved |
| "This paper is relevant to my research" | Name P1/P2/π and a specific task |
| Listing every author | First author et al.; bold colleagues only |
| Including Low-tier papers "for completeness" | Omit entirely |
| Long Moderate entries | Use compact template |
| Hallucinating σ(r) or f_NL constraints | Quote abstract or write "not stated" |

---

## After the digest

Offer: "Want a `paper-digestion` deep dive on any **Read now** paper?"

---

## Critical insights, program connections, and future work

The digest is not a literature alert — it is a **research steering document**. Every High-tier card must help Helen decide *what to do next*, not just *what was posted*. Read `RESEARCH_INTERESTS.md` (Research Identity + open questions) before writing connections; skim the three project pillars (P1 MAPs/DESI, P2 CMB B-mode Fisher, unified LSS×CMB) so links name **active threads**, not generic field labels.

### What "critical insights" means here

Go beyond paraphrase. For each High paper, deliver at least one of:

| Insight type | Example |
|--------------|---------|
| **Degeneracy / systematic** | "Bispectrum weakens DE evidence but pulls \(\sum m_\nu\) positive — opposite directions from the neutrino-mass paper in today's list." |
| **Method transfer** | "Their clustering-informed \(n(z)\) likelihood is copy-paste for MAP mock photo-\(z\) challenges." |
| **Tension with your stack** | "Limber bias exceeds your Fisher \(\sigma(r)\) degradation budget for Rubin-scale 3×2pt — check before joint DESI×imaging forecasts." |
| **Surprise / non-obvious** | "Configuration-space \(f_{\mathrm{NL}}\) with fixed \(p\) prior may be prior-dominated unless HMF \(p\) is folded in." |
| **Cross-paper link (same digest)** | "Pairs with `2606.23936`: bispectrum + PNG pipeline share mock covariance infrastructure." |

Put the sharpest version in **Insight**; put your evaluative take in **Critical comment**.

### Connections to current work — required depth

**Links to your program** must answer: *which active file, simulation, or open question?*

| Depth | Bad | Good |
|-------|-----|------|
| Generic | "Relevant to PNG work" | "Test whether MAP LRG×QSO joint \(f_{\mathrm{NL}}\) matches DESI DR1 interval when \(p_{\rm LRG}=1.0\pm0.1\)" |
| Generic | "Useful for Fisher forecasts" | "Compare their Limber bias table to your pixel Fisher F_rr degradation per operator before Rubin×DESI combo paper" |
| Generic | "Parity PNG" | "Forecast parity-odd trispectrum in SGWB using `2LPTPNG-ODD` ICs — they claim scale-dependent helicity is detectable" |

When a paper touches an open question from `RESEARCH_INTERESTS.md`, cite it by name in the **Open question** row (e.g. "f_NL–assembly-bias degeneracy with MAP catalogs", "σ(r) degradation per operator").

For **Moderate** tier: one **Connection** bullet must still name a concrete anchor; add **Pursue timing** only if `Near-term` or `Now (tandem)` — otherwise omit.

### Future work — actionable bullets

Each High card gets **1–2 bullets** in **Future work**. Format:

```
- **[Deliverable]:** [specific action] → [what you learn / what it unlocks]
```

Examples:

- **Mock comparison:** Run MAP LRG 2pcf through DESI PNG pipeline's universality relation with HMF-derived \(p\) vs. fixed Gaussian → quantify prior vs. physics sensitivity.
- **Code fork:** Port clustering-informed \(n(z)\) weighting from GalSBI into AbacusAurora light-cone validation for one DES Y3 footprint.
- **Forecast add-on:** Add parity-odd trispectrum SGWB template to existing PNG-sims Fisher notebook; compare to SKAO chapter detectability claim.
- **Collaboration ping:** Email Verde group re: bispectrum×PNG mock sharing for DR1/DR2 cross-covariance treatment.

Do **not** write vague futures ("explore further", "keep an eye on", "could be useful"). If you cannot name a deliverable, downgrade the paper to Moderate or omit.

### Pursue timing rubric

**This field is mandatory for every High-tier card.** It tells Helen whether to act *now*, *soon*, or *later*. Be honest — not every relevant paper is urgent.

| Label | Meaning | When to use |
|-------|---------|-------------|
| **`Now (tandem)`** | Pursue **in parallel with active work** — same codebase, same paper draft, same sim suite, or same collaborator thread already open | Paper supplies a benchmark, method, or dataset you need *this month*; gap blocks a current deliverable; direct extension of in-progress MAP/PNG/Fisher analysis |
| **`Near-term`** | Queue for **next 1–3 months** — new branch, side project, or proposal section; not blocking today but high leverage | Opens a clear new analysis on existing AbacusAurora/Quijote-PNG/Fisher infrastructure; timely DESI/Euclid/ACT data product; colleague overlap worth a meeting |
| **`Background`** | **Monitor** — cite later, read when cited, or revisit after current milestone | Review papers, theory without forward model, precursor survey (eBOSS) methods, white papers, results that need DR2+ before acting |

**Format (required):**

```markdown
**Pursue timing:** `Now (tandem)` — [one sentence: active thread + why now]
```

Examples:

- **`Now (tandem)`** — DESI DR1 \(f_{\mathrm{NL}}\) is the empirical target for your MAP PNG validation; run comparison before next group meeting.
- **`Now (tandem)`** — Roman/Rubin Limber bias table should feed directly into your joint 3×2pt Fisher — same scale cuts as your draft.
- **`Near-term`** — GalSBI image-level SBI after MAP v1 mocks ship; schedule after AbacusAurora light-cone cut.
- **`Background`** — eBOSS EFT multitracer prior trick is proven; revisit when DESI ELG×LRG EFT pipeline starts.

### Flag especially fruitful papers

In addition to per-card **Pursue timing**, use these digest-level signals when warranted:

#### 1. Priority reads today (top of report)

Reserve for papers with **`Now (tandem)`** only. Max 3. One line = active thread + immediate action.

#### 2. `⭐ Tandem opportunity` tag in At a glance table

Add a column or suffix when a paper is **`Now (tandem)`**:

```markdown
| High | [2606.24651](url) | DESI PNG f_NL | P1, π | Read now | ⭐ tandem |
```

#### 3. Themes today — call out tandem clusters

When 2+ papers reinforce the same active thread, say so explicitly:

```markdown
- **DESI / PNG (⭐ pursue in tandem):** `2606.24651` + `2606.23936` — joint bispectrum+PNG mock covariance is the natural next AbacusAurora validation target.
```

#### 4. End-of-digest **Suggested next steps** (optional block)

If ≥2 `Now (tandem)` papers, append after **Not reported**:

```markdown
## Suggested next steps
1. **[Thread name]:** [paper A] + [paper B] → [single concrete action this week]
2. ...
```

### Moderate tier — when to elevate pursuit language

Usually Moderate = compact card only. **Exception:** if a Moderate paper is **`Now (tandem)`** or **`Near-term`** with unusually high leverage, add two lines:

```markdown
**Pursue timing:** `Near-term` — [why]
**Future work:** One bullet with deliverable.
```

Do not promote to full High template unless the abstract supports it.

### Voice for comments and future work

- Write as a colleague who knows the MAP/PNG/Fisher stack, not as a neutral abstract bot.
- Prefer "you should compare X to Y" over "one could consider comparing."
- When uncertain, say so: "If their \(p\) prior is wrong for QSOs, your MAP QSO PNG forecast needs the same sensitivity test."
- Cross-reference other papers **in the same digest** when they reinforce or contradict each other.

### Quality checklist additions (future work & pursuit)

- [ ] Every High card has **Critical comment** (evaluative, not summary)
- [ ] Every High card has **Future work** with named deliverable(s)
- [ ] Every High card has **Pursue timing** with one-sentence justification
- [ ] ≥1 paper marked **`Now (tandem)`** when the list contains a direct hit on active P1/P2/π work
- [ ] **Priority reads** lists only `Now (tandem)` papers
- [ ] **Themes today** flags tandem clusters when 2+ papers share an active thread
- [ ] Connections cite `RESEARCH_INTERESTS.md` open questions by name when applicable
- [ ] No vague future-work bullets ("explore", "investigate further", "keep watching")
