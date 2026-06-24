### 1. Identify and Read the Paper

1. The user will typically point to a **folder** that contains:
   - One main `.tex` file (e.g. `main.tex`, `paper.tex`, or similar),
   - A compiled `.pdf` of the same paper (e.g. `main.pdf`),
   - Additional assets (figures in `.png`, `.jpg`, `.pdf`, `.svg`, etc.).

2. In that folder, identify the **main .tex file** by:
   - Preferring files with conventional names like `main.tex`, `paper.tex`, or `<project-name>.tex`, or
   - If multiple candidates exist, choosing the one that:
     - Includes `\begin{document}` and most of the paper’s sections, and
     - Is not clearly a small subfile (e.g. `supplement.tex`, `response.tex`, `macros.tex`).

3. Treat this main `.tex` file as the **source of truth**:
   - Read it fully (or in chunks if large).
   - Detect the title, authors, abstract, and major sections.

4. If a `.pdf` with the same base name exists in the folder (e.g. `main.tex` and `main.pdf`), optionally:
   - Skim it for figure/table captions and layout cues.
   - Use it only to disambiguate or clarify content from the `.tex`.

5. at the start of the .md file, include a table of contents-styled list of sections and brief description of what is covered in each section

6. For each **results section** (sections that report empirical findings, model fits, or numerical outcomes—typically not intro, methods-only, or appendices): include a **summary of key results** and **surprising or important findings**. Structure this as a subsection (e.g. "Key Results and Surprising Findings by Results Section") with one block per results section. For each block: list 3–7 bullet points under "Key results" and 1–4 bullet points under "Surprising findings" (or equivalent). This helps readers quickly grasp what each part of the paper establishes and what stands out. For each section, provide detailed summaries of the main ideas and thorough review of key concepts with helpful guiding questions to test understanding. then explore future directions and potential improvements.

Paper Summary Document Structure
0. Metadata

Title

Authors

Date (if available)

Field / Subfield (inferred)

One-sentence paper contribution

1. Executive Summary (1–2 pages max)

What problem is being solved?

Why does it matter?

What is new?

What are the main results?

Who should care?

This makes the agent useful to busy researchers.

2. Structured Table of Contents Overview

For each section:

Section X: Title

3–6 bullet summary of what it covers

What role it plays in the argument

3. Deep Section-by-Section Analysis

For each section:

A. Core Ideas

Detailed explanation

Reformulation in plain language

Any equations explained conceptually

B. Key Concepts

Definitions

Assumptions

Technical mechanisms

C. Guiding Questions

What assumptions are critical?

What would break this argument?

How does this connect to previous work?

What is implicitly assumed?

This transforms the output from “summary” to “research training tool.”

4. Key Results and Surprising Findings (Results Sections Only)

For each results section:

Section X: [Title]

Key Results

3–7 concrete findings

Include numbers when possible

State effect sizes, constraints, comparisons

Surprising / Important Findings

1–4 bullets

Unexpected trends

Tensions with prior work

Theoretical implications

Scaling behavior

This is good in your version — keep it.

5. Methodological Evaluation

Add this — it’s extremely valuable:

What are the strengths?

What are the hidden assumptions?

What are possible systematic issues?

What validation tests were performed?

Are there ablation studies?

This makes the agent feel like a serious research assistant.

6. Limitations

What cannot be concluded?

What uncertainties dominate?

Where is the model fragile?

What future data would matter most?

7. Future Directions and Extensions

Split into:

A. Natural Follow-Ups

Obvious next experiments

Extensions of method

B. Ambitious Directions

Theoretical generalizations

Cross-field applications

C. Potential Improvements

Computational

Statistical

Experimental

III. Improve Results Detection

You currently define results sections as:

sections that report empirical findings

Make this more robust.

Have the agent detect sections that contain:

Words like: “Results”, “Constraints”, “Measurements”, “Performance”, “Evaluation”, “Experiments”

Tables of fit parameters

Error bars

Phrases like “we find”, “we measure”, “we obtain”

If uncertain, classify as:

Conceptual

Methodological

Results

Discussion

This classification improves downstream structure.

IV. Make It Adaptive to Field (Important for You)

Given your background (CMB, DESI, large-scale structure):

If the paper is about cosmology / physics, additionally do this:

Explicitly summarize:

Parameter constraints

Priors

Likelihood construction

Covariance modeling

Systematics treatment

Comparison to Planck / DESI / etc.

If ML paper, additionally do this:

Dataset

Loss function

Baselines

Ablations

Scaling laws

The skill improves dramatically when summaries are field-aware.

V. Add a “Reconstruction of the Argument”

One powerful addition:

Include a section:

Logical Flow of the Paper

What is assumed?

What is derived?

What is demonstrated?

What depends on what?

Represent as a dependency chain:

Problem → Model → Estimator → Validation → Results → Interpretation

This forces deep structural understanding.

VI. Add Quality-Control Steps for the Agent

To improve performance, embed self-checks:

Before finishing, the agent should internally verify:

Did I identify all major sections?

Did I expand all \input files?

Did I summarize every results section?

Did I include numbers where possible?

Did I distinguish claims from evidence?

Did I avoid hallucinating content not present?

This dramatically reduces shallow summaries.