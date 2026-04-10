# EN Resume PDF Generation — 英文简历 PDF 生成

## Font Setup

Helvetica is built into reportlab — no registration needed:

```python
FONT_R  = 'Helvetica'           # Regular — body text, bullets
FONT_B  = 'Helvetica-Bold'      # Bold — name, section titles, entry titles, skill labels
FONT_I  = 'Helvetica-Oblique'   # Italic — roles, dates
FONT_BI = 'Helvetica-BoldOblique'  # Bold-Italic (rarely used)
```

### Font usage rules

| Element | Font | Size | Color |
|---------|------|------|-------|
| Name (header) | FONT_B | 22pt | Black |
| Contact line | FONT_R | 9pt | Gray (0.3,0.3,0.3) |
| Section title | FONT_B | 11pt | Black |
| Entry title | FONT_B | 10pt | Black |
| Entry location | FONT_R | 9pt | Gray (0.3,0.3,0.3) |
| Subtitle/role | FONT_I | 9pt | Gray (0.35,0.35,0.35) |
| Date | FONT_I | 9pt | Gray (0.35,0.35,0.35) |
| Bullet text | FONT_R | 9pt | Black |
| Skill label | FONT_B | 9pt | Black |
| Skill value | FONT_R | 9pt | Black |
| Publication | FONT_R | 8pt | Black |

## Page Layout

Same as CN version:

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

W, H = A4
LM = 18 * mm
RM = 18 * mm
TM = 15 * mm
CW = W - LM - RM
```

## Text Wrapping (Word-Level)

English text wraps at word boundaries:

```python
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
```

## Complete Generator Template

```python
"""Generate EN resume PDF with proper font hierarchy using reportlab."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os

MYINFO = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(MYINFO, "Resume_EN.pdf")

FONT_R  = 'Helvetica'
FONT_B  = 'Helvetica-Bold'
FONT_I  = 'Helvetica-Oblique'

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
        name = "Full Name"
        nw = self._sw(name, FONT_B, 22)
        self.c.drawString((W - nw) / 2, self.y, name)
        self.y -= 16

        # Contact
        self.c.setFont(FONT_R, 9)
        self.c.setFillColorRGB(0.3, 0.3, 0.3)
        contact = "Tel: xxx  |  Email: xxx  |  GitHub: xxx"
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


# ── Build ──
r = R()
r.header()

r.section("EDUCATION")
r.entry("University Name", "City, State")
r.sub("Degree, Major", "Graduation Date")
r.bullet("Coursework: ...")

r.section("SKILLS")
r.skill_row("Technical: ", "Python, ...")
r.skill_row("Language: ", "English (Native), ...")

r.section("EXPERIENCE")
r.entry("Company/Project", "City, State")
r.sub("Role", "Date Range")
r.bullet("Achievement description...")

r.section("PUBLICATIONS")
r.pub('[1] Author "Title", venue, year.')

r.save()
print(f"EN: {OUTPUT} ({os.path.getsize(OUTPUT):,} bytes)")
print(f"Y: {r.y:.0f} (bottom: {TM:.0f})")
```

## Unicode Tips for Helvetica

Helvetica supports standard Latin + common symbols, but NOT:
- Thin space `\u2009` → renders as black square ■
- Some CJK chars → garbled

Safe special characters:
- En-dash `\u2013` (–) → works for negative numbers
- Bullet `\u2022` (•) → works
- Right single quote `\u2019` (') → works
- Left/right double quotes `\u201c` `\u201d` ("") → works

If you see black squares in the PDF, the character is not in the font.
Replace with ASCII equivalents.
