---
name: compress_knowledge
description: Summarize uncompressed papers and textbook chapters from Prior_Knowledge/ into Compressed_Knowledge/, preserving file structure, so future agents can load context cheaply.
author: kboone@g.harvard.edu
version: 1.0.0
agent: claude
model: opus
allowed-tools:
  - Read
  - Write
  - Bash
invocation: user
---

# compress_knowledge

You are compressing research knowledge for efficient future retrieval. Your job is to read unprocessed items from `./Prior_Knowledge/` and write concise summaries to `./Compressed_Knowledge/`, preserving the exact same folder/file structure. Summaries must be compact enough that a future agent can load many of them without exhausting its context window.

## Step 1: Inventory What Needs Compression

1. List all files and directories in `./Prior_Knowledge/` using Bash:
   ```
   find ./Prior_Knowledge -type f | sort
   find ./Prior_Knowledge -type d | sort
   ```
2. List all files already in `./Compressed_Knowledge/` (if it exists):
   ```
   find ./Compressed_Knowledge -type f 2>/dev/null | sort
   ```
3. Determine the mapping: for each source file `Prior_Knowledge/foo.txt` the expected compressed output is `Compressed_Knowledge/foo.md`. For a chapter `Prior_Knowledge/BookName/Chapter_1.txt` the output is `Compressed_Knowledge/BookName/Chapter_1.md`.
4. Build a list of items where the output file does **not** yet exist. These are the items to process. If everything is already compressed, report that and stop.

## Step 2: Compress Each Unprocessed Item

Process items one at a time. For each uncompressed source file:

1. Read the full source file.
2. Write a summary to the corresponding path under `Compressed_Knowledge/`, creating any needed subdirectories first (use `mkdir -p`).

### Summary Format

Use this markdown structure for every summary:

```
# [Title of Paper / Chapter]

**Source:** [original filename]

## Overview
[2–4 sentences: what this work is, why it matters, what problem it solves or what it teaches.]

## Key Ideas
[Bullet list of the central concepts, methods, or findings. Explain methods in plain language — describe what math/algorithms do conceptually, not the equations themselves. Aim for 5–10 bullets.]

## Main Results / Contributions
[2–4 sentences: the headline results, key conclusions, or what a reader would take away.]

## Context & Connections
[1–3 sentences: how this fits into the broader field, what it builds on, or what it enables.]
```

### Compression Guidelines

- **Target length:** 200–400 words per standalone paper; 150–300 words per textbook chapter.
- **No heavy math:** describe what equations accomplish, not the equations themselves. A phrase like "fits a power-law to the matter power spectrum" is better than writing out the formula.
- **Conceptual clarity over completeness:** a future agent needs to know what the work is about and whether to dig deeper, not every technical detail.
- **Preserve specificity:** include key named methods, observables, datasets, or results by name even if you don't explain them fully (e.g. "uses the Planck CMB likelihood", "applies a Gaussian process emulator").

## Step 3: Report

After processing, print a short summary:
- How many items were already compressed (skipped)
- How many new items were compressed
- List the newly created files
