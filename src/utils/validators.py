"""Input validation helpers."""

from __future__ import annotations


def not_empty(value: str) -> bool:
    return bool(value and value.strip())
