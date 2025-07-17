"""Basic smoke tests for the Clinical-Sabah application."""

import importlib

import pytest

try:
    import PyQt5  # noqa: F401
except Exception:
    PYQT5 = False
else:
    PYQT5 = True


@pytest.mark.skipif(not PYQT5, reason="PyQt5 not installed")
def test_entrypoint_importable():
    """Application entry point should import without errors."""
    importlib.import_module("clinical_sabah")
