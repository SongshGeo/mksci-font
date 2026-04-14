"""Matplotlib rc configuration helpers for mksci-font."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from matplotlib import pyplot as plt

from .font_loader import DEFAULT_FONT_NAME, ensure_font_available


def _normalize_config_inputs(
    font_name: str | Mapping[str, Any] = DEFAULT_FONT_NAME,
    rc_params: Mapping[str, Any] | None = None,
) -> tuple[str, dict[str, Any]]:
    """Normalize compatible input formats for config functions.

    Args:
        font_name: Target font name, or a legacy rcParams mapping.
        rc_params: Optional rcParams mapping.

    Returns:
        A tuple of normalized ``(font_name, rc_params)``.

    Raises:
        TypeError: If arguments cannot be normalized.
    """
    if isinstance(font_name, Mapping):
        if rc_params is not None:
            raise TypeError("Cannot pass both mapping font_name and rc_params.")
        return DEFAULT_FONT_NAME, dict(font_name)

    if not isinstance(font_name, str):
        raise TypeError("font_name must be a string.")

    return font_name, dict(rc_params or {})


def build_rc_config(
    font_name: str | Mapping[str, Any] = DEFAULT_FONT_NAME,
    rc_params: Mapping[str, Any] | None = None,
    **overrides: Any,
) -> dict[str, Any]:
    """Build Matplotlib rcParams used by this package.

    Args:
        font_name: Preferred serif font family name.
        rc_params: Additional rcParams values.
        **overrides: Additional rcParams values with higher precedence.

    Returns:
        A merged rcParams dictionary.
    """
    normalized_font_name, normalized_rc_params = _normalize_config_inputs(
        font_name=font_name,
        rc_params=rc_params,
    )
    ensure_font_available(normalized_font_name)

    config: dict[str, Any] = {
        "font.family": "serif",
        "font.serif": [normalized_font_name],
        "mathtext.fontset": "stix",
        "axes.unicode_minus": False,
    }
    config.update(normalized_rc_params)
    config.update(overrides)
    return config


def config_font(
    font_name: str | Mapping[str, Any] = DEFAULT_FONT_NAME,
    rc_params: Mapping[str, Any] | None = None,
    **overrides: Any,
) -> dict[str, Any]:
    """Apply font rc settings globally.

    Args:
        font_name: Preferred serif font family name.
        rc_params: Optional rcParams mapping.
        **overrides: Extra rcParams overrides.

    Returns:
        The resolved configuration dictionary that was applied.
    """
    config = build_rc_config(font_name=font_name, rc_params=rc_params, **overrides)
    plt.rcParams.update(config)
    return config
