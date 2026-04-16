import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def generate_pdf(summary, path="exports/reports/report.pdf"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = canvas.Canvas(path, pagesize=LETTER)
    text = c.beginText(40, 750)
    for line in summary.split("\n"):
        text.textLine(line)
    c.drawText(text)
    c.save()
    return path
