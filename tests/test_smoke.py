import matplotlib
import matplotlib.pyplot as plt

import mksci_font
from mksci_font import config as config_module
from mksci_font import font_wrapper
from mksci_font import mksci_font as mksci_decorator
from mksci_font import text_ops

matplotlib.use("Agg")


def test_public_api_exports():
    assert set(mksci_font.__all__) == {
        "config_font",
        "mksci_font",
        "show",
        "update_font",
    }


def test_build_config_and_global_config_font(monkeypatch):
    monkeypatch.setattr(config_module, "ensure_font_available", lambda _: None)

    config = font_wrapper.get_config(font_kwargs={"font.size": 11})
    assert config["font.family"] == "serif"
    assert config["font.serif"] == ["SunTimes"]
    assert config["font.size"] == 11

    applied = mksci_font.config_font(rc_params={"font.size": 13})
    assert applied["font.serif"] == ["SunTimes"]
    assert plt.rcParams["font.serif"][0] == "SunTimes"
    assert plt.rcParams["font.size"] == 13


def test_config_font_keeps_legacy_mapping_call(monkeypatch):
    monkeypatch.setattr(config_module, "ensure_font_available", lambda _: None)

    applied = mksci_font.config_font({"font.size": 14})

    assert applied["font.serif"] == ["SunTimes"]
    assert plt.rcParams["font.size"] == 14


def test_update_font_applies_requested_labels(monkeypatch):
    monkeypatch.setattr(config_module, "ensure_font_available", lambda _: None)
    monkeypatch.setattr(
        text_ops, "update_figure_font", lambda figure, font_name="SunTimes": figure
    )

    _, ax = plt.subplots()
    ax.set_title("Origin title")

    updated = mksci_font.update_font(
        ax,
        mapping_strings={"Origin title": "Updated title"},
        xlabel="X label",
        ylabel="Y label",
    )
    assert updated is ax
    assert ax.get_title() == "Updated title"
    assert ax.get_xlabel() == "X label"
    assert ax.get_ylabel() == "Y label"
    plt.close(ax.figure)


def test_decorator_preserves_function_metadata(monkeypatch):
    monkeypatch.setattr(config_module, "ensure_font_available", lambda _: None)
    monkeypatch.setattr(
        text_ops, "update_figure_font", lambda figure, font_name="SunTimes": figure
    )

    @mksci_decorator(ylabel="Y")
    def plot_demo():
        _, ax = plt.subplots()
        ax.set_ylabel("old")
        return ax

    ax = plot_demo()
    assert plot_demo.__name__ == "plot_demo"
    assert ax.get_ylabel() == "Y"
    plt.close(ax.figure)
