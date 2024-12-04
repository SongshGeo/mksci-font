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


def is_font_loaded(font_name: str) -> bool:
    """检查指定字体是否已加载。

    Args:
        font_name: 要检查的字体名称。

    Returns:
        bool: 如果字体已加载返回 True，否则返回 False。

    Examples:
        >>> is_font_loaded('SimSun')
        True
        >>> is_font_loaded('一个不知名的字体')
        False
    """
    font_names = [font.name for font in fm.fontManager.ttflist]
    return font_name in font_names


def all_fonts_loaded() -> bool:
    """检查是否所有 FONTS 中定义的字体都已加载完成。

    Returns:
        bool: 如果所有字体都已加载返回 True，否则返回 False。

    Examples:
        >>> all_fonts_loaded()
        True

    Note:
        此函数检查当前会话中是否已加载所有 FONTS 中定义的字体
        （使用中文宋体和英文 Times New Roman 所必需）。
    """
    return all(is_font_loaded(font) for font in FONTS)


def show(figure: Optional[plt.Figure] = None, *args, **kwargs) -> None:
    """显示 matplotlib 图形。

    Args:
        figure: 要显示的图形对象。如果为 None，则创建新的图形。
        *args: 传递给 plt.show 的位置参数。
        **kwargs: 传递给 plt.show 的关键字参数。

    Returns:
        None

    Examples:
        显示一个新的图形：
        >>> show()

        显示现有的图形：
        >>> fig, ax = plt.subplots()
        >>> show(fig)

    Note:
        如果指定了 figure，该对象将被设置为当前的 matplotlib 图形对象。
    """
    if figure is not None:
        plt.figure(figure.number)
    with plt.rc_context(get_config()):
        results = plt.show(*args, **kwargs)
    return results


def get_config(font_name: str = "SunTimes", font_kwargs: dict = None, **kwargs) -> dict:
    """
    返回用于 Matplotlib 图形的字体配置字典。

    Parameters
    ----------
    font_name : str, optional
        衬线字体的名称。默认为 "SunTimes"。
    font_kwargs : dict, optional
        包含字体配置选项的字典。默认为 `None`。
    **kwargs
        其他字体配置选项。

    Returns
    -------
    dict
        用于 Matplotlib 图形的字体配置字典。

    Raises
    ------
    ValueError
        如果在 `FONT_DIRS` 中未找到字体。

    Notes
    -----
    该函数返回用于 Matplotlib 图形的字体配置字典。字体配置包括衬线字体、数学字体、负号处理等。用户可以指定
    `font_name` 和其他字体配置选项，也可以将它们作为关键字参数传递。默认情况下，衬线字体为 "SunTimes"。

    """
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


def add_fonts() -> bool:
    """
    添加指定文件夹下的字体到 matplotlib 的字体管理器。

    Returns
    -------
    bool
        如果成功添加所有字体，则返回 `True`，否则返回 `False`。

    Notes
    -----
    该函数将在指定文件夹 `FONT_DIRS` 中查找所有字体文件，并将其添加到 matplotlib 的字体管理器中。如果字体已经成功加载，
    则返回 `True`，否则返回 `False`。

    Raises
    ------
    RuntimeError
        如果无法找到任何字体文件，则会引发运行时错误。
    """
    if all_fonts_loaded():
        return True
    font_files = fm.findSystemFonts(fontpaths=FONT_DIRS)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    return all_fonts_loaded()


def replace_text(obj: Artist, replacements: Dict[str, str]) -> Artist:
    """在给定的 `Artist` 对象中查找任何匹配给定字典中键的 `Text` 对象，并将其替换为相应的值。

    Parameters
    ----------
    obj : matplotlib.artist.Artist
        要搜索 `Text` 对象的 `Artist` 对象。
    replacements : dict
        一个字符串替换的字典，其中每个键都是要查找的字符串，每个值都是替换字符串。

    Returns
    -------
    matplotlib.artist.Artist

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> text_obj = ax.text(0.5, 0.5, 'Hello, world!', fontsize=12)
    >>> replace_text(ax, {'Hello, world!': 'Goodbye, world!'})
    Replaced "Hello, world!" with "Goodbye, world!"

    Notes
    -----
    该函数仅替换与字典键的文本内容完全匹配的文本，不进行部分匹配或大小写不敏感匹配。
    """
    for text_obj in obj.get_children():
        if isinstance(text_obj, plt.Text):
            _replace_text_objects(text_obj, replacements)
        elif hasattr(text_obj, "get_children"):
            replace_text(text_obj, replacements)
    update_figure_font(obj.figure)
    return obj


def _replace_text_objects(text_obj, mapping: Dict[str, str]):
    """
    将 `Artist` 对象中的 `Text` 对象的文本内容进行替换。

    Parameters
    ----------
    text_obj : matplotlib.text.Text
        要替换文本的 `Text` 对象。
    mapping : Dict[str, str]
        一个字符串替换的字典，其中每个键都是要查找的字符串，每个值都是替换字符串。

    Returns
    -------
    None

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> text_obj = ax.text(0.5, 0.5, 'Hello, world!', fontsize=12)
    """
    old_text = text_obj.get_text()
    new_text = mapping.get(old_text, old_text)
    if new_text != old_text:
        with plt.rc_context(get_config()):
            text_obj.set_text(new_text)


