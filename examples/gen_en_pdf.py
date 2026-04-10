"""
Example: Generate EN resume PDF with proper font hierarchy using reportlab.

Usage:
  1. Replace placeholder content with your own info
  2. Run: python gen_en_pdf.py

Requirements:
  - pip install reportlab
  - Helvetica is built into reportlab (no extra fonts needed)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os

DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(DIR, "Resume_EN.pdf")

# Helvetica is built into reportlab — no registration needed
FONT_R = 'Helvetica'
FONT_B = 'Helvetica-Bold'
FONT_I = 'Helvetica-Oblique'

# ── Page Layout ───────────────────────────────────────────────────────────────
W, H = A4
LM = 18 * mm
RM = 18 * mm
TM = 15 * mm
CW = W - LM - RM


class R:
    def __init__(self):
        self.c = canvas.Canvas(OUTPUT, pagesize=A4)
        self.y = H - TM

    def _sw(self, text, font, size):
        return self.c.stringWidth(text, font, size)

    def _wrap(self, text, font, size, max_w):
        """Word-level wrapping for English text."""
        words = text.split(' ')
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if self._sw(test, font, size) > max_w:
                if cur:
                    lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)
        return lines

    def header(self):
        # Name - bold, large, centered (no photo for EN)
        self.c.setFont(FONT_B, 22)
        name = "Your Name"  # ← Replace
        nw = self._sw(name, FONT_B, 22)
        self.c.drawString((W - nw) / 2, self.y, name)
        self.y -= 16

        # Contact
        self.c.setFont(FONT_R, 9)
        self.c.setFillColorRGB(0.3, 0.3, 0.3)
        contact = "Tel: +1(xxx)xxx-xxxx  |  Email: your@email.com  |  GitHub: github.com/yourname"
        cw = self._sw(contact, FONT_R, 9)
        self.c.drawString((W - cw) / 2, self.y, contact)
        self.c.setFillColorRGB(0, 0, 0)
        self.y -= 12

    def section(self, title):
        self.y -= 6
        self.c.setFont(FONT_B, 11)
        self.c.drawString(LM, self.y, title)
        self.y -= 3
        self.c.setStrokeColorRGB(0.2, 0.2, 0.2)
        self.c.setLineWidth(0.6)
        self.c.line(LM, self.y, W - RM, self.y)
        self.y -= 11

    def entry(self, title, location=""):
        self.c.setFont(FONT_B, 10)
        self.c.drawString(LM, self.y, title)
        if location:
            self.c.setFont(FONT_R, 9)
            self.c.setFillColorRGB(0.3, 0.3, 0.3)
            lw = self._sw(location, FONT_R, 9)
            self.c.drawString(W - RM - lw, self.y, location)
            self.c.setFillColorRGB(0, 0, 0)
        self.y -= 15

    def sub(self, role, date):
        self.c.setFont(FONT_I, 9)
        self.c.setFillColorRGB(0.35, 0.35, 0.35)
        self.c.drawString(LM, self.y, role)
        dw = self._sw(date, FONT_I, 9)
        self.c.drawString(W - RM - dw, self.y, date)
        self.c.setFillColorRGB(0, 0, 0)
        self.y -= 13

    def bullet(self, text):
        bx = LM + 5 * mm
        self.c.setFont(FONT_R, 9)
        self.c.drawString(LM + 2 * mm, self.y + 0.5, "\u2022")
        lines = self._wrap(text, FONT_R, 9, CW - 7 * mm)
        for line in lines:
            self.c.drawString(bx, self.y, line)
            self.y -= 12
        self.y -= 2

    def skill_row(self, label, value):
        self.c.setFont(FONT_B, 9)
        self.c.drawString(LM, self.y, label)
        lw = self._sw(label, FONT_B, 9)
        self.c.setFont(FONT_R, 9)
        self.c.drawString(LM + lw + 1, self.y, value)
        self.y -= 13.5

    def pub(self, text):
        self.c.setFont(FONT_R, 8)
        lines = self._wrap(text, FONT_R, 8, CW)
        for line in lines:
            self.c.drawString(LM, self.y, line)
            self.y -= 10
        self.y -= 2

    def save(self):
        self.c.save()


# ── Build ─────────────────────────────────────────────────────────────────────
# Replace ALL content below with your own info.

r = R()
r.header()

r.section("EDUCATION")
r.entry("MIT", "Cambridge, MA")
r.sub("Master of Science, Computer Science", "Jun 2024")
r.bullet("Coursework: Machine Learning, Deep Learning, Distributed Systems, Algorithm Design")
r.entry("Stanford University", "Stanford, CA")
r.sub("Bachelor of Science, Mathematics", "Jun 2021")
r.bullet("Coursework: Probability, Statistics, Optimization, Real Analysis")

r.section("SKILLS")
r.skill_row("Technical: ", "Python, C++, PyTorch, SQL, Git, Docker, Kubernetes")
r.skill_row("Domain: ", "Machine Learning, NLP, Recommendation Systems, MLOps")
r.skill_row("Language: ", "English (Native), Mandarin (Fluent)")

r.section("EXPERIENCE")
r.entry("Google", "Mountain View, CA")
r.sub("Software Engineer Intern", "Jul 2023 \u2013 Jan 2024")
r.bullet("Optimized ranking model for search recommendations, improving CTR by 3.2% validated via online A/B test")
r.bullet("Designed feature engineering pipeline processing 1B+ daily user events with Apache Beam")

r.entry("AutoML Pipeline \u2013 Open Source Project")
r.sub("Independent Developer", "Jan 2023 \u2013 Present")
r.bullet("Built automated ML pipeline supporting data cleaning, feature selection, model training, and hyperparameter search end-to-end")
r.bullet("500+ GitHub stars, adopted by 3 companies in production environments")

r.section("PUBLICATIONS")
r.pub('[1] X. Zhang, Y. Li "Efficient Transformer for Long-Sequence Recommendation", AAAI 2024.')

r.save()
print(f"EN: {OUTPUT} ({os.path.getsize(OUTPUT):,} bytes)")
print(f"Y: {r.y:.0f} (bottom: {TM:.0f})")
# Target: Y should be within 5-15pt of TM (bottom margin).
# If Y >> TM: increase spacing in section/entry/bullet methods.
# If Y < TM: decrease spacing or trim content.
