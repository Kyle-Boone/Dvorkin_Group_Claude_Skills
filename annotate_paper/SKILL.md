---
name: annotate_paper
description: Downloads an arXiv paper's LaTeX source, reads Compressed_Knowledge to understand the user's background, produces both an original and a heavily annotated .tex file with inline blue explanations and assumption flags, and compiles both to PDF. Saved to ./Papers/.
argument-hint: "<arxiv-url> [-h]"
invocation: user
subagent-type: claude
model: opus
allowed-tools: [Read, Write, Bash, WebFetch, Glob]
---

# annotate_paper

Arguments: **$ARGUMENTS**

## Step 0: Parse Arguments

Check `$ARGUMENTS` for flags:

- If `-h` is present, print the following and stop:

```
NAME
    annotate_paper — annotate an arXiv paper with inline LaTeX explanations tailored to your background

SYNOPSIS
    /annotate_paper <arxiv-url> [-h]

DESCRIPTION
    Downloads the LaTeX source of an arXiv paper, reads your Compressed_Knowledge
    library to understand your background, then produces:
      - The original .tex source (compiled to PDF)
      - An annotated .tex with inline blue explanations, callout boxes,
        pedagogical links, and flagged physical assumptions (compiled to PDF)

    Annotations are aggressive: every concept with any ambiguity gets a note.
    Every physical assumption — stated or implicit — gets flagged.

OPTIONS
    -h          Print this help text and exit.

    arxiv-url   Full arXiv abstract URL, e.g.:
                https://arxiv.org/abs/2401.12345

OUTPUT
    ./Papers/<FirstAuthor>_<Year>_<ShortTitle>/
        <ShortTitle>.pdf               — compiled original
        <ShortTitle>_annotated.pdf     — compiled annotated
        source/                        — all source files, figures, build artifacts
            <ShortTitle>.tex
            <ShortTitle>_annotated.tex
            figures/, *.bib, *.cls, *.aux, *.log, etc.

EXAMPLES
    /annotate_paper https://arxiv.org/abs/2401.12345
    /annotate_paper -h
```

- Extract the arXiv ID from the URL. If none provided, ask for one.

## Step 1: Download the Paper

Fetch metadata via WebFetch on the abstract URL:
- Title, authors (full list), year, abstract

Download and extract the source:
```bash
mkdir -p $TMPDIR/annotate_src
curl -L "https://arxiv.org/e-print/{ID}" -o $TMPDIR/annotate_src/source
cd $TMPDIR/annotate_src
tar -xzf source 2>/dev/null || tar -xf source 2>/dev/null || gunzip -c source > main.tex 2>/dev/null
```

Identify the main .tex file (contains `\documentclass`). Follow all `\input`
and `\include` directives to understand the full document structure. Note the
location of any .bib files, figure files, and style files — these must all be
preserved.

## Step 2: Set Up Output Directory

```bash
mkdir -p "./Papers/{FirstAuthor}_{Year}_{ShortTitle}/source"
```

Copy the entire extracted source tree into the `source/` subdirectory. Name
the main tex file `{ShortTitle}.tex`. The top-level folder will only contain
the two final PDFs; all source, figures, bib files, style files, and build
artifacts stay in `source/`.

## Step 3: Read Prior Knowledge

Use Glob to list all files in `./Compressed_Knowledge/`. Read each one. Then produce
two explicit lists that you will carry through the rest of the skill:

**Known well** — methods, formalisms, datasets, statistics, and surveys the user
works with directly. Do NOT annotate these; skip them entirely unless there is a
genuinely non-obvious connection to this paper's approach.

**Adjacent / new** — topics mentioned in Prior_Knowledge only in passing, or not
present at all. Annotate these whenever they appear.

Keep these two lists in mind for every annotation decision in Step 5.

## Step 4: Prepare the Annotated .tex

Create `source/{ShortTitle}_annotated.tex` as a copy of the assembled source.

**Modify the preamble** — add these packages after `\documentclass` (or near
the top of the preamble, before `\begin{document}`):

