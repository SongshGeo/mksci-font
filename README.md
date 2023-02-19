
mksci-font
==========

`mksci-font` 用于方便地将 Matplotlib 支持中文字体允许您配置图形为“中文宋体、英文 Times New Roman”。

## 安装

使用喜欢的包管理工具安装：

```bash
pip install mksci-font
```

使用方法
----

### 配置默认字体设置

要为 Matplotlib 配置默认字体设置，可以使用 `config_font()` 函数。

python

```python
# 同时还可以修改字号，以及其它任何 rcParams 支持的属性
config_font({"font.size": 12})

_, ax = plt.subplots(figsize=(4, 1))
ax.text(0.5, 0.5, msg, ha='center', va='center')
plt.show();

```

![U73Adi](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/U73Adi.jpg)

### 针对做图函数修改

对于返回`matplotlib.axes`的作图函数，可以简单使用 `@mksci_font` 装饰器，在修改字体的同时，可以将图中元素换成中文。

python

```python
msg = "让 Matplotlib 图件使用 \n “中文宋体、英文 Times New Roman”"
mapping_string = {'Origin title': '替换后的标题'}

@mksci_font(mapping_string, ylabel="覆盖原Y轴标签")
def plot():
    _, ax = plt.subplots(figsize=(4, 3))
    ax.text(0.5, 0.6, "mksci-font 中文", ha='center')
    ax.text(0.5, 0.3, msg, ha='center')
    ax.set_ylabel("will be replaced...")  # will be replaced by '中文'
    ax.set_xlabel("中文 & English & $TeX_{mode}$")
    ax.set_title("Origin title")
    return ax


ax = plot()
show()
```

![WbZq1I](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/WbZq1I.jpg)

### 更新现有图形的文本元素

可以使用 `update_font()` 函数更新已有图像，使用方法与`@mksci_font`类似：

```python
_, ax = plt.subplots(figsize=(4, 3))
ax.text(0.5, 0.6, "mksci-font 中文", ha='center')
ax.text(0.5, 0.3, msg, ha='center')
ax.set_ylabel("will be replaced...")  # will be replaced by '中文'
ax.set_xlabel("中文 & English & $TeX_{mode}$")
ax.set_title("Origin title")

msg = "让 Matplotlib 图件使用 \n “中文宋体、英文 Times New Roman”"
mapping_string = {'Origin title': '替换后的标题'}
update_font(ax, mapping_string, ylabel="覆盖原Y轴标签")
```

更多用法例子可以见[这个笔记本](tests/test_plot_jupyter.ipynb)

许可证
---

本项目基于 MIT 许可证开源。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

关于作者
---

[Shuang Song](https://cv.songshgeo.com/), a scientist who also travels.

<a href="https://www.buymeacoffee.com/USgxYspYW4" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
