---
name: weekly_digest
description: Writes a compact, plain-language weekly digest of the biggest results in cosmology (5–8 topics), with extra attention to dark matter substructure, summary statistics and stellar streams when something notable appeared. Normally run automatically by ~/Claude/.weekly_digest/run.sh.
argument-hint: "[-h] [-papers <papers.json> -out <digest.json>]"
invocation: user
allowed-tools: [Read, Write, Bash, Glob]
---

# weekly_digest

Arguments: **$ARGUMENTS**

## Step 0: Parse Arguments

- If `-h` is present, print the following and stop:

```
NAME
    weekly_digest — plain-language weekly digest of the biggest cosmology results

SYNOPSIS
    /weekly_digest [-h] [-papers FILE -out FILE]

DESCRIPTION
    Reads the past week's astro-ph.CO papers (plus astro-ph.GA papers about
    streams and substructure), groups the biggest results into 5–8 topics, and
    writes each topic as linked takeaways with a short conversational overview,
    pedagogical reading and open research questions.

    This normally runs on its own once a week via launchd
    (~/Claude/.weekly_digest/run.sh), which fetches papers, calls this skill,
    checks every link against arXiv, and renders ./Weekly_Digest/<date>.html.

OPTIONS
    -h              Print this help text and exit.
    -papers FILE    JSON list of fetched papers (written by fetch.py).
    -out FILE       Where to write the digest JSON.

    With no options, runs the full pipeline now (same as run.sh --force).
```

- If `-papers` and `-out` are both given, continue to Step 1.
- If neither is given (a manual run), run
  `bash ~/Claude/.weekly_digest/run.sh --force` with Bash, tell the user where
  the report was written (or the error), and stop. Do not do Steps 1–4 yourself.

## Step 1: Read the papers

Read the `-papers` JSON file. Each entry has `id`, `title`, `authors`, `abstract`,
`date` and `categories`. Read every abstract before choosing anything.

## Step 2: Choose 5–8 topics

Group the papers into themes, then pick the 5–8 themes that matter most to the
field this week. Judge this by: major collaboration results, new datasets or
measurements, results bearing on big open questions (the Hubble tension, dark
energy, neutrino mass, the nature of dark matter, inflation), and things people
in the field will be talking about.

- If several notable papers share a theme, they go in the same topic.
- **Focus areas:** dark matter substructure (subhalos, dwarf galaxies, lensing
  perturbers), summary statistics (higher-order statistics, wavelets,
  simulation-based / field-level inference), and stellar streams. Give these a
  somewhat lower bar, but include them **only if something genuinely notable**
  came out. Never pad a topic, and never force a focus area in.
- Skip routine incremental papers, even if they are on-topic.

## Step 3: Write each topic

Audience: someone with general cosmology knowledge (expansion, CMB, dark matter,
dark energy, large-scale structure) but **no specialist knowledge of the
subfield**. Write conversationally, in plain English. Define any jargon in passing
or avoid it. No equations, and no unexplained acronyms beyond CMB, DESI, JWST
and the like (even then, say what the experiment is the first time).

For each topic:
- `heading`: a short, plain-English name for the area (e.g. "Measuring the Hubble constant").
- `takeaways`: one entry per notable paper (or per tightly linked paper pair):
  - `headline`: the takeaway as one sentence. This is the linked title in the
    report. State the result, not the paper's title.
  - `id`: the arXiv ID. It **must** come from the papers file.
  - `paragraph`: one paragraph (4–6 sentences) on what was done, how in broad
    strokes, and why it matters for the bigger picture.
- `learn_more`: 2–3 pedagogical reviews, lecture notes or classic introductions
  on arXiv for this area, as `{id, title, note}`. `note` is a few words on why
  it's a good entry point. Only list papers you are confident exist, with their
  exact titles. Every one is checked against arXiv afterwards, and any mismatch
  is dropped, so a wrong ID just wastes a slot.
- `open_questions`: 3–5 short bullets on open problems or active research
  directions in this area, phrased generally.

## Step 4: Write the digest JSON

Write the `-out` file with exactly this shape:

```json
{"topics": [
  {"heading": "...",
   "takeaways": [{"headline": "...", "id": "2610.12345", "paragraph": "..."}],
   "learn_more": [{"id": "1807.06209", "title": "...", "note": "..."}],
   "open_questions": ["...", "..."]}
]}
```

Order the topics from most to least significant. Write nothing else to disk. The
pipeline verifies the links and renders the HTML itself. Finish by printing
`DIGEST_JSON_WRITTEN`.
