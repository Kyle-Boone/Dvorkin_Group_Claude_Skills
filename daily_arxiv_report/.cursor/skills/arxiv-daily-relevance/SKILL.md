---
name: arxiv-daily-relevance
description: >-
  Fetches a daily arXiv listing URL, filters papers for relevance to Helen Shao's
  LSS×CMB research program (RESEARCH_INTERESTS.md), and reports summaries,
  insights, and project connections. Use when the user provides an arXiv list/mailer
  link, asks for a daily paper digest, arXiv scan, or what's new and relevant
  in astro-ph for their research.
---

# arXiv Daily Relevance Digest

Filter a **daily arXiv listing** (user-provided URL) down to papers relevant to the research program in `RESEARCH_INTERESTS.md`. Report **only relevant papers** with summaries and connections to Project 1 (MAPs/DESI), Project 2 (CMB B-mode Fisher), and the unified LSS×CMB program.

## Quick start

User provides today's arXiv link, e.g.:
- `https://arxiv.org/list/astro-ph/new`
- A mailer URL with `skip` / `show` parameters

```
@arxiv-daily-relevance

Today's link: <URL>
```

Optional: `Save to digests/YYYY-MM-DD.md` (and raw JSON — see Step 2)

## Working directory

Default output paths assume the dedicated workspace:

**`~/Documents/harvard-docs/cora-cosmology/journal-cosmology/arxiv_scroll/`** — use `fetch.sh` and `digests/` here.

If the user works from `arxiv_scroll/`, read paths from `arxiv_scroll/paths.env`:

| Variable | Purpose |
|----------|---------|
| `ARXIV_DIGESTS_DIR` | `digests/YYYY-MM-DD.raw.json` and `.md` |
| `ARXIV_FETCH_SCRIPT` | Python listing fetcher |
| `ARXIV_RELEVANCE_CRITERIA` | Filter rules |
| `RESEARCH_INTERESTS` | Connection paragraphs |

When cwd is `assembly-bias-HOD`, `arxiv-digests/` is still valid; prefer `arxiv_scroll/digests/` if the user says they use the dedicated folder.

## How arXiv access works

See [ACCESS.md](ACCESS.md) for the full picture. Short version:

1. You paste a **public listing URL** (`arxiv.org/list/...`) — no login.
2. The agent runs `fetch_arxiv_list.py` via **Shell + network** — a normal HTTPS GET, HTML parsed to JSON.
3. Missing abstracts are backfilled via the **arXiv Atom API** (`export.arxiv.org/api/query`), not by opening 100 browser tabs.
4. **WebFetch / browser** are fallbacks only if the script fails.

The agent does **not** read PDFs or invent abstracts. Everything in the digest must come from fetched JSON.

## Workflow

Copy and track progress:

```
Digest progress:
- [ ] Step 1: Load research context
- [ ] Step 2: Fetch listing
- [ ] Step 3: Triage all papers
- [ ] Step 4: Deep-read relevant papers
- [ ] Step 5: Write digest report
- [ ] Step 6: Save file (if requested)
```

### Step 1: Load research context

1. Read [relevance-criteria.md](relevance-criteria.md) — filtering rules and tags.
2. Skim `RESEARCH_INTERESTS.md` (Research Identity + open questions) when writing connection paragraphs.
3. Do **not** dump the full master doc into the report.

### Step 2: Fetch listing

**Always run the fetch script first** (do not WebFetch the listing page for triage).

From **`arxiv_scroll/`** (recommended):

```bash
cd ~/Documents/harvard-docs/cora-cosmology/journal-cosmology/arxiv_scroll
./fetch.sh "https://arxiv.org/list/astro-ph/new"
# → digests/YYYY-MM-DD.raw.json
```

Or manually:

```bash
source ~/Documents/harvard-docs/cora-cosmology/journal-cosmology/arxiv_scroll/paths.env
python3 "${ARXIV_FETCH_SCRIPT}" "<ARXIV_LIST_URL>" -o "${ARXIV_DIGESTS_DIR}/YYYY-MM-DD.raw.json"
```

From **`assembly-bias-HOD/`** (legacy):

```bash
python3 .cursor/skills/arxiv-daily-relevance/scripts/fetch_arxiv_list.py \
  "<ARXIV_LIST_URL>" -o arxiv-digests/YYYY-MM-DD.raw.json
```

Requires **network** permission. The listing HTML usually includes abstracts inline. Add `--with-abstracts` only if `abstracts_missing` > 0 in the JSON metadata.

**Paginated mailers:** If the user provides multiple URLs (`skip=0`, `skip=96`, …), fetch each and merge JSON (dedupe by `arxiv_id`).

**If script fails:** Fall back to WebFetch on the listing URL, parse manually, or ask the user to retry. Document the failure in the digest header.

Do **not** proceed to triage without structured paper metadata for the full list.

### Step 3: Triage (relevance filter)

