# How the agent accesses arXiv

This document explains **what actually happens** when you paste a daily arXiv link and invoke `@arxiv-daily-relevance`.

## What you provide

A **listing URL**, not a single paper. Typical forms:

| URL pattern | What it is |
|-------------|------------|
| `https://arxiv.org/list/astro-ph/new` | Today's new astro-ph submissions |
| `https://arxiv.org/list/astro-ph/new?skip=96&show=96` | Paginated slice (cross-lists, replacements) |
| `https://arxiv.org/list/hep-th/new` | Other categories (usually out of scope) |

The agent does **not** need your arXiv account. These pages are public HTML.

## Three access paths (in priority order)

### 1. Python fetch script (preferred)

```bash
python .cursor/skills/arxiv-daily-relevance/scripts/fetch_arxiv_list.py \
  "<LISTING_URL>" -o arxiv-digests/YYYY-MM-DD.raw.json
```

**How it works:**
- The agent runs this in the **Shell** tool with **network permission**
- `urllib.request` performs a normal HTTPS GET to `arxiv.org`
- HTML is parsed locally into structured JSON: `arxiv_id`, title, authors, subjects, comments, abstract

**Why preferred:** Structured output, reproducible, abstracts usually inline on listing pages, can be saved and re-triaged without re-fetching.

**Limits:**
- Depends on arXiv HTML layout (parser may need updates if arXiv changes markup)
- Very large lists (~200+ papers) produce large JSON — triage in batches
- arXiv asks for reasonable request rates; script fetches one listing page, then optional API batches for missing abstracts

### 2. arXiv Atom API (abstract backfill)

When listing HTML lacks an abstract, the script calls:

```
https://export.arxiv.org/api/query?id_list=ID1,ID2,...&max_results=N
```

**How it works:** Official arXiv API returns Atom XML with title, authors, abstract (`<summary>`). Batched in chunks of 50 IDs with a short delay between requests.

**Why used:** More reliable than scraping individual `/abs/` pages; same data the agent would get from WebFetch on abs URLs.

### 3. WebFetch / browser (fallback only)

| Tool | When used | Drawbacks |
|------|-----------|-----------|
| **WebFetch** | Script fails or user gives a single `/abs/` URL | Returns markdown, loses dt/dd structure; harder to parse 100+ papers |
| **cursor-ide-browser** | Debugging layout, verifying a paper page | Slow; overkill for daily digest |

The skill instructs the agent **not** to browse paper-by-paper unless the script fails or deep-reading one High-tier paper.

## Dedicated workspace: `arxiv_scroll/`

You can run everything from **`~/Documents/harvard-docs/cora-cosmology/journal-cosmology/arxiv_scroll/`** without `cd` into `assembly-bias-HOD`:

```bash
cd ~/Documents/harvard-docs/cora-cosmology/journal-cosmology/arxiv_scroll
./fetch.sh "https://arxiv.org/list/astro-ph/new"
```

- **Output:** `digests/YYYY-MM-DD.raw.json`
- **Config:** `paths.env` (absolute paths to skill script, relevance criteria, `RESEARCH_INTERESTS.md`)
- **Cursor:** Open `arxiv_scroll` as workspace; `@arxiv-daily-relevance` works via symlink in `.cursor/skills/`

See `arxiv_scroll/README.md` for full instructions.

## End-to-end data flow

```
Your mailer URL
      │
      ▼
arxiv_scroll/fetch.sh  (or fetch_arxiv_list.py via paths.env)
      │
      ▼
arxiv_scroll/digests/YYYY-MM-DD.raw.json
      │
      ▼
Agent triage (relevance-criteria.md + RESEARCH_INTERESTS.md)
      │
      ▼
arxiv_scroll/digests/YYYY-MM-DD.md
```

**Intermediate JSON is optional but recommended** when you say "save" — lets you re-run triage without hitting arXiv again.

## What the agent cannot do (without extra steps)

- **PDF full text** — not fetched by default; use `paper-digestion` on a downloaded PDF
- **Private / paywalled content** — arXiv is open; journal versions may differ
- **Real-time subscription** — you paste the link each day; no automatic cron (use Cursor Automations or `/loop` separately if desired)
- **Guaranteed completeness** if the mailer spans multiple `skip=` pages — agent must fetch **each URL you provide** or you provide the main `/new` link

## Network & sandbox

- Shell fetch requires `full_network` (or sandbox allowlist for arxiv.org)
- If a fetch fails with connection error, the agent retries with network permission or falls back to WebFetch
- No API key required for arXiv

## arXiv etiquette (embedded in script)

- Identifying `User-Agent` header
- API batches: ≤50 IDs per request, ~3s pause between batches
- One listing fetch per digest unless paginated URLs provided
