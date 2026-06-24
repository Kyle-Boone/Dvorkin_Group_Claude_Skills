# Digests

Daily fetch + report files live here when you work from `arxiv_scroll/`.

| File | Description |
|------|-------------|
| `YYYY-MM-DD.raw.json` | Full listing fetch |
| `YYYY-MM-DD.md` | Markdown digest — `REPORT-GUIDE.md` |
| `YYYY-MM-DD.tex` + `.pdf` | LaTeX digest — `REPORT-LATEX-GUIDE.md`, compile via `../compile_digest.sh` |

Fetch:

```bash
cd ~/Documents/harvard-docs/cora-cosmology/journal-cosmology/arxiv_scroll
./fetch.sh "https://arxiv.org/list/astro-ph/new"
```
