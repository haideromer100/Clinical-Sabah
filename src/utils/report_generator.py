"""Generate patient visit reports."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

LOGO_PATH = Path("assets/icons/logo.png")


def generate_report(pdf_path: Path, patient: dict, visits: Iterable[dict]) -> None:
    """Create a PDF report for a patient."""
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    y = height - 50
    if LOGO_PATH.exists():
        c.drawImage(str(LOGO_PATH), 50, y - 50, width=100, preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y - 70, f"Patient Report: {patient['name']}")
    c.setFont("Helvetica", 12)
    y -= 100
    for visit in visits:
        c.drawString(50, y, f"{visit['visit_date']}: {visit['treatment']}")
        y -= 20
    c.save()
