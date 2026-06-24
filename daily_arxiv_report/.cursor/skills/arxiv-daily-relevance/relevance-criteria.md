# Relevance criteria — Helen Shao research program

**Master reference:** `RESEARCH_INTERESTS.md` in the repository root. Read it when criteria are ambiguous or when writing deep connection paragraphs.

## Report only if relevant

Include a paper in the digest **only** if it plausibly connects to at least one pillar below. When in doubt at triage, fetch the abstract; if still borderline, omit.

## Three pillars + unified program

| Tag | Pillar | Include when paper touches |
|-----|--------|------------------------------|
| **P1** | AbacusAurora + MAPs + DESI | Galaxy–halo connection, HOD/HOMe/assembly bias, MAPs, Abacus/AbacusSummit/Aurora, DESI ELG/LRG/BGS/QSO clustering, multi-tracer, conformity, fiber collisions, mock catalogs, sub-Mpc clustering, merger trees |
| **P2** | CMB B-mode Fisher | Primordial B-modes, tensor-to-scalar ratio **r**, E/B separation, delensing, BICEP/Keck/SO B-modes, pixel Fisher, mode loss, mapmaking/reobservation matrix, CMB polarization systematics |
| **U** | Unified LSS×CMB | Multi-probe cosmology, DESI×ACT/SO/Euclid joint analyses, galaxy×CMB lensing, kSZ, CMB lensing × LSS, neutrino mass from combined probes, consistent forward models across probes |
| **M** | Methods | EFT of LSS, EFTofLSS, simulation-based priors (SBP), bispectrum / beyond-2pt / marked statistics, field-level inference, SBI/GNN/emulators, differentiable cosmology, mock covariances, Fisher forecasts |
| **π** | Primordial physics | PNG / f_NL (local, equilateral, orthogonal), inflation, neutrino cosmology, scale-dependent bias; **parity-violating / parity-odd PNG**; **PNG IC generation in N-body sims** (SHMC12, Quijote-PNG, 2LPTPNG) |

A paper may carry multiple tags (e.g. `P1, π` or `U, P2, M, π`).

## PNG & parity-violating signals (high priority within π)

**Companion codebase:** `/Users/Shao/Downloads/daniel/PNG-sims` (also referenced in `RESEARCH_INTERESTS.md` §3A)

