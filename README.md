
mksci-font
==========

`mksci-font` 用于方便地将 Matplotlib 支持中文字体允许您配置图形为“中文宋体、英文 Times New Roman”。

## 安装

使用喜欢的包管理工具安装：

```bash
pip install mksci-font
```

当前版本要求 `Python >= 3.10`。

之所以提高最低 Python 版本，是为了跟进 `Pillow` 的安全修复版本，并避免旧版本传递依赖持续触发安全告警。

### 从源码开发（uv）

本仓库使用 [uv](https://docs.astral.sh/uv/) 管理依赖与锁文件。克隆后可在项目根目录执行：

```bash
uv sync --extra dev
uv run pytest tests/test_smoke.py
```

修改 `pyproject.toml` 中的依赖后，请同步锁文件并更新导出的 `requirements.txt`（供仅使用 pip 的环境或工具扫描）：

```bash
uv lock
uv export --no-hashes --no-emit-project -o requirements.txt
```

使用方法
----

### 配置默认字体设置

要为 Matplotlib 配置默认字体设置，可以使用 `config_font()` 函数。

```python
# 推荐写法：显式传 rc_params
config_font(rc_params={"font.size": 12})

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

## 维护说明

项目显式约束了安全版本的 `Pillow`，而不是仅依赖 `matplotlib` 的传递依赖解析结果。
这样可以在保持与 `matplotlib` 兼容的同时，避免解析到存在已知安全问题的旧版本。

字体资源策略：

- 默认优先使用系统中已安装的 `SunTimes` 字体。
- 如果你希望随包分发字体文件，可将 `.ttf/.ttc/.otf` 放到 `mksci_font/data/`，运行时会自动尝试注册。
- 当系统字体不可用且包内也没有字体文件时，库会抛出明确错误，提示安装字体或补充文件。

依赖解析以 `uv.lock` 为准；`requirements.txt` 由 `uv export` 生成，提交前请与锁文件保持一致。

许可证
---

本项目基于 MIT 许可证开源。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

关于作者
---

[Shuang Song](https://cv.songshgeo.com/), a scientist who also travels.

<a href="https://www.buymeacoffee.com/USgxYspYW4" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
