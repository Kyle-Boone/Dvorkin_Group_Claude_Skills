# Examples — arXiv daily relevance digest

See [REPORT-GUIDE.md](REPORT-GUIDE.md) for full writing rules.

## Invocation

```
@arxiv-daily-relevance

Use digests/2026-06-24.raw.json in arxiv_scroll.
Write digests/2026-06-24.md following REPORT-GUIDE.md
```

## Example output (abbreviated but structurally complete)

```markdown
# arXiv Daily Digest — 2026-06-24

**Source:** https://arxiv.org/list/astro-ph/new  
**Raw data:** `digests/2026-06-24.raw.json` (fetched 2026-06-24T18:10:12Z)  
**Scanned:** 167 | **Relevant:** 5 (3 high · 2 mod) | **Criteria:** relevance-criteria.md

## Priority reads today

1. [2606.xxxxx](https://arxiv.org/abs/2606.xxxxx) — DESI ELG×LRG ξ systematics at z ~ 0.95: direct MAP/HOMe benchmark.
2. [2606.yyyyy](https://arxiv.org/abs/2606.yyyyy) — Fisher σ(r) with external delensing tracers: compare to Project 2 R^src plan.

## Themes today

- **DESI / galaxy–halo:** xxxxx — multi-tracer clustering; zzzzz — assembly bias in ELG hosts
- **CMB / delensing:** yyyyy — SO delensing forecast with LSS tracers
- **Methods:** vvvvv — differentiable EFT emulator for Stage IV nuisances

## At a glance

| Tier | ID | Title (short) | Tags | Action |
|------|-----|---------------|------|--------|
| High | [2606.xxxxx](url) | DESI ELG×LRG ξ DR2 | P1, U | Read now |
| High | [2606.yyyyy](url) | SO delensing Fisher | P2, U | Read now |
| High | [2606.zzzzz](url) | f_NL bispectrum + HMF | π, M | Skim |
| Mod | [2606.aaaaa](url) | PNG IC separable kernels | π | Watch |

## High relevance

### [DESI DR2 clustering of ELGs and LRGs in shared 0.8 < z < 1.1 window](https://arxiv.org/abs/2606.xxxxx) · `2606.xxxxx`

| Field | Content |
|-------|---------|
| **Authors** | Author et al.; **Hadzhiyska** |
| **Subjects** | Cosmology and Nongalactic Astrophysics (astro-ph.CO) |
| **Type** | data |
| **Tags** | P1, U |
| **Boosts** | survey · colleague |

**Bottom line:** New DESI multi-tracer clustering in the exact redshift window your MAP mocks target.

**What they did:** Measure ξ₀ and ξ₂ for ELG and LRG samples in the shared 0.8 < z < 1.1 window, including ELG×LRG cross-correlation, with explicit fiber-collision and FKP weight treatment.

**Main result:**
- Reports ~5–8% relative difference in small-scale ELG×LRG asymmetry vs previous HOD-based mocks (if stated in abstract — otherwise omit numbers)

**Links to your program:**

| Anchor | Connection |
|--------|------------|
| **P1** | Primary validation target for MAP-selected ELG/LRG catalogs vs HOMe |
| **Open question** | MAP vs HOMe validation; sub-Mpc residuals |

**Insight:** If they marginalize over HOD nuisance space rather than forward-modeling assembly bias, tension at r < 1 h⁻¹ Mpc may reflect model class—not DESI systematics alone.

**Caveat:** Abstract does not report conformity or orphan-satellite fractions; MAP-specific tests still needed.

**Action:** Read now — compare systematics table to your planned Y1 pipeline.

---

### [Fisher forecasts for Simons Observatory delensing with external galaxy tracers](https://arxiv.org/abs/2606.yyyyy) · `2606.yyyyy`

| Field | Content |
|-------|---------|
| **Authors** | Author et al. |
| **Type** | forecast |
| **Tags** | P2, U, M |
| **Boosts** | survey · inference |

**Bottom line:** Independent σ(r) degradation curve after delensing — benchmark for your pixel Fisher + R^src architecture.

**What they did:** Gaussian Fisher forecast for primordial B-mode recovery using SO noise model and external LSS delensing tracers at specified f_sky.

**Main result:**
- σ(r) = X×10⁻³ at fiducial r = 10⁻³ (only if in abstract)

**Links to your program:**

| Anchor | Connection |
|--------|------------|
| **P2** | Compare tier assumptions vs your Tier-3 pixel Fisher on B3 patch |
| **Unified** | Delensing tracer quality ties to AbacusAurora LSS maps for DESI×SO |

**Insight:** If they assume perfect E/B purification post-delensing, your zeroEE upper bound is the right sanity check on their quoted σ(r).

**Caveat:** Likely no mapmaking/reobservation matrix R — your operator-chain degradation is complementary, not redundant.

**Action:** Read now — extract delensing tracer assumptions for Project 2 medium-term plan.

## Moderate relevance

### [Separable bispectrum kernels for non-local PNG initial conditions](https://arxiv.org/abs/2606.aaaaa) · `2606.aaaaa`
**Tags:** π · **Type:** theory  
**Bottom line:** Extends SHMC12-class IC algorithm — monitor for AbacusAurora PNG embedding.  
**Connection:** **PNG-sims** — cross-check kernel choices in `2LPTPNG` vs any new template.  
**Action:** Watch

## Not reported

162 papers omitted (exoplanets, stellar, galactic, unrelated ML, or Low tier).
```

## Anti-patterns

- ❌ Summarizing every astro-ph paper on the list
- ❌ Moderate papers with full High-tier cards
- ❌ Claiming a connection without naming P1/P2/U/M/π
- ❌ Hallucinating abstract content
- ❌ Empty "Insight" that repeats the bottom line
