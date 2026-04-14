#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

import matplotlib
import matplotlib.pyplot as plt

import mksci_font
from mksci_font import font_wrapper

matplotlib.use("Agg")


def test_public_api_exports():
    assert set(mksci_font.__all__) == {
        "config_font",
        "mksci_font",
        "show",
        "update_font",
    }


def test_get_config_and_config_font(monkeypatch):
    monkeypatch.setattr(font_wrapper, "add_fonts", lambda: True)

    config = font_wrapper.get_config(font_kwargs={"font.size": 11})

    assert config["font.family"] == "serif"
    assert config["font.serif"] == ["SunTimes"]
    assert config["font.size"] == 11

    mksci_font.config_font(**{"font.size": 13})
    assert plt.rcParams["font.serif"][0] == "SunTimes"
    assert plt.rcParams["font.size"] == 13


def test_update_font_applies_requested_labels(monkeypatch):
    monkeypatch.setattr(font_wrapper, "add_fonts", lambda: True)
    monkeypatch.setattr(font_wrapper, "update_figure_font", lambda figure: figure)

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
