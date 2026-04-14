"""Decorator APIs for applying mksci-font behavior."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from functools import wraps
from typing import Any

from matplotlib import pyplot as plt

from .config import build_rc_config
from .font_loader import DEFAULT_FONT_NAME
from .text_ops import update_font


def mksci_font(
    mapping_strings: Mapping[str, str] | None = None,
    font_name: str = DEFAULT_FONT_NAME,
    **elements: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorate plotting functions and apply text/font updates.

    Args:
        mapping_strings: Optional exact string replacement mapping.
        font_name: Font family name to apply.
        **elements: Element text keyed by setter suffix.

    Returns:
        A decorator for plotting functions that return a Matplotlib artist.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with plt.rc_context(build_rc_config(font_name=font_name)):
                artist = func(*args, **kwargs)
                return update_font(
                    artist,
                    mapping_strings=mapping_strings,
                    font_name=font_name,
                    **elements,
                )

        return wrapper

    return decorator
