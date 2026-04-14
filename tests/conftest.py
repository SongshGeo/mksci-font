"""Shared pytest fixtures for mksci_font test suite."""

import matplotlib
import pytest
from matplotlib import pyplot as plt

from mksci_font import config as config_module

matplotlib.use("Agg")


@pytest.fixture(autouse=True)
def mock_font_availability(monkeypatch):
    """Mock font availability checks for tests unrelated to font installation."""
    monkeypatch.setattr(config_module, "ensure_font_available", lambda _: None)


@pytest.fixture
def axes():
    """Create and cleanup a Matplotlib Axes for each test case."""
    _, ax = plt.subplots()
    yield ax
    plt.close(ax.figure)