Read papers from the **saved JSON**, not from memory of the listing page.

For **every** paper in `papers[]`:

1. Check title, subjects, comments against [relevance-criteria.md](relevance-criteria.md).
2. Assign tags: `P1`, `P2`, `U`, `M`, `π` (see criteria file).
3. Assign tier: **High** / **Moderate** / **Low**.
4. Apply **priority boosts** (survey / inference / π / colleague) per [relevance-criteria.md](relevance-criteria.md) — may promote Moderate → High.
5. **Low → skip entirely** (do not mention in report).
6. For High/Moderate with empty `abstract`, run script with `--with-abstracts` or fetch that one abs page — **never guess from title alone**.

**Batching large lists:** Triage in chunks of ~50 papers from JSON; accumulate High/Moderate into the final report.

**Hard rule:** If zero papers pass, say so briefly. Do not pad with loosely related papers.

**Theory-only cosmology:** Include at Moderate by default if on-pillar; do not require a forward model.

### Step 4: Deep-read relevant papers (High tier only)

For **High** tier only (Moderate stays abstract-level unless user asks):
- Use `abstract`, `comments`, and `subjects` from JSON first.
- Optional: WebFetch one `abs_url` for journal ref / code links not in listing.
- Do **not** download PDF unless user asks.
- Extract: main claim, methods, datasets/surveys, key numbers **only if stated in abstract**.

### Step 5: Write digest report

**Follow [REPORT-GUIDE.md](REPORT-GUIDE.md)** — required structure, card templates, voice, and quality checklist.

Minimum sections: **Priority reads** (if ≥2 High), **Themes today**, **At a glance** table, **High** (full cards), **Moderate** (compact cards), **Not reported**.

High-tier card must include: **Bottom line**, **What they did**, **Main result**, **Links to your program** (concrete anchor table), **Insight**, **Critical comment**, **Future work**, **Pursue timing** (`Now (tandem)` · `Near-term` · `Background`), **Caveat**, **Action**. See REPORT-GUIDE.md for pursuit rubric and tandem flagging.

Do not use the old bullet-only format. See [examples.md](examples.md) for a complete sample.

### Step 6: Save (optional)

If user requests a file or says "save", write **both** to their digest dir:

```
arxiv_scroll/digests/YYYY-MM-DD.raw.json   # from Step 2
arxiv_scroll/digests/YYYY-MM-DD.md         # relevance digest
```

(`assembly-bias-HOD/arxiv-digests/` if user explicitly uses that project folder.)

## Relevance rules (summary)

| Include | Exclude |
|---------|---------|
| DESI, ACT, SO, Euclid, CMB, LSS, galaxy–halo, MAP/HOD, EFT, SBI, PNG, neutrinos, delensing, B-modes; **theory-only cosmology** on these topics | Exoplanets, stellar, unrelated ML, particle theory with no cosmology angle |

**Boost to High:** inference methodology, Stage IV survey hook, PNG/neutrino/inflation/parity-PNG (π), PNG IC simulation papers, colleague overlap.

Full rules: [relevance-criteria.md](relevance-criteria.md)

## Quality checks

Before delivering (see [REPORT-GUIDE.md](REPORT-GUIDE.md) checklist):

- [ ] High cards use full template (Bottom line → Action, including Critical comment, Future work, Pursue timing); Moderate uses compact template only
- [ ] **Pursue timing** set on every High card; ≥1 **`Now (tandem)`** when list warrants it
- [ ] **Future work** bullets name deliverables, not vague "explore further"
- [ ] **Insight** is non-obvious; **Caveat** present for each High paper
- [ ] **Links** name concrete anchors (MAP, AbacusAurora, PNG-sims, Fisher, open question #)
- [ ] Every reported paper has tags (P1/P2/U/M/π); colleague authors **bolded**
- [ ] No fabricated numbers or survey claims
- [ ] Scanned vs relevant counts stated; Themes match included papers only
- [ ] Low-tier papers omitted entirely

## Relationship to other skills

- **This skill:** daily **list** triage → markdown digest ([REPORT-GUIDE.md](REPORT-GUIDE.md))
- **@arxiv-digest-latex:** same triage → **LaTeX PDF** with color boxes + near-term pursue section ([REPORT-LATEX-GUIDE.md](../arxiv-digest-latex/REPORT-LATEX-GUIDE.md))
- **annotate_paper** / **annotated_paper.md:** full single-paper LaTeX source annotation
- **paper-digestion:** deep dive on one paper folder

## Additional resources

- [REPORT-GUIDE.md](REPORT-GUIDE.md) — **how to write the digest** (cards, voice, cosmology extras)
- [ACCESS.md](ACCESS.md) — how the agent reaches arXiv (script, API, fallbacks)
- [relevance-criteria.md](relevance-criteria.md) — tags, keywords, exclusions, colleague list
- [examples.md](examples.md) — sample invocation and full structural example
