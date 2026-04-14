"""Utilities for discovering and loading fonts for Matplotlib."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from matplotlib import font_manager as fm

DEFAULT_FONT_NAME = "SunTimes"
FONT_DATA_DIR = Path(__file__).resolve().parent / "data"
FONT_FILE_SUFFIXES = (".ttf", ".ttc", ".otf")


def is_font_loaded(font_name: str) -> bool:
    """Check whether a font name is available in Matplotlib font manager.

    Args:
        font_name: Font family name to check.

    Returns:
        ``True`` if the font name is already available.
    """
    font_names = {font.name for font in fm.fontManager.ttflist}
    return font_name in font_names


def get_packaged_font_files(font_dir: Path = FONT_DATA_DIR) -> list[Path]:
    """Collect packaged font files under a directory.

    Args:
        font_dir: Directory expected to contain bundled font files.

    Returns:
        A list of font file paths with supported suffixes.
    """
    if not font_dir.exists():
        return []

    font_paths: list[Path] = []
    for suffix in FONT_FILE_SUFFIXES:
        font_paths.extend(font_dir.glob(f"*{suffix}"))
    return sorted(font_paths)


def add_fonts(font_paths: Iterable[Path] | None = None) -> bool:
    """Register font files into Matplotlib's global font manager.

    Args:
        font_paths: Font file paths to register. If omitted, packaged files are used.

    Returns:
        ``True`` if at least one font file was registered, otherwise ``False``.
    """
    candidates = (
        list(font_paths) if font_paths is not None else get_packaged_font_files()
    )
    if not candidates:
        return False

    for font_file in candidates:
        fm.fontManager.addfont(str(font_file))
    return True


def ensure_font_available(font_name: str = DEFAULT_FONT_NAME) -> None:
    """Ensure the target font can be resolved by Matplotlib.

    The function first checks existing loaded fonts. If unavailable, it attempts to
    register packaged font files from ``mksci_font/data``.

    Args:
        font_name: Font family name required by rendering operations.

    Raises:
        ValueError: If the font is still unavailable after attempting registration.
    """
    if is_font_loaded(font_name):
        return

    add_fonts()
    if is_font_loaded(font_name):
        return

    raise ValueError(
        f"Font '{font_name}' is not available. "
        f"Install it on the system or bundle font files under: {FONT_DATA_DIR}"
    )
