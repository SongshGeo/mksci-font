"""Display helpers for Matplotlib figures."""

from __future__ import annotations

from typing import Any

from matplotlib import pyplot as plt

from .config import build_rc_config
from .font_loader import DEFAULT_FONT_NAME


def show(
    figure: plt.Figure | None = None,
    *args: Any,
    font_name: str = DEFAULT_FONT_NAME,
    **kwargs: Any,
) -> Any:
    """Show a Matplotlib figure with package font settings.

    Args:
        figure: Optional figure to make current before showing.
        *args: Positional args passed to ``plt.show``.
        font_name: Font family name to apply.
        **kwargs: Keyword args passed to ``plt.show``.

    Returns:
        The return value from ``plt.show``.
    """
    if figure is not None:
        plt.figure(figure.number)
    with plt.rc_context(build_rc_config(font_name=font_name)):
        return plt.show(*args, **kwargs)
