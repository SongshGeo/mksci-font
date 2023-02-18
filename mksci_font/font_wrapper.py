#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

from typing import Callable, Dict, Optional

import pkg_resources
from matplotlib import font_manager as fm
from matplotlib import pyplot as plt
from matplotlib.artist import Artist

FONT_DIRS = pkg_resources.resource_filename("mksci_font", "data")
FONTS = ("SunTimes",)


def is_font_loaded(font_name):
    # Use findfont to check if the font is loaded
    font_names = [font.name for font in fm.fontManager.ttflist]
    return font_name in font_names


def all_fonts_loaded():
    return all(is_font_loaded(font) for font in FONTS)


def show(figure=None, *args, **kwargs):
    """显示图形"""
    if figure is not None:
        plt.figure(figure.number)  # set the given figure as the current figure
    with plt.rc_context(get_config()):
        results = plt.show(*args, **kwargs)
    return results


def get_config(font_name="SunTimes", font_kwargs: dict = None, **kwargs) -> dict:
    added = add_fonts()
    if font_kwargs is None:
        font_kwargs = {}
    if added is False:
        raise ValueError(f"No fonts found in the following directories: {FONT_DIRS}")
    return (
        {
            "font.family": "serif",
            "font.serif": [font_name],  # 衬线字体, 优先输入字体
            "mathtext.fontset": "stix",  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
            "axes.unicode_minus": False,  # 处理负号，即-号
            # 'text.usetex': text_usetex,  # 使用latex渲染文本
        }
        | kwargs
        | font_kwargs
    )


def add_fonts():
    if all_fonts_loaded():
        return True
    font_files = fm.findSystemFonts(fontpaths=FONT_DIRS)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    return all_fonts_loaded()


def replace_text(obj: Artist, replacements: Dict[str, str]) -> Artist:
    """
    Replaces any `Text` objects in the given `Artist` object that match a key in the given dictionary of replacements
    with the corresponding value.

    Parameters
    ----------
    ax : matplotlib.Artist.Artist
        The `Artist` object to search for `Text` objects.
    replacements : dict
        A dictionary of string replacements, where each key is the string to search for and each value is the replacement
        string.

    Returns
    -------
    None

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> text_obj = ax.text(0.5, 0.5, 'Hello, world!', fontsize=12)
    >>> replace_text(ax, {'Hello, world!': 'Goodbye, world!'})
    Replaced "Hello, world!" with "Goodbye, world!"

    Notes
    -----
    This function only replaces exact matches of the text content in the dictionary keys, and does not perform partial
    or case-insensitive matching.
    """
    for text_obj in obj.get_children():
        if isinstance(text_obj, plt.Text):
            _replace_text_objects(text_obj, replacements)
        elif hasattr(text_obj, "get_children"):
            replace_text(text_obj, replacements)
    update_figure_font(obj.figure)
    return obj


def _replace_text_objects(text_obj, mapping: Dict[str, str]):
    old_text = text_obj.get_text()
    new_text = mapping.get(old_text, old_text)
    if new_text != old_text:
        with plt.rc_context(get_config()):
            text_obj.set_text(new_text)


def update_figure_font(figure):
    # Update the font properties of the text elements in the figure
    config = get_config()
    with plt.rc_context(config):
        for text_obj in figure.findobj(lambda x: isinstance(x, plt.Text)):
            text_obj.set_fontfamily(plt.rcParams.get("font", config["font.serif"]))
    # Draw the figure with the updated font properties
    figure.canvas.draw_idle()
    return figure


def update_elements(ax: Artist, refresh_all: bool = True, **elements: dict):
    """Updates the text elements of the given Artist object with the given new values."""
    config = get_config()
    for element in elements:
        try:
            setting_func = getattr(ax, f"set_{element}")
            with plt.rc_context(config):
                text_obj = setting_func(elements[element])
                text_obj.set_fontfamily(plt.rcParams.get("font", config["font.serif"]))
        except AttributeError as e:
            raise AttributeError(f"No such attribute: {element}") from e
    if refresh_all:
        update_figure_font(ax.figure)
    return ax


def mksci_font(
    mapping_strings: Optional[Dict[str, str]] = None, **elements: Dict[str, str]
) -> Callable:
    """替换坐标轴标签文本的装饰器"""
    if mapping_strings is None:
        mapping_strings = {}

    def decorator(func):
        def wrapper(*args, **kwargs):
            config = get_config()
            with plt.rc_context(config):
                ax = func(*args, **kwargs)
                update_elements(ax, **elements)
                replace_text(ax, mapping_strings)
            return ax

        return wrapper

    return decorator


def config_font(*args, **kwargs):
    plt.rcParams.update(get_config("SunTimes", *args, **kwargs))
