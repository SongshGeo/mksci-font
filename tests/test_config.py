"""Tests for configuration normalization and global rc updates."""

import pytest
from matplotlib import pyplot as plt

from mksci_font import config as config_module


class TestConfigModule:
    """Test rc configuration normalization and merge rules."""

    @pytest.mark.parametrize(
        ("font_name", "rc_params", "expected_font", "expected_size"),
        [
            ("SunTimes", {"font.size": 11}, "SunTimes", 11),
            ({"font.size": 12}, None, "SunTimes", 12),
        ],
    )
    def test_build_rc_config_accepts_supported_input_forms(
        self,
        font_name,
        rc_params,
        expected_font,
        expected_size,
    ):
        """build_rc_config should support string font name and legacy mapping style."""
        config = config_module.build_rc_config(font_name=font_name, rc_params=rc_params)
        assert config["font.serif"] == [expected_font]
        assert config["font.size"] == expected_size

    def test_build_rc_config_rejects_ambiguous_mapping_plus_rc_params(self):
        """Passing mapping as font_name plus rc_params should raise clear TypeError."""
        with pytest.raises(TypeError, match="Cannot pass both mapping"):
            config_module.build_rc_config(
                font_name={"font.size": 12},
                rc_params={"axes.labelsize": 10},
            )

    @pytest.mark.parametrize("invalid_font_name", [123, 1.2, object()])
    def test_build_rc_config_rejects_non_string_font_name(self, invalid_font_name):
        """Non-string font_name should fail fast with explicit type validation."""
        with pytest.raises(TypeError, match="font_name must be a string"):
            config_module.build_rc_config(font_name=invalid_font_name)

    def test_overrides_take_precedence_over_rc_params(self):
        """Keyword overrides should win over rc_params when keys conflict."""
        config = config_module.build_rc_config(
            font_name="SunTimes",
            rc_params={"font.size": 8},
            **{"font.size": 16},
        )
        assert config["font.size"] == 16

    def test_config_font_updates_global_rcparams(self):
        """config_font should apply merged config to matplotlib global rcParams."""
        applied = config_module.config_font(rc_params={"font.size": 13})
        assert applied["font.serif"] == ["SunTimes"]
        assert plt.rcParams["font.size"] == 13
