"""Choose which matplotlib style module to apply in a script."""

from __future__ import annotations

import importlib
import os
from typing import Literal

StyleName = Literal["fresco", "legacy"]

STYLES: dict[str, str] = {
    "fresco": "plot_params_fresco",  # PLOTTING_STYLE.md (CONGRESS + FRESCO paper look)
    "legacy": "plot_params",         # CMU serif, LaTeX, large tick labels
}


def load_style(name: StyleName | str = "fresco"):
    """Import a style module by name."""
    key = name.lower()
    if key not in STYLES:
        raise ValueError(f"Unknown style {name!r}. Choose from: {', '.join(STYLES)}")
    return importlib.import_module(STYLES[key])


def apply_plot_style(name: StyleName | str | None = None):
    """
    Apply rcParams from the requested style module.

    If ``name`` is None, use the ``PLOT_STYLE`` environment variable,
    then fall back to ``fresco``.

    Resets matplotlib defaults first so switching styles in one session
    does not leave fresco settings active when you select legacy (or vice versa).
    """
    import matplotlib.pyplot as plt

    if name is None:
        name = os.environ.get("PLOT_STYLE", "fresco")
    plt.rcdefaults()
    mod = load_style(name)
    mod.apply_plot_params()
    return mod


def palette_for(name: StyleName | str | None = None):
    """Return the PALETTE dict for a style (for explicit colors in scatter/hist)."""
    mod = load_style(name or os.environ.get("PLOT_STYLE", "fresco"))
    return getattr(mod, "PALETTE", {})