| Topic | Include when paper touches | Code / paper anchor |
|-------|---------------------------|---------------------|
| **PNG IC simulation** | Separable bispectrum kernels, 2LPT PNG ICs, non-local PNG, initial condition generators | Scoccimarro+12 (SHMC12); `2LPTPNG`; Quijote-PNG (Coulton et al.) |
| **PNG shapes** | Local f_NL, equilateral, orthogonal (CMB/LSS), folded, generic non-local templates | Quijote-PNG §2; SHMC12 §2 |
| **Scale-dependent bias** | b_φ(k), peak-background split, f_NL–assembly-bias degeneracy, HMF information content | SHMC12 §3; [2305.10597](https://arxiv.org/abs/2305.10597); AbacusPNG |
| **Parity-violating PNG** | Parity-odd trispectrum, parity-violating non-Gaussianity, Chern-Simons, birefringence, odd bispectrum/trispectrum | `2LPTPNG-ODD` (`PAR_ODD_FNL`) |
| **PNG inference** | Matter/galaxy bispectrum, Fisher forecasts for f_NL, field-level PNG, CMB bispectrum constraints | Quijote-PNG §6–7; Philcox/Verde DESI PNG |

**Auto-boost to High** (if on-topic): papers that extend or validate PNG IC algorithms, report new parity-violating observables with simulation forecasts, or address f_NL–bias degeneracies with methods you use (HMF, multi-tracer, beyond-2pt).

## High-signal keywords (title / abstract / subjects)

**Surveys & data:** DESI, Euclid, LSST/Rubin, ACT, Simons Observatory, CMB-S4, Planck, SDSS, BOSS, eBOSS

**LSS & galaxies:** large-scale structure, galaxy clustering, BAO, RSD, galaxy bias, halo occupation, assembly bias, conformity, ELG, LRG, emission-line galaxy, photometric/redshift-space distortion

**CMB:** cosmic microwave background, CMB lensing, B-mode, E-mode, polarization, delensing, Sunyaev-Zeldovich, kSZ, tSZ

**Sims & mocks:** N-body, Abacus, Quijote, **Quijote-PNG**, CAMELS, IllustrisTNG, mock catalog, light-cone, **2LPT PNG ICs**, separable bispectrum kernel

**PNG & parity:** primordial non-Gaussianity, f_NL, g_NL, bispectrum, trispectrum, scale-dependent bias, b_φ, peak-background split, **parity-odd**, **parity-violating**, Chern-Simons, birefringence, non-local PNG, equilateral, orthogonal PNG

**Inference:** effective field theory, EFTofLSS, Fisher matrix, MCMC, simulation-based inference, symbolic regression, normalizing flow

## Priority boosts (tier promotion)

Apply **after** initial tier assignment. Multiple boosts can promote Moderate → High.

| Boost | Promote when paper has… |
|-------|-------------------------|
| **Survey hook** | Explicit Stage IV target: DESI, Euclid, LSST/Rubin, ACT, Simons Observatory, CMB-S4, or forecast/constraints framed for near-term data |
| **Inference hook** | Likelihood, Fisher, MCMC, EFT pipeline, SBI, emulator, covariance, systematic marginalization, or observational analysis methodology |
| **π hook** | PNG / f_NL (any shape), **parity-violating / parity-odd PNG**, neutrino mass or hierarchy, inflation (**r**, primordial B-modes), scale-dependent bias, **PNG IC simulation** |
| **Colleague overlap** | Author overlap with §15–18 network (see list below) |

**Theory-only cosmology:** Papers with **no forward model** (no mocks, sims, or data pipeline) are **still eligible**. Default tier is **Moderate** if the topic fits a pillar (especially **π**). Promote to **High** if any boost above applies, or if the theory directly addresses an open question in `RESEARCH_INTERESTS.md`.

## Colleague overlap (boost priority; not limited to this list)

Papers by or clearly building on work from: Villaescusa-Navarro, Spergel, Verde, Wandelt, Philcox, Chen, Ivanov, Seljak, Ruiz-Zapatero, Sherwin, Lizancos, Guachalla, Hadzhiyska, Wechsler, Farren, Hill, Sabyr, Fabbian, Eisenstein, Johnson (MAP), Garrison (Abacus), **Coulton, Scoccimarro, Jung, Jamieson** (Quijote-PNG / PNG ICs).

Mark these with **Colleague overlap** in the report.

## Relevance tiers

| Tier | Criteria | Report depth |
|------|----------|--------------|
| **High** | Directly advances P1, P2, or a stated open question; **or** theory/inference paper with survey, inference, or π boost | Full entry: summary, connections, insights, suggested action |
| **Moderate** | Adjacent method or survey context; **theory-only cosmology** on-program without boosts; useful to monitor | Shorter entry: 2–3 sentence summary + one connection bullet |
| **Low** | Weak keyword match only; cosmology topic but no clear pillar link | **Omit** from digest |

## Exclude (do not report)

- Stellar, exoplanet, solar, planetary, most galactic structure (unless explicit LSS/CMB tracer link)
- Pure high-energy / particle theory without cosmological observables
- Black-hole / GR bursts unless CMB/LSS cosmology connection
- Machine learning on unrelated domains

**Not excluded:** Cosmology papers that are exclusively theory (no forward model, no data analysis) — include when they touch LSS, CMB, dark matter, growth, or primordial physics pillars.

## Connection prompts (use when writing entries)

For each included paper, answer where applicable:

1. **Which project?** P1 / P2 / Unified / Prior (CAMELS, neutrino paper, **PNG-sims / Quijote-PNG**)
2. **Forward model, theory, or inference?** Mocks/covariances, pure theory, or analysis methodology?
3. **Boosts?** Survey hook / inference hook / π hook / colleague overlap?
4. **Degeneracy / systematic?** Does it address a bottleneck named in `RESEARCH_INTERESTS.md`?
5. **Method transfer?** EFT, beyond-2pt, ML, Fisher, MCMC — applicable to your stack?
6. **Collaboration?** Overlap with §15–18 colleagues?
7. **Action?** Read now / skim / add to watch list / potential citation

## Open questions to watch (from master doc)

- MAP vs HOMe validation; sub-Mpc residuals
- f_NL–assembly-bias degeneracy with MAP catalogs
- PNG IC validation: `2LPTPNG` / `2LPTPNG-ODD` → AbacusAurora embedding
- Parity-odd trispectrum observables and bias modeling (PBS / MAP)
- σ(r) degradation per operator; delensing + Π_B recovery
- Beyond-2pt for bias degeneracy breaking in galaxy×CMB cross-correlations
- Joint EFT + Fisher + SBI on one AbacusAurora suite
