"""Tests for decorator and display helper modules."""

from matplotlib import pyplot as plt

from mksci_font import decorators as decorators_module
from mksci_font import display as display_module
from mksci_font import text_ops


class TestDecoratorAndDisplayModules:
    """Test decorator wrapping and show helper behavior."""

    def test_decorator_preserves_metadata_and_updates_artist(self, monkeypatch):
        """mksci_font decorator should preserve __name__ and mutate artist labels."""
        monkeypatch.setattr(
            text_ops, "update_figure_font", lambda figure, font_name="SunTimes": figure
        )

        @decorators_module.mksci_font(ylabel="Y")
        def plot_demo():
            """Demo function for decorator testing."""
            _, ax = plt.subplots()
            ax.set_ylabel("old")
            return ax

        ax = plot_demo()
        assert plot_demo.__name__ == "plot_demo"
        assert plot_demo.__doc__ == "Demo function for decorator testing."
        assert ax.get_ylabel() == "Y"
        plt.close(ax.figure)

    def test_show_passes_through_to_matplotlib_show(self, monkeypatch, axes):
        """display.show should forward args/kwargs and return underlying result."""
        received = {}

        def fake_show(*args, **kwargs):
            received["args"] = args
            received["kwargs"] = kwargs
            return "show-result"

        monkeypatch.setattr(display_module.plt, "show", fake_show)
        result = display_module.show(axes.figure, "arg1", block=False)
        assert result == "show-result"
        assert received["args"] == ("arg1",)
        assert received["kwargs"] == {"block": False}
