"""Basic smoke tests for the Clinical-Sabah application."""

import importlib


def test_entrypoint_importable():
    """Application entry point should import without errors."""
    importlib.import_module("clinical_sabah")
