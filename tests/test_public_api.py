"""Tests for package public API and compatibility facade."""

import mksci_font
from mksci_font import font_wrapper


class TestPublicApi:
    """Validate public package exports and legacy facade contracts."""

    def test_package_exports_expected_symbols(self):
        """Package should expose only stable top-level API symbols."""
        assert set(mksci_font.__all__) == {
            "config_font",
            "mksci_font",
            "show",
            "update_font",
        }

    def test_legacy_wrapper_still_exposes_compat_symbols(self):
        """Legacy module should keep compatibility aliases for old imports."""
        assert "get_config" in font_wrapper.__all__
        assert "update_font" in font_wrapper.__all__
        assert font_wrapper.FONTS == ("SunTimes",)
