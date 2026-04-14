"""Compatibility facade for legacy imports from ``mksci_font.font_wrapper``."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .config import build_rc_config, config_font
from .decorators import mksci_font
from .display import show
from .font_loader import DEFAULT_FONT_NAME, FONT_DATA_DIR, add_fonts, is_font_loaded
from .text_ops import replace_text, update_elements, update_figure_font, update_font

FONT_DIRS = str(FONT_DATA_DIR)
FONTS = (DEFAULT_FONT_NAME,)


def all_fonts_loaded() -> bool:
    """Check whether all required default fonts are currently available.

    Returns:
        ``True`` if all default fonts can be resolved by Matplotlib.
    """
    return all(is_font_loaded(font_name) for font_name in FONTS)


def get_config(
    font_name: str | Mapping[str, Any] = DEFAULT_FONT_NAME,
    font_kwargs: Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Build rcParams configuration.

    This function is kept for backward compatibility and delegates to
    :func:`mksci_font.config.build_rc_config`.

    Args:
        font_name: Preferred serif font family name, or a legacy rcParams mapping.
        font_kwargs: Optional rcParams mapping.
        **kwargs: Extra rcParams overrides.

    Returns:
        A merged rcParams dictionary.
    """
    return build_rc_config(font_name=font_name, rc_params=font_kwargs, **kwargs)


__all__ = [
    "FONT_DIRS",
    "FONTS",
    "add_fonts",
    "all_fonts_loaded",
    "config_font",
    "get_config",
    "is_font_loaded",
    "mksci_font",
    "replace_text",
    "show",
    "update_elements",
    "update_figure_font",
    "update_font",
]
