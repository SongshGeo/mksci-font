"""Tests for text replacement and artist update operations."""

import pytest
from matplotlib.text import Text

from mksci_font import text_ops


class TestTextOpsModule:
    """Test text replacement, update, and refresh behavior."""

    def test_replace_text_updates_exact_match_only(self, axes, monkeypatch):
        """replace_text should replace exact keys and keep unmatched text unchanged."""
        axes.set_title("Origin")
        axes.set_xlabel("Keep")
        called = {"count": 0}
        monkeypatch.setattr(
            text_ops,
            "update_figure_font",
            lambda figure, font_name="SunTimes": (
                called.__setitem__("count", called["count"] + 1) or figure
            ),
        )

        text_ops.replace_text(axes, {"Origin": "Updated"}, font_name="SunTimes")
        assert axes.get_title() == "Updated"
        assert axes.get_xlabel() == "Keep"
        assert called["count"] >= 1

    def test_replace_text_does_not_refresh_when_nothing_changes(
        self, axes, monkeypatch
    ):
        """replace_text should skip expensive refresh when mapping has no hit."""
        axes.set_title("NoChange")
        called = {"count": 0}
        monkeypatch.setattr(
            text_ops,
            "update_figure_font",
            lambda figure, font_name="SunTimes": (
                called.__setitem__("count", called["count"] + 1) or figure
            ),
        )
        text_ops.replace_text(axes, {"Origin": "Updated"}, font_name="SunTimes")
        assert called["count"] == 0

    def test_update_elements_updates_requested_labels(self, axes, monkeypatch):
        """update_elements should set selected labels and keep return identity."""
        monkeypatch.setattr(
            text_ops, "update_figure_font", lambda figure, font_name="SunTimes": figure
        )
        result = text_ops.update_elements(
            axes,
            refresh_all=False,
            xlabel="X label",
            ylabel="Y label",
        )
        assert result is axes
        assert axes.get_xlabel() == "X label"
        assert axes.get_ylabel() == "Y label"

    def test_update_elements_raises_for_unknown_setter(self, axes):
        """update_elements should raise AttributeError for unsupported element name."""
        with pytest.raises(AttributeError, match="No such attribute"):
            text_ops.update_elements(axes, not_a_real_label="value")

    def test_update_font_combines_mapping_and_direct_element_updates(
        self, axes, monkeypatch
    ):
        """update_font should apply mapping replacements and explicit kwargs updates."""
        axes.set_title("Origin")
        monkeypatch.setattr(
            text_ops, "update_figure_font", lambda figure, font_name="SunTimes": figure
        )
        updated = text_ops.update_font(
            axes,
            mapping_strings={"Origin": "Mapped"},
            refresh=False,
            xlabel="X",
        )
        assert updated is axes
        assert axes.get_title() == "Mapped"
        assert axes.get_xlabel() == "X"

    def test_update_figure_font_applies_target_font_family(self, axes):
        """update_figure_font should set font family on figure text objects."""
        text_obj = axes.set_title("Title")
        text_ops.update_figure_font(axes.figure, font_name="SunTimes")
        assert isinstance(text_obj, Text)
        assert text_obj.get_fontfamily() == ["SunTimes"]
