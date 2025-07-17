"""File management utilities."""

from __future__ import annotations

import shutil
from pathlib import Path

VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}
FILES_DIR = Path("data/patient_files")


def store_file(patient_id: int, path: str, file_type: str) -> str:
    """Store a file for a patient and return the stored path."""
    src = Path(path)
    if src.suffix.lower() not in VALID_EXTENSIONS:
        raise ValueError("Invalid file type")
    dest_dir = FILES_DIR / str(patient_id)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy(src, dest)
    return str(dest)
