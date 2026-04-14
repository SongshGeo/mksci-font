"""Tests for font discovery and registration helpers."""

import pytest

from mksci_font import font_loader


class TestFontLoaderModule:
    """Test font discovery and registration behavior in edge conditions."""

    def test_get_packaged_font_files_returns_empty_for_missing_dir(self, tmp_path):
        """Font discovery should return empty list when directory does not exist."""
        missing = tmp_path / "missing_fonts"
        assert font_loader.get_packaged_font_files(missing) == []

    def test_get_packaged_font_files_filters_and_sorts_supported_suffixes(
        self, tmp_path
    ):
        """Discovery should include only supported suffixes and return sorted paths."""
        valid_b = tmp_path / "b.ttc"
        valid_a = tmp_path / "a.ttf"
        ignored = tmp_path / "ignored.txt"
        valid_b.write_text("font-b")
        valid_a.write_text("font-a")
        ignored.write_text("not-a-font")

        files = font_loader.get_packaged_font_files(tmp_path)
        assert files == [valid_a, valid_b]

    def test_add_fonts_returns_false_when_no_candidates(self):
        """add_fonts should return False when there is no file to register."""
        assert font_loader.add_fonts(font_paths=[]) is False

    def test_add_fonts_registers_each_candidate(self, monkeypatch, tmp_path):
        """add_fonts should call matplotlib addfont once per candidate path."""
        called: list[str] = []
        monkeypatch.setattr(
            font_loader.fm.fontManager,
            "addfont",
            lambda path: called.append(path),
        )

        f1 = tmp_path / "a.ttf"
        f2 = tmp_path / "b.otf"
        f1.write_text("a")
        f2.write_text("b")
        assert font_loader.add_fonts([f1, f2]) is True
        assert called == [str(f1), str(f2)]

    def test_ensure_font_available_raises_when_font_still_unavailable(
        self, monkeypatch
    ):
        """ensure_font_available should raise actionable ValueError if loading fails."""
        monkeypatch.setattr(font_loader, "is_font_loaded", lambda _: False)
        monkeypatch.setattr(font_loader, "add_fonts", lambda: False)
        with pytest.raises(ValueError, match="not available"):
            font_loader.ensure_font_available("MissingFont")
