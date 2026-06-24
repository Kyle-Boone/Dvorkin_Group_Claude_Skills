---
name: add_arxiv
description: Download the LaTeX source of an ArXiv paper and save it as a named text file in ./Prior_Knowledge/
argument-hint: "[arxiv-abstract-url] [-h]"
allowed-tools: [Bash, WebFetch, Write]
invocation: user
---

## Overview

Given an ArXiv abstract URL, fetch the paper's metadata and download its raw LaTeX source, then save it as a well-named `.txt` file in `./Prior_Knowledge/` in the current working directory.

## Step 0: Parse Arguments

If args contain `-h` or `--help`, print the following and stop:

```
Usage: /add_arxiv [arxiv-abstract-url]

Download the LaTeX source of an ArXiv paper into ./Prior_Knowledge/.

Arguments:
  url     ArXiv abstract page URL, e.g.:
          https://arxiv.org/abs/1706.03762

Options:
  -h, --help    Show this help and exit

Output:
  ./Prior_Knowledge/Author_Year_ShortTitle.txt

Example:
  /add_arxiv https://arxiv.org/abs/1706.03762
```

## Step 1: Extract the ArXiv ID

Parse the paper ID from the URL. For `https://arxiv.org/abs/1706.03762`, the ID is `1706.03762`.

## Step 2: Fetch Metadata

Use WebFetch on the abstract URL to extract:
- **Title**
- **Authors** (first author's last name for the filename)
- **Year** (from the submission date)
- **Abstract** (to include at the top of the saved file)

## Step 3: Download the LaTeX Source

Run:
```bash
mkdir -p /tmp/arxiv_{id}
curl -L "https://arxiv.org/e-print/{id}" -o /tmp/arxiv_{id}/source
cd /tmp/arxiv_{id}
tar -xzf source 2>/dev/null || gunzip -c source > main.tex 2>/dev/null
```

Then collect all `.tex` file content:
```bash
find /tmp/arxiv_{id} -name "*.tex" | sort | xargs cat
```

Use the concatenated `.tex` content as the body of the saved file.

## Step 4: Generate Filename

Format: `{FirstAuthorLastname}_{Year}_{CamelCaseTitle}.txt`

Example: `Vaswani_2017_AttentionIsAllYouNeed.txt`

Rules: no spaces, no special characters, max ~70 chars total.

## Step 5: Save the File

Write to `./Prior_Knowledge/{filename}`:
```
Title: {title}
Authors: {authors}
Source: {original url}
Retrieved: {today's date}
─────────────────────────────────────────
Abstract:
{abstract}

─────────────────────────────────────────
LaTeX Source:
{concatenated .tex content}
```

## Step 6: Confirm

Tell the user:
- Full path of the saved file
- Paper title and first author
- Flag if the TeX source was missing or extraction failed
