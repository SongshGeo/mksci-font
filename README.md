
mksci-font
==========

`mksci-font` is a Python package that makes it easy to convert Matplotlib figures for use with Chinese fonts. It includes several functions that allow you to configure the font settings for your figures, as well as update the text elements of existing figures to use Chinese fonts.

Installation
------------

To install `mksci-font`, you can use pip:

bash

```bash
pip install mksci-font
```

Usage
-----

### Setting the default font configuration

To configure the default font settings for Matplotlib, you can use the `config_font()` function. This function takes no arguments, and sets the default font family to "SimSun" for Chinese text and "Times" for English text:

python

```python
from mksci_font import config_font

config_font()
```

### Converting a function to use Chinese fonts

To convert a function that generates a Matplotlib axes to use Chinese fonts, you can use the `@mksci_font` decorator. This decorator wraps your function and applies the configured font settings to the resulting figure:

python

```python
from mksci_font import mksci_font

@mksci_font
def my_plot():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    ax.set_xlabel('X轴')
    ax.set_ylabel('Y轴')
    ax.set_title('中文标题')

    return ax
```

### Updating the text elements of an existing figure

To update the text elements of an existing figure to use Chinese fonts, you can use the `update_elements()` function. This function takes an existing Matplotlib axes object and updates its text elements to use the configured font settings:

python

```python
from mksci_font import update_elements

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Title')

update_elements(ax, xlabel='X轴', ylabel='Y轴', title='中文标题')
```

License
-------

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
