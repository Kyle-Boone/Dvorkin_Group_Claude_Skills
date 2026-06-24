"""Matplotlib rcParams for the CONGRESS + FRESCO paper look (see PLOTTING_STYLE.md)."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe

PALETTE = {
    "blue": "#2E5C8A",
    "orange": "#E08214",
    "grey": "#7A7A7A",
    "lblue": "#7FA8C9",
    "lorange": "#F2B66D",
    "dark": "#222222",
    "green": "#2E8B57",
    "purple": "#7A4B8A",
}

PE_DARK = [pe.withStroke(linewidth=2.5, foreground="w")]
PE_LIGHT = [pe.withStroke(linewidth=2.5, foreground="k")]

_PAPER_RC = {
    # fonts
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Times", "STIXGeneral"],
    "mathtext.fontset": "stix",
    "font.size": 14,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 11,
    # figure
    "figure.dpi": 120,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    # axes
    "axes.linewidth": 1.0,
    "axes.edgecolor": PALETTE["dark"],
    "axes.labelcolor": PALETTE["dark"],
    "axes.grid": False,
    "axes.prop_cycle": mpl.cycler(
        color=[
            PALETTE["blue"],
            PALETTE["orange"],
            PALETTE["grey"],
            PALETTE["green"],
            PALETTE["purple"],
            PALETTE["lblue"],
        ]
    ),
    # ticks — inward on all four sides + minor ticks
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.major.size": 5.0,
    "ytick.major.size": 5.0,
    "xtick.minor.size": 2.8,
    "ytick.minor.size": 2.8,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "xtick.minor.width": 0.8,
    "ytick.minor.width": 0.8,
    # legend / lines / markers
    "legend.frameon": False,
    "lines.linewidth": 1.6,
    "lines.markersize": 4.5,
    # avoid LaTeX / notebook-backend overrides from older configs
    "text.usetex": False,
}


def use_paper_style():
    """Apply paper rcParams. Idempotent; safe to call at the top of each script."""
    plt.rcParams.update(_PAPER_RC)


def apply_plot_params():
    """Alias for use_paper_style() (keeps older import names working)."""
    use_paper_style()
