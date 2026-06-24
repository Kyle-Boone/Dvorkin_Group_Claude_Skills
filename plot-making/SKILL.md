---
name: scientific-journal-plots
description: >-
  Creates matplotlib/seaborn figures for scientific journal publications using
  serif fonts, inward ticks, muted palettes, and publication export settings.
  Use when making plots for papers, ApJ-style figures, matplotlib styling,
  seaborn charts, rcParams, or when the user references plot_style, plot_params,
  or PLOTTING_STYLE.
---

# Scientific Journal Plots (matplotlib / seaborn)

## Quick start

1. **Apply style first** — before any plotting calls.
2. **Default style: `fresco`** — serif, STIX math, inward ticks, no grid, 200 dpi export.
3. **Use named palette colors** — never raw matplotlib tab10 defaults unless encoding a documented convention.
4. **Save as PDF** (vector) for journal submission; PNG only for slides/previews.

```python
import sys
from pathlib import Path

# If scripts/ from this skill are on the path (or copied into the project):
from plot_style import apply_plot_style, palette_for

mod = apply_plot_style("fresco")   # or "legacy" for CMU+LaTeX look
PALETTE = palette_for("fresco")

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, color=PALETTE["blue"], lw=1.8, label="data")
ax.set(xlabel=r"$x$", ylabel=r"$f(x)$")
ax.legend(loc="best")
fig.savefig("figure.pdf")  # bbox=tight applied via rcParams
```

## Style selection

| Style | Module | When to use |
|-------|--------|-------------|
| `fresco` (default) | `plot_params_fresco.py` | Journal papers — DejaVu/STIX serif, no LaTeX engine required |
| `legacy` | `plot_params.py` | CMU Serif + `text.usetex=True`, larger tick labels (17.5 pt) |

```python
from plot_style import apply_plot_style

apply_plot_style()              # fresco, or PLOT_STYLE env var
apply_plot_style("legacy")      # explicit override
```

`apply_plot_style` calls `plt.rcdefaults()` first so switching styles in one session is safe.

## Workflow checklist

Copy and track when building a figure:

```
Plot progress:
- [ ] Style applied (fresco or legacy)
- [ ] figsize set explicitly (typical: 6×4 or 6×5 inches)
- [ ] Colors from PALETTE or documented survey/line palette
- [ ] Axis labels with math via $...$ where needed
- [ ] Legend: frameon=False (set by rcParams; don't override)
- [ ] No ax.grid() calls
- [ ] Annotated text uses path_effects halo if over busy background
- [ ] Saved at publication dpi (200 for fresco)
- [ ] Filename matches paper convention (e.g. fig3_sfrd.pdf)
```

## Hard rules (never break)

- **No grids** — `axes.grid = False`; do not call `ax.grid()`.
- **No legend frames** — `legend.frameon = False`.
- **Serif fonts only** — no sans-serif defaults.
- **Inward ticks on all four sides** — major + minor ticks visible.
- **No annotation bbox** — use `path_effects` halos instead of `bbox=dict(...)`.
- **Black marker edges** on scatter/error-bar points over dense backgrounds: `mec="k"`.

## Path effects for annotations

```python
from matplotlib import patheffects as pe

PE_DARK  = [pe.withStroke(linewidth=2.5, foreground="w")]  # dark text on busy bg
PE_LIGHT = [pe.withStroke(linewidth=2.5, foreground="k")]  # bright text on dark bg

ax.text(x, y, "label", color="black", path_effects=PE_DARK)
```

`PE_DARK` / `PE_LIGHT` are exported from `plot_params_fresco.py`.

## Common figure patterns

### Line plot with error bars (headline data)

```python
ax.errorbar(x, y, yerr=dy, fmt="o", ms=18, mew=2.0, capsize=4,
            color=PALETTE["blue"], ecolor=PALETTE["blue"], elinewidth=2.2,
            mec="k", zorder=20, label="This work")
```

### Multi-survey overlay (z-order)

```python
ZORDER_JADES    = 5
ZORDER_FRESCO   = 10
ZORDER_CONGRESS = 20   # CONGRESS on top
```

Survey colors when CONGRESS + FRESCO share axes: orange `#F97316`, blue `#3B82F6`, JADES `dimgrey`.

### Filter distinction by marker shape (not color)

- F356W → `marker="o"`
- F444W → `marker="s"`

### Seaborn usage

Seaborn is used only for palette extraction in legacy style (`sns.color_palette("Set1", 10, desat=0.7)`). Prefer matplotlib directly with fresco rcParams. If using seaborn axes-level functions, call `apply_plot_style()` first and pass explicit `color=PALETTE[...]` — do not rely on seaborn's default theme.

## Export

| Setting | fresco | legacy |
|---------|--------|--------|
| `savefig.dpi` | 200 | figure dpi (72) |
| `savefig.bbox` | tight | None |
| Preferred format | PDF | PDF |

```python
fig.savefig("output.pdf")                    # vector, preferred
fig.savefig("preview.png", dpi=200)          # raster preview only
```

## Bootstrapping in a new project

Copy these three files from this skill's `scripts/` directory into the project (or add `scripts/` to `PYTHONPATH`):

- `plot_style.py` — style loader
- `plot_params_fresco.py` — default journal style
- `plot_params.py` — legacy CMU+LaTeX style

## Adapting existing plots

When refactoring ad-hoc matplotlib code:

1. Add `apply_plot_style("fresco")` at top.
2. Replace hardcoded colors with `PALETTE[...]` or survey/line palette from reference.
3. Remove all `ax.grid()` calls.
4. Set `legend.frameon=False` if overridden.
5. Bump `savefig` to PDF at dpi 200.
6. Add `mec="k"` to markers on dense overlays.
7. Replace text `bbox=` with `path_effects=PE_DARK`.

## Additional resources

- Full palette tables, line-identity colors, marker size conventions: [reference.md](reference.md)
- Style module source: [scripts/](scripts/)