```latex
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\usepackage{soul}

% Inline annotation — blue italic note
\newcommand{\annotation}[1]{{\color[HTML]{1565C0}\textit{\small$\triangleright$ #1}}}

% Assumption flag — amber bold inline
\newcommand{\assumption}[1]{{\color[HTML]{B45309}\textbf{[ASSUMPTION: }}}{\color[HTML]{B45309}#1}{\color[HTML]{B45309}\textbf{]}}}

% Callout box for longer context
% colupper (not fontupper \color) is used so the color persists across page/column breaks
\tcbuselibrary{skins,breakable}
\definecolor{annotcolor}{HTML}{1565C0}
\definecolor{pedagcolor}{HTML}{00695C}
\newtcolorbox{annotbox}{
  enhanced, breakable,
  colback=blue!4!white, colframe=blue!50!white,
  leftrule=3pt, rightrule=0pt, toprule=0pt, bottomrule=0pt,
  colupper=annotcolor,
  fontupper=\itshape\small,
  before upper={\textbf{$\triangleright$ Note:}\ }
}

% Research opportunity flag — green inline note (promising techniques or open problems worth pursuing)
\newcommand{\connection}[1]{{\color[HTML]{2E7D32}\itshape\small$\leftrightarrow$ #1}}

% Pedagogical link box
\newtcolorbox{pedagbox}{
  enhanced, breakable,
  colback=teal!4!white, colframe=teal!40!white,
  leftrule=3pt, rightrule=0pt, toprule=0pt, bottomrule=0pt,
  colupper=pedagcolor,
  fontupper=\itshape\small,
  before upper={\textbf{$\rightarrow$ Learn more:}\ }
}

% Paper-opening physical intuition overview
\newtcolorbox{overviewbox}{
  enhanced, breakable,
  colback=orange!6!white, colframe=orange!50!white,
  leftrule=3pt, rightrule=0pt, toprule=0pt, bottomrule=0pt,
  colupper=orange!70!black,
  fontupper=\itshape\small,
  before upper={\textbf{$\star$ Paper Overview:}\ }
}

% Cosmological parameter constraint explanation
\newtcolorbox{parambox}{
  enhanced, breakable,
  colback=violet!5!white, colframe=violet!40!white,
  leftrule=3pt, rightrule=0pt, toprule=0pt, bottomrule=0pt,
  colupper=violet!70!black,
  fontupper=\itshape\small,
  before upper={\textbf{$\Omega$ Why constrain this?}\ }
}
```

If the document uses a journal class that conflicts with tcolorbox (e.g.,
emulateapj, mnras), add `\PassOptionsToPackage{table}{xcolor}` before
`\documentclass` if needed, and use simpler colored text fallbacks if tcolorbox
causes conflicts.

## Step 5: Annotate

### Paper overview (do this first)

Insert the overview box **immediately before the first `\section{...}` command** — that is,
after all title-page commands (`\maketitle`, `\begin{abstract}...\end{abstract}`,
`\begin{keywords}...\end{keywords}`) and after the body-of-paper comment block, but
before the Introduction section heading. Do **not** place it before `\begin{abstract}` or
between `\begin{document}` and `\maketitle`: in two-column journal classes (mnras, aastex,
emulateapj, revtex) those locations are in a special single-column title-page context
where tcolorbox boxes overflow off the page.

```latex
\begin{overviewbox}
[Write 3–4 sentences targeting a cosmology grad student with Dodelson & Schmidt
fluency and familiarity with the user's own papers. Cover: (a) the core physical
question the paper asks and why it matters, (b) the observable or dataset it
exploits and the physical lever arm connecting data to inference, and (c) what
the reader should watch for as they proceed. Concise — orienting context, not a
summary.]
\end{overviewbox}

\section{Introduction}
```

Then work through the document section by section.

**Gating rule — apply before every annotation:**
Before adding any annotation, check your Known/Adjacent lists from Step 3.
- If the concept is on **Known well**: skip it entirely. Do not explain it.
- If the concept is on **Adjacent / new**: always annotate it.
- If uncertain: lean toward annotating, but keep the note brief.

**Known-in-a-new-context rule:** If a concept is on the "Known well" list but
appears in a novel combination, approximation regime, or dataset context that
differs meaningfully from how the user encounters it in their own work, annotate
the *difference or new application* — not the base concept. Example: if the user
knows power spectra but this paper applies them to an unusual field or with an
atypical approximation, annotate that specific departure.

**Over-gating check:** After completing all annotations, ask: does the annotated
file look roughly 25% longer than the original (e.g., ~5 extra pages for a
19-page paper)? If barely longer, re-examine the densest technical sections for
passages that were skipped and add annotations for the highest-opacity content.

**Use `\annotation{}` for inline notes (insert right after the relevant text):**
- Any acronym not standard in the user's subfield (skip well-known ones like
  CMB, SNR, MCMC, SNe Ia, etc. that appear in Prior_Knowledge)
- Any statistical or ML technique from the **Adjacent / new** list that gets a
  passing mention
- Any citation used as a fact without explanation ("as shown by X...")
- Any equation variable or symbol not defined nearby
- Implicit methodological choices that affect results but aren't called out by
  the authors

**Dense equation blocks — high priority target:**
When 2 or more equations appear in succession and introduce several new variables
or operators, add an `\begin{annotbox}` BEFORE the block with a 2–4 sentence
physical/intuitive explanation of what the block is computing and why. Then use
`\annotation{}` inline for individual symbols on first appearance. Do not skip
dense math — these are the highest-value annotation locations.

**Equation clarity test:** Before moving past any equation, ask: "If I
encountered this equation without the surrounding prose, would I immediately know
what physical quantity it computes and why?" If not, annotate it — even a single
equation with an unusual operator, approximation, or notation warrants at least
an inline `\annotation{}`. The trigger is opacity to the reader, not equation
count.

**Dense terminology paragraphs:**
When a paragraph introduces 3 or more unfamiliar terms or technique names
without explanation, add an `\begin{annotbox}` AFTER the paragraph summarizing
what family of methods these belong to and what they are collectively trying to
accomplish.

