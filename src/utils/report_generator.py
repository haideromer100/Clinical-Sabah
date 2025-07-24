"""Generate patient visit reports."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

LOGO_PATH = Path("assets/icons/logo.png")


def generate_report(patient: dict, visits: Iterable[dict], pdf_path: Path) -> None:
    """Create a PDF report for a patient."""
    width, height = A4
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    y = height - 50

    if LOGO_PATH.exists():
        c.drawImage(str(LOGO_PATH), 50, y - 50, width=80, preserveAspectRatio=True, mask='auto')
        y -= 100

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Patient Report: {patient['name']}")
    y -= 30

    c.setFont("Helvetica", 12)
    for visit in visits:
        c.drawString(50, y, f"{visit['visit_date']}: {visit['treatment']}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

    c.save()
