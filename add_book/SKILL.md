---
name: add_book
description: Convert a PDF textbook into per-chapter text files in ./Prior_Knowledge/ for faster future loading
argument-hint: "[pdf-path] [--chapters N-M]"
allowed-tools: Read, Write, Bash
invocation: user
---

## Overview

Given a path to a PDF textbook, extract and save the full text organized by chapter into
`./Prior_Knowledge/{BookName}/`. Future sessions load individual chapter .txt files (fast,
no PDF overhead) instead of re-processing the PDF each time. Run this once per book.

## Step 0: Parse Arguments

If args contain `-h` or `--help`, print the following and stop:

```
Usage: /add_book [pdf-path] [--chapters N-M]

Convert a PDF textbook into fast-loading per-chapter text files in ./Prior_Knowledge/.

Arguments:
  pdf-path          Path to the PDF file (absolute or relative)
  --chapters N-M    Only process chapters N through M (inclusive). Useful for
                    resuming after hitting a daily usage limit or processing in
                    batches. Chapters outside this range are skipped entirely.

Output:
  ./Prior_Knowledge/{BookName}/overview.md             Chapter index + summaries
  ./Prior_Knowledge/{BookName}/chapter_01_{Title}.txt  Per-chapter text files

Examples:
  /add_book ~/Books/Griffiths_QuantumMechanics.pdf
  /add_book ./textbooks/StatMech.pdf --chapters 6-10
  /add_book ./textbooks/StatMech.pdf --chapters 3-3
```

Parse `--chapters N-M` from the args if present. Store as `chapter_start` and `chapter_end` integers. If not provided, set both to `null` (process all chapters).

## Step 1: Read PDF Metadata and Table of Contents

Use the Read tool on the PDF with pages "1-20" to extract:
- **Title** and **Authors**
- **Table of Contents**: chapter titles and their starting page numbers

If the TOC is not found in pages 1-20, also check pages 1-5 and the last 5 pages.

## Step 2: Determine Chapter Boundaries

From the TOC, build a chapter list with start and end pages:
- End page of chapter N = start page of chapter N+1 minus 1
- For the final chapter, get the total page count via Bash:
  ```bash
  pdfinfo [pdf-path] | grep "^Pages:"
  ```
  Fall back to `mdls -name kMDItemNumberOfPages [pdf-path]` on macOS if pdfinfo is unavailable.

If `--chapters N-M` was provided, filter the chapter list to only include chapters N through M (inclusive). Tell the user upfront which chapters will be processed and which will be skipped.

## Step 2.5: Calibrate the PDF Page Offset

The TOC lists *book* page numbers, but the Read tool uses *PDF* page numbers. Front matter (cover, half-title, copyright, TOC, preface, etc.) creates a fixed offset between the two. Determine it before reading any chapter content.

**Procedure:**
1. From the TOC, take the first chapter that will be processed. Let its book start page be `P`.
2. Estimate a likely offset range. Most textbooks have 10–20 pages of front matter, so try `offset = 11` as a first guess.
3. Read **3 PDF pages** starting at `P + offset - 1` (i.e., pages `P+offset-1` through `P+offset+1`).
4. Check whether the chapter title heading and the printed page number `P` appear in those pages.
   - If yes: `pdf_page = book_page + offset` is confirmed.
   - If no: adjust by ±1–3 and re-read until the chapter title is found. Do not read more than ~5 pages per probe — each probe is cheap.
5. Record the confirmed `offset` value. All subsequent page calculations use `pdf_page = book_page + offset`.

This step costs at most 2–3 small reads and prevents reading the wrong pages for every chapter.

## Step 3: Generate Folder and File Names

- **Folder name**: CamelCase, no spaces or special characters, max 50 chars
  - e.g. `GriffithsIntroductionToQuantumMechanics`
- **Chapter filenames**: `chapter_{NN}_{CamelCaseTitle}.txt` (zero-padded number)
  - e.g. `chapter_03_TheFormalismOfQuantumMechanics.txt`

Create the output directory:
```bash
mkdir -p ./Prior_Knowledge/{BookName}
```

## Step 4: Extract and Save Each Chapter

**IMPORTANT — process one chapter at a time, sequentially. Never read multiple chapters in parallel.**

PDF pages are returned as images and consume far more context than plain text. Reading many chapters simultaneously fills the context window and causes failures. The correct pattern is: finish one chapter completely (all reads + write its file) before starting the next.

For each chapter in sequence:

1. Calculate `pdf_start = book_start + offset` and `pdf_end = book_end + offset`.
2. Read the chapter in sequential 20-page chunks (the Read tool maximum):
   - Chunk 1: pages `pdf_start` to `min(pdf_start+19, pdf_end)`
   - Chunk 2: pages `pdf_start+20` to `min(pdf_start+39, pdf_end)`
   - … and so on, **one chunk at a time** — do not issue parallel reads within a chapter.
3. After reading ALL chunks for this chapter, write the complete chapter file with this header:
   ```
   Chapter {N}: {Title}
   Pages {start}–{end}
   ─────────────────────────────────────────
   {extracted text}
   ```
4. **Write the file before moving to the next chapter.** Do not hold multiple chapters' content in context simultaneously.

Report progress to the user after each chapter file is written (e.g. "✓ Chapter 6 written (22 pages)").

**Do not read multiple chapters' page ranges in the same parallel batch.**

## Step 5: Create the Overview File

If `--chapters` was specified, skip this step entirely — don't overwrite or create `overview.md` for a partial run. The overview should only be written once all chapters are done.

Otherwise, write `./Prior_Knowledge/{BookName}/overview.md`:

```markdown
# {Book Title}
**Authors:** {authors}
**Source:** {original pdf path}
**Converted:** {today's date}

---

## Chapter Index

| # | Title | Pages | File |
|---|-------|-------|------|
| 1 | {Chapter Title} | {start}–{end} | chapter_01_{Title}.txt |
| 2 | ... | ... | ... |

---

## Chapter Summaries

### Chapter 1: {Title}
{2–3 sentence summary based on the extracted text}

### Chapter 2: {Title}
{2–3 sentence summary}

...
```

## Step 6: Confirm

Report to the user:
- Full path of the folder created
- Number of chapters extracted
- List of any chapters that failed extraction or had ambiguous page boundaries
- Remind the user: "Read ./Prior_Knowledge/{BookName}/overview.md to orient yourself, then load only the chapter files you need."
