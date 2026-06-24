# arxiv_scroll

Dedicated workspace for daily arXiv mailer triage. **You do not need to `cd` into `assembly-bias-HOD`.**

Research context and the agent skill still live in the main project; this folder holds **digests only** plus thin wrappers.

## Layout

```
arxiv_scroll/
├── README.md           ← you are here
├── paths.env           ← absolute paths to skill script + RESEARCH_INTERESTS.md
├── fetch.sh            ← one-command listing fetch
├── compile_digest.sh   ← compile digests/YYYY-MM-DD.tex → PDF
├── digests/            ← .raw.json, .md, .tex, .pdf
└── .cursor/skills/     ← symlinks to arxiv skills (for @ in this workspace)
```

## Quick start

### 1. Fetch today's listing

```bash
cd ~/Documents/harvard-docs/cora-cosmology/journal-cosmology/arxiv_scroll

./fetch.sh "https://arxiv.org/list/astro-ph/new"
```

Optional date label and API abstract backfill:

```bash
./fetch.sh "https://arxiv.org/list/astro-ph/new" 2026-06-24 --with-abstracts
```

Output: `digests/2026-06-24.raw.json`

### 2. Triage + report (Cursor agent)

Open **`arxiv_scroll`** as your Cursor workspace (or stay in any folder) and chat:

```
@arxiv-daily-relevance

Use digests/2026-06-24.raw.json in arxiv_scroll.
Relevance: paths.env → ARXIV_RELEVANCE_CRITERIA and RESEARCH_INTERESTS.
Write digests/2026-06-24.md following REPORT-GUIDE.md
```

### 2b. LaTeX PDF digest (color-coded, near-term opportunities)

```
@arxiv-digest-latex

Use digests/2026-06-24.raw.json
Write digests/2026-06-24.tex following REPORT-LATEX-GUIDE.md
Then: ./compile_digest.sh 2026-06-24
```

Produces a PDF with `fruitfulbox` / `pursuebox` highlighting **tandem research ideas**. See `assembly-bias-HOD/.cursor/skills/arxiv-digest-latex/REPORT-LATEX-GUIDE.md`.

### 3. Manual fetch (without wrapper)

```bash
source ~/Documents/harvard-docs/cora-cosmology/journal-cosmology/arxiv_scroll/paths.env

python3 "${ARXIV_FETCH_SCRIPT}" \
  "https://arxiv.org/list/astro-ph/new" \
  -o "${ARXIV_DIGESTS_DIR}/$(date +%Y-%m-%d).raw.json"
```

## Paths (edit `paths.env` if you move folders)

| Variable | Points to |
|----------|-----------|
| `ARXIV_FETCH_SCRIPT` | `assembly-bias-HOD/.cursor/skills/.../fetch_arxiv_list.py` |
| `ARXIV_RELEVANCE_CRITERIA` | `relevance-criteria.md` |
| `RESEARCH_INTERESTS` | `RESEARCH_INTERESTS.md` |
| `ARXIV_DIGESTS_DIR` | `arxiv_scroll/digests/` |
| `ARXIV_LATEX_TEMPLATE` | LaTeX digest skeleton |
| `ARXIV_LATEX_MACROS` | Color-coded annotation macros |

## Open this folder in Cursor

For `@arxiv-daily-relevance` and `@arxiv-digest-latex` when **only** this folder is open, symlinks under `.cursor/skills/` point to `assembly-bias-HOD`. Relevance rules read via `paths.env`.

## Paginated mailers

```bash
./fetch.sh "https://arxiv.org/list/astro-ph/new?skip=96&show=96" 2026-06-24-page2
```

Ask the agent to merge JSON files by `arxiv_id` before triage.

## See also

- `assembly-bias-HOD/.cursor/skills/arxiv-daily-relevance/ACCESS.md` — how HTTPS / API access works