**Use `\begin{annotbox}...\end{annotbox}` for longer context:**
- A method or formalism central to the paper but not well-covered in
  Prior_Knowledge — give a 2–4 sentence explanation
- The "so what" of a major result — why does this matter for cosmology

**Use `\begin{pedagbox}...\end{pedagbox}` for deep topics:**
- When a topic (e.g., field-level inference, normalizing flows, emulators)
  would take multiple paragraphs to explain properly, don't. Write one sentence
  and cite a review:
  "This builds on [topic]. For a pedagogical treatment see [Author Year]
  (arXiv:XXXX.XXXXX)."
  Only cite arXiv IDs you are confident exist. If uncertain, describe what
  to search for.

**Use `\connection{}` for research opportunities — two triggers only:**
1. A technique or method in the paper that looks particularly promising to
   explore or adopt: briefly say why in one sentence.
2. An open problem or limitation the authors call out — "future work," a dropped
   assumption, a listed caveat — that could plausibly be a research project:
   say in one sentence what pursuing it would involve.

Never use `\connection{}` to point back at something the user already knows.
Prior_Knowledge informs what gets annotated; it does not appear in the PDF text.

**Use `\assumption{}` for ALL physical assumptions — leave none out:**
- Gaussianity of the likelihood or field
- Linearity (of perturbations, of the signal model, of systematics)
- Fiducial cosmology choices and why they matter
- Scale cuts and their physical motivation
- Flat-sky, Limber, or Born approximations
- Any survey-specific approximation (mask treatment, shape noise model, PSF)
- "We assume X for simplicity / to be explored in future work"
- Any place the authors marginalize over nuisance parameters that could absorb
  real physics

For assumptions that are especially load-bearing — ones where breaking them
would qualitatively change the result — add an `\begin{annotbox}` after the
`\assumption{}` explaining what would change.

**Cosmological parameter constraints:** If constraining cosmological parameters
is a primary stated goal of the paper (framed as such in the abstract or
introduction), identify which parameters are being constrained in the results.
For each distinct cosmological parameter (e.g., $\sigma_8$, $\Omega_m$, $w_0$,
$S_8$), add a `\begin{parambox}` at the first place it appears as a constrained
output (posterior, chain, or results table):

- What feature of this dataset is physically sensitive to this parameter?
- Why does varying the parameter change that observable (the physical mechanism)?
- What degeneracies exist and how does this analysis break them?

Keep each box to 3–4 sentences. Skip nuisance parameters, incidental
constraints, and internal priors. Only flag parameters the paper is explicitly
designed to measure.

## Step 6: Compile Both PDFs

**Check for pdflatex/latexmk:**
```bash
which latexmk || which pdflatex
```

**If neither is found, install LaTeX.** Work through these options in order
until one succeeds:

```bash
# Option 1: BasicTeX via Homebrew (minimal, ~100MB, adds packages on demand)
brew install --cask basictex && eval "$(/usr/libexec/path_helper)"

# Option 2: Full MacTeX via Homebrew (~4GB, everything included)
brew install --cask mactex && eval "$(/usr/libexec/path_helper)"

# Option 3: If brew itself is missing
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install --cask basictex && eval "$(/usr/libexec/path_helper)"
```

After installing BasicTeX, install latexmk:
```bash
sudo tlmgr update --self && sudo tlmgr install latexmk
```

**Compile the original:**
```bash
cd "./Papers/{FirstAuthor}_{Year}_{ShortTitle}/source"
latexmk -pdf -interaction=nonstopmode {ShortTitle}.tex 2>&1
```

**Compile the annotated version:**
```bash
latexmk -pdf -interaction=nonstopmode {ShortTitle}_annotated.tex 2>&1
```

**After successful compilation, copy the PDFs up to the parent folder:**
```bash
cp {ShortTitle}.pdf ../{ShortTitle}.pdf
cp {ShortTitle}_annotated.pdf ../{ShortTitle}_annotated.pdf
```

**If compilation fails due to missing packages**, parse the log for lines like
`! LaTeX Error: File 'X.sty' not found.` and install them:
```bash
sudo tlmgr install <package-name>
```
Then retry compilation. Repeat until the log is clean or no new missing
packages appear.

**If compilation fails for other reasons** (macro conflicts, journal class
issues, etc.):
- Read the error carefully and attempt a targeted fix in the .tex source
- Common fixes: add `\PassOptionsToPackage{table}{xcolor}` before
  `\documentclass`, remove conflicting options, replace a broken `\usepackage`
  with a compatible alternative
- Retry after each fix
- Keep trying until it compiles — this is a one-time setup problem and
  persistence here pays off for all future uses of this skill

## Step 7: Report

Tell the user:
- Paths to the two PDFs at the top level (e.g., `Papers/.../Paper.pdf` and `.../_annotated.pdf`)
- Compilation status (succeeded / failed + reason)
- Count of annotations by type (inline notes / callout boxes / pedagogical
  links / assumption flags / research opportunities / parameter boxes)
- Confirm: overview box written (1 expected); over-gating check performed and result
- A 3–5 sentence preview: the paper's main claim, the key methods used, and
  the most important assumptions flagged
