# Scientific Journal Plots — Reference

## Fresco palette (default prop cycle)

| Name | Hex | Use |
|------|-----|-----|
| blue | `#2E5C8A` | Primary trace |
| orange | `#E08214` | Secondary trace |
| grey | `#7A7A7A` | Tertiary / reference |
| green | `#2E8B57` | Fourth series |
| purple | `#7A4B8A` | Fifth series |
| lblue | `#7FA8C9` | Light accent |
| lorange | `#F2B66D` | Light accent |
| dark | `#222222` | Axes, labels, edges |

## Legacy palette (seaborn Set1, desat=0.7)

| Name | Hex |
|------|-----|
| blue | `#377EB8` |
| orange | `#FF7F00` |
| grey | `#999999` |
| green | `#4DAF4A` |
| purple | `#984EA3` |
| lblue | `#AECBE8` |
| lorange | `#FFC56E` |
| dark | `#000000` |

## Survey palette (CONGRESS + FRESCO papers)

Use when both surveys appear on the same axes:

| Survey | Colour | Hex | Notes |
|--------|--------|-----|-------|
| CONGRESS / F356W | vibrant orange | `#F97316` | Tailwind orange-500 |
| FRESCO / F444W | cobalt blue | `#3B82F6` | Tailwind blue-500 |
| JADES | dimgrey | `dimgrey` | matplotlib named |

CONGRESS-internal variants (exposure schematic only):

- Module A: `#C2410C` (Tailwind orange-700)
- Module B: `#FDBA74` (Tailwind orange-300)

Orange–blue is greyscale-safe and protanopia/deuteranopia-safe.

## NIRCam vs NIRSpec palette

| Population | Colour | Hex |
|------------|--------|-----|
| NIRCam grism | purple | `#9467BD` |
| NIRSpec MOS | green | `#2CA02C` |
| NIRCam+NIRSpec overlap | dim cool grey | `#5F6062` |
| Ground-only spec-z | silver | `silver` |

## Emission-line identity palette

| Line | Hex | Notes |
|------|-----|-------|
| Pa α | `#1f77b4` | tab:blue |
| Pa β | `#17becf` | teal — avoids green/red clash with He I |
| He I 1.083 µm | `#d62728` | tab:red |
| Hβ | `#9467bd` | tab:purple |
| Br β | `#ff7f0e` | tab:orange |
| Hα (Lin+25) | `#e377c2` | tab:pink |

## Marker conventions (SFRD-style figures)

| Class | `ms` | `mew` | `capsize` | `elinewidth` |
|-------|-----:|------:|----------:|-------------:|
| This-work science | 18 | 2.0 | 4 | 2.2 |
| External companion | 8.5 | — | 2.5 | 1.0 |
| Literature compilation | 7.0 | — | 2.5 | 1.0 |
| Legend proxies | 11 | — | — | — |

Always `mec="k"` on markers over dense contours.

## Fresco rcParams summary

```
font.family: serif (DejaVu Serif, Times New Roman, STIX)
mathtext.fontset: stix
font.size: 14 | axes.labelsize: 14 | xtick/ytick: 13 | legend: 11
figure.dpi: 120 | savefig.dpi: 200 | savefig.bbox: tight
axes.linewidth: 1.0 | axes.grid: False
xtick/ytick.direction: in | top/right ticks: True | minor ticks: visible
legend.frameon: False
lines.linewidth: 1.6 | lines.markersize: 4.5
text.usetex: False
```

## Legacy rcParams highlights (differs from fresco)

```
font.serif: CMU Serif | text.usetex: True
axes.labelsize: 19 | xtick/ytick.labelsize: 17.5 | legend.fontsize: 17
axes.linewidth: 1.8 | lines.linewidth: 2.5
figure.figsize: [6.15, 5.0] | figure.dpi: 72
axes.prop_cycle: seaborn Set1 (10 colors, desat=0.7)
savefig.dpi: figure (not 200)
```

Legacy `apply_plot_params()` filters blocked keys (backend, interactive, etc.) and rebuilds prop_cycle for modern matplotlib.

## Design rationale

- **Serif + STIX math** matches ApJ/journal body text; embedded `$...$` renders consistently without requiring a full LaTeX install (fresco).
- **Inward ticks + minor ticks** give calibration without grids; outward ticks waste space at small figure sizes.
- **Muted palette** prevents neighbouring traces from competing at print resolution.
- **dpi 200 + bbox tight** yields crisp PDFs without manual cropping.
- **Path-effect halos** replace bbox backgrounds for annotations on images/contours.

## Anti-patterns

| Don't | Do instead |
|-------|------------|
| `ax.grid()` | Rely on inward minor ticks |
| `legend(frameon=True)` | Leave default False |
| `bbox=dict(...)` on text | `path_effects=PE_DARK` |
| Default tab10 colors | `PALETTE` or documented line/survey hex |
| Sans-serif fonts | Serif via rcParams |
| PNG for journal submission | PDF vector export |
| seaborn `set_style("whitegrid")` | `apply_plot_style("fresco")` |

## Minimal worked example

```python
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plot_style import apply_plot_style, palette_for
from plot_params_fresco import PE_DARK

apply_plot_style("fresco")
PALETTE = palette_for("fresco")

x = np.linspace(0, 10, 200)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, np.sin(x), lw=1.8, color=PALETTE["blue"], label="sin")
ax.plot(x, np.cos(x), lw=1.8, color=PALETTE["orange"], label="cos")
ax.set(xlabel="x", ylabel="f(x)", xlim=(0, 10), ylim=(-1.2, 1.2))
ax.text(2.0, 0.9, "demo", color="black", path_effects=PE_DARK)
ax.legend(loc="lower left")
fig.savefig("demo.pdf")
```
