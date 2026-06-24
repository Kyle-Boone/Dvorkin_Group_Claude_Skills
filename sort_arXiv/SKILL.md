---
name: sort_arXiv
description: Reads Prior_Knowledge papers to profile research interests, fetches recent astro-ph.CO and physics.data-an submissions from arXiv, scores each paper for personal relevance and cosmological importance, and outputs a ranked HTML report.
argument-hint: "[-h] [-days <N>]"
invocation: user
subagent-type: claude
allowed-tools: [Read, Write, Bash, WebFetch, Glob]
---

# sort_arXiv

Arguments: **$ARGUMENTS**

## Step 0: Parse Arguments

Check `$ARGUMENTS` for flags:

- If `-h` is present, print the following and stop:

```
NAME
    sort_arXiv — fetch, score, and rank recent arXiv papers by research relevance

SYNOPSIS
    /sort_arXiv [-h] [-days N]

DESCRIPTION
    Reads papers in ./Prior_Knowledge/ to build a profile of the user's research
    interests, then fetches recent submissions from astro-ph.CO and physics.data-an
    on arXiv. Each paper is scored on two dimensions:

      Relevance  — how interesting the user would likely find it based on prior work
      Importance — how significant it is to cosmology overall

    The top 20 papers by each score are compiled into an HTML report saved to
    ./Arxiv_Organized/<YYYY-MM-DD>.html.

OPTIONS
    -h          Print this help text and exit.
    -days N     Look back N weekdays (Mon–Fri only; arXiv has no weekend posts).
                Defaults to 5 if omitted.

EXAMPLES
    /sort_arXiv                 Fetch the past 5 weekdays of papers
    /sort_arXiv -days 10        Fetch the past 10 weekdays of papers
    /sort_arXiv -h              Show this help
```

- Parse `-days N` as integer LOOKBACK_DAYS. Default to 5 if absent.

## Step 1: Read Prior Knowledge

Use Glob to list all files in `./Prior_Knowledge/`. Read each file and build a
research profile of the user: topics, methods, datasets, recurring concepts,
and scientific questions they engage with. Hold this profile in mind for scoring.

## Step 2: Calculate Date Range

From today's date, count back LOOKBACK_DAYS weekdays (Mon–Fri; skip Sat/Sun).
That is the START date. TODAY is the END date. Format both as YYYYMMDD.

Example: today = 2026-06-18, LOOKBACK_DAYS = 5
  → count back: 6/17, 6/16, 6/13, 6/12, 6/11
  → START = 20260611, END = 20260618

## Step 3: Fetch Papers from arXiv

For each of the two categories, fetch via the arXiv API:

  https://export.arxiv.org/api/query?search_query=cat:{CATEGORY}+AND+submittedDate:[{START}0000+TO+{END}2359]&sortBy=submittedDate&sortOrder=descending&max_results=200

Categories: `astro-ph.CO`, then `physics.data-an`

Parse the Atom XML to extract per paper:
- arXiv ID
- Title
- Authors list
- Abstract
- Submission date
- URL: https://arxiv.org/abs/{id}

After both fetches, deduplicate by arXiv ID.

## Step 4: Score Each Paper

For every paper in the combined set, assign two integer scores (1–10):

**Relevance Score** — likelihood the user would find this interesting, based on Prior Knowledge.
- 10 = directly overlaps the user's methods/topics/datasets
- 5  = adjacent field, partial overlap
- 1  = unrelated to user's work

**Importance Score** — significance of this paper to cosmology broadly.
- 10 = landmark result, major new dataset/method, or addresses a fundamental open question
- 5  = solid contribution, moderate novelty
- 1  = incremental or highly niche

Score all papers before ranking.

## Step 5: Rank and Select

- Sort all papers by Relevance Score descending → Top-Relevance list (top 20)
- Sort all papers by Importance Score descending → Top-Importance list (top 20)
- A paper may appear on both lists; show it independently in each.

## Step 6: Generate HTML Report

Run `mkdir -p ./Arxiv_Organized` if the directory doesn't exist.

Write `./Arxiv_Organized/{TODAY}.html` (e.g., `2026-06-18.html`).

The page should:
- Use clean inline CSS — dark background (#1a1a2e), light text, readable sans-serif font
- Show a header: "arXiv Digest — {TODAY}" and subheader: "Papers from {START_FORMATTED} to {END_FORMATTED}"
- Have two sections with clear headings: "Top 20 by Personal Relevance" and "Top 20 by Cosmological Importance"
- Each paper entry includes:
  - Rank number and both scores displayed as badges (e.g. "Relevance: 9 | Importance: 7")
  - Title as a hyperlink to the arXiv page
  - Authors: first author + "et al." if more than 3 authors, otherwise all names
  - A 2–3 sentence plain-English summary of what the paper does and why it matters
  - arXiv ID shown as small muted text

After writing the file, report the path and total number of papers scored.