def update_figure_font(figure: plt.Figure):
    """
    更新图形中文本元素的字体属性。

    Parameters
    ----------
    figure : matplotlib.figure.Figure
        要更新的 matplotlib 图形对象。

    Returns
    -------
    matplotlib.figure.Figure
        更新后的 matplotlib 图形对象。

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.set_title('题')
    >>> update_figure_font(fig)

    Notes
    -----
    此函数遍历图形中的文本元素，并根据 get_config() 函数返回的配置更新它们的字体属性。默认情况文本将设置为中文宋体，英文 Times New Roman。
    """
    # Update the font properties of the text elements in the figure
    config = get_config()
    with plt.rc_context(config):
        for text_obj in figure.findobj(lambda x: isinstance(x, plt.Text)):
            text_obj.set_fontfamily(plt.rcParams.get("font", config["font.serif"]))
        # Draw the figure with the updated font properties
        figure.canvas.draw_idle()
    return figure


def update_elements(artist: Artist, refresh_all: bool = True, **elements: dict):
    """使用给定的新值更新给定 Artist 对象的文本元素。

    Args:
        artist: 要更新的 Artist 对象。
        refresh_all: 是否刷新整个画布。默认值为 True。
        **elements: 每个元素名称（如 'xlabel'，'ylabel' 或 'title'）都是一个字符串，
            对应着要更改的属性的名称，相应的值则是要设置的新文本。

    Returns:
        matplotlib.artist.Artist: 更新后的 Artist 对象。

    Examples:
        >>> fig, ax = plt.subplots()
        >>> ax.set_xlabel('X轴')
        >>> update_elements(ax, xlabel='时间', ylabel='价格', title='标题')
    """
    config = get_config()
    for element, value in elements.items():
        try:
            setting_func = getattr(artist, f"set_{element}")
            with plt.rc_context(config):
                text_obj = setting_func(value)
                text_obj.set_fontfamily(plt.rcParams.get("font", config["font.serif"]))
        except AttributeError as e:
            raise AttributeError(f"No such attribute: {element}") from e
    if refresh_all:
        update_figure_font(artist.figure)
    return artist


def update_font(
    ax: Artist,
    mapping_strings: Dict[str, str] = None,
    refresh: bool = False,
    **elements: Dict[str, str],
) -> Artist:
    """将给定Artist对象的文本元素使用给定的新值更新。

    参数：
        ax: Artist
            要更新的Artist对象。
        mapping_strings: Dict[str, str]，可选
            一个字符串映射字典，其中每个键都是要搜索的字符串，每个值都是要替换的字符串。
        refresh: bool，可选
            是否刷新整个画布。
        **elements: Dict[str, str]
            每个元素名称（如 'xlabel'，'ylabel' 或 'title'）都是一个字符串，对应着要更改的属性的名称，
            相应的值则是要设置的新文本。

    返回：
        Artist
            更新后的Artist对象。

    用法：
        update_font(ax, mapping_strings={'Hello, world!': 'Goodbye, world!'}, xlabel='X轴', ylabel='Y轴', title='标题')

    """
    if mapping_strings is not None:
        replace_text(ax, mapping_strings)
    update_elements(ax, refresh_all=refresh, **elements)
    return ax


def mksci_font(
    mapping_strings: Optional[Dict[str, str]] = None, **elements: Dict[str, str]
) -> Callable:
    """
    将中文字体应用到装饰器中。

    Args:
        mapping_strings (Dict[str, str], optional): 字符串替换字典。默认为 None。
        **elements (Dict[str, str]): 字体配置选项。

    Returns:
        Callable: 装饰器函数。

    Decorator Example:
        >>> @mksci_font(xlabel='时间', ylabel='价格')
        >>> def my_plot():
        >>>     fig, ax = plt.subplots()
        >>>     ax.plot([1, 2, 3], [2, 3, 1])
        >>>     ax.set_title('标题')
        >>>     return ax

    Notes:
        该函数是一个装饰器函数，用于将一个生成 matplotlib.axes 的函数包装成中文，同时覆盖中文的标签标题等。
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            config = get_config()
            with plt.rc_context(config):
                ax = func(*args, **kwargs)
                ax = update_font(ax, mapping_strings, **elements)
            return ax

        return wrapper

    return decorator


def config_font(*args, **kwargs):
    """
    将字体配置应用于 `plt.rcParams` 中，以更改全局字体属性。

    Parameters
    ----------
    *args
        传递给 `get_config` 的位置参数
    **kwargs
        传递给 `get_config` 的关键字参数

    Returns
    -------
    None

    Examples
    --------
    >>> config_font()  # 设置默认字体
    >>> config_font("SimSun", fontsize=12)  # 设置字体为宋体, 字号为12

    Notes
    -----
    此函数的实现依赖于 `get_config` 函数，将 `get_config` 的结果应用于 `plt.rcParams`。
    """
    plt.rcParams.update(get_config("SunTimes", *args, **kwargs))
