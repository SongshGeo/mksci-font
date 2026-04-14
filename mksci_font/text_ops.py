"""Operations for updating text content and font styles on Matplotlib artists."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from matplotlib.artist import Artist
from matplotlib.figure import Figure
from matplotlib.text import Text

from .config import build_rc_config
from .font_loader import DEFAULT_FONT_NAME


def _apply_text_font(text_obj: Any, font_name: str) -> None:
    """Apply a font family to a text-like object when possible."""
    if hasattr(text_obj, "set_fontfamily"):
        text_obj.set_fontfamily([font_name])


def update_figure_font(figure: Figure, font_name: str = DEFAULT_FONT_NAME) -> Figure:
    """Update font family for all ``Text`` objects in a figure.

    Args:
        figure: Target figure to update.
        font_name: Font family name to apply.

    Returns:
        The updated figure.
    """
    build_rc_config(font_name=font_name)
    for text_obj in figure.findobj(lambda x: isinstance(x, Text)):
        text_obj.set_fontfamily([font_name])
    figure.canvas.draw_idle()
    return figure


def _replace_text_object(text_obj: Text, mapping: Mapping[str, str]) -> bool:
    """Replace text content for one text object.

    Args:
        text_obj: Text object to mutate.
        mapping: Replacement mapping from old text to new text.

    Returns:
        ``True`` if replacement occurred.
    """
    old_text = text_obj.get_text()
    new_text = mapping.get(old_text, old_text)
    if new_text == old_text:
        return False

    text_obj.set_text(new_text)
    return True


def replace_text(
    obj: Artist,
    replacements: Mapping[str, str],
    font_name: str = DEFAULT_FONT_NAME,
) -> Artist:
    """Replace exact text matches under an artist tree.

    Args:
        obj: Root artist object.
        replacements: String replacement mapping.
        font_name: Font family name used after replacement.

    Returns:
        The same artist object.
    """
    changed = False
    for child in obj.get_children():
        if isinstance(child, Text):
            changed = _replace_text_object(child, replacements) or changed
        elif hasattr(child, "get_children"):
            replace_text(child, replacements, font_name=font_name)

    if changed and obj.figure is not None:
        update_figure_font(obj.figure, font_name=font_name)
    return obj


def update_elements(
    artist: Artist,
    refresh_all: bool = True,
    font_name: str = DEFAULT_FONT_NAME,
    **elements: str,
) -> Artist:
    """Update label-like elements on an artist.

    Args:
        artist: Target artist object.
        refresh_all: Whether to refresh all text objects on the figure.
        font_name: Font family name to apply.
        **elements: Element text keyed by setter suffix, e.g. ``xlabel``.

    Returns:
        The same artist object.

    Raises:
        AttributeError: If an element setter does not exist.
    """
    build_rc_config(font_name=font_name)
    for element, value in elements.items():
        try:
            setter = getattr(artist, f"set_{element}")
        except AttributeError as exc:
            raise AttributeError(f"No such attribute: {element}") from exc
        text_obj = setter(value)
        _apply_text_font(text_obj, font_name=font_name)

    if refresh_all and artist.figure is not None:
        update_figure_font(artist.figure, font_name=font_name)
    return artist


def update_font(
    artist: Artist,
    mapping_strings: Mapping[str, str] | None = None,
    refresh: bool = False,
    font_name: str = DEFAULT_FONT_NAME,
    **elements: str,
) -> Artist:
    """Update text content and font settings for a Matplotlib artist.

    Args:
        artist: Target artist object.
        mapping_strings: Optional exact string replacement mapping.
        refresh: Whether to refresh the full figure text font.
        font_name: Font family name to apply.
        **elements: Element text keyed by setter suffix.

    Returns:
        The same artist object.
    """
    if mapping_strings:
        replace_text(artist, mapping_strings, font_name=font_name)
    update_elements(artist, refresh_all=refresh, font_name=font_name, **elements)
    return artist
