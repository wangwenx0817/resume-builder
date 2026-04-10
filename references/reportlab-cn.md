# CN Resume PDF Generation — 中文简历 PDF 生成

## Font Setup

macOS Songti.ttc provides 3 useful weights via subfontIndex:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Font hierarchy: Black > Bold > Light
pdfmetrics.registerFont(TTFont('Song-Black', '/System/Library/Fonts/Supplemental/Songti.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('Song-Bold',  '/System/Library/Fonts/Supplemental/Songti.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('Song-Light', '/System/Library/Fonts/Supplemental/Songti.ttc', subfontIndex=3))
```

### Font usage rules

| Element | Font | Size | Color |
|---------|------|------|-------|
| Name (header) | Song-Black | 22pt | Black |
| Contact line | Song-Light | 8.5pt | Gray (0.3,0.3,0.3) |
| Section title | Song-Black | 11pt | Black |
| Entry title | Song-Bold | 10pt | Black |
| Entry location | Song-Light | 9pt | Gray (0.3,0.3,0.3) |
| Subtitle/role | Song-Light | 9pt | Gray (0.35,0.35,0.35) |
| Date | Song-Light | 9pt | Gray (0.35,0.35,0.35) |
| Bullet text | Song-Light | 9pt | Black |
| Skill label | Song-Bold | 9pt | Black |
| Skill value | Song-Light | 9pt | Black |
| Publication | Song-Light | 8pt | Black |

### Why Songti, not PingFang?

PingFang.ttc uses PostScript outlines → reportlab throws:
`"postscript outlines are not supported"`

Songti.ttc uses TrueType outlines → works perfectly with reportlab.

## Page Layout

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

W, H = A4                    # 595.28 × 841.89 pt
LM = 18 * mm                 # Left margin
RM = 18 * mm                 # Right margin
TM = 15 * mm                 # Top margin
CW = W - LM - RM             # Content width
```

## Photo Handling

```python
from reportlab.lib.utils import ImageReader

# Photo dimensions (portrait, passport-style)
PW, PH = 18 * mm, 24 * mm    # Typical range: 16-22mm × 22-28mm

# Position: top-right corner, aligned with education section
# self.y is current Y position after header
self.c.drawImage(
    ImageReader(PHOTO_PATH),
    W - RM - PW - 2 * mm,    # X: right-aligned with small offset
    self.y - PH + 24,        # Y: aligned near top of education
    PW, PH
)
```

### Photo tuning tips

- If photo overlaps "纽黑文" or location text → reduce PW/PH or shift left
- If photo is cut off at top → increase Y offset (+2pt at a time)
- If photo is cut off at right → increase X offset (move left)
- Keep photo within the margin area, don't let it extend beyond RM

## Text Wrapping (Character-Level)

Chinese text wraps character-by-character (no word boundaries):

```python
def _wrap(self, text, font, size, max_w):
    """Split text into lines that fit within max_w."""
    lines, cur = [], ""
    for ch in text:
        if self._sw(cur + ch, font, size) > max_w:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines
```

## Complete Generator Template

```python
"""Generate CN resume PDF with proper font hierarchy using reportlab."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os

MYINFO = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(MYINFO, "photo.jpg")
OUTPUT = os.path.join(MYINFO, "Resume_CN.pdf")

pdfmetrics.registerFont(TTFont('Song-Black', '/System/Library/Fonts/Supplemental/Songti.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('Song-Bold',  '/System/Library/Fonts/Supplemental/Songti.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('Song-Light', '/System/Library/Fonts/Supplemental/Songti.ttc', subfontIndex=3))

W, H = A4
LM = 18 * mm
RM = 18 * mm
TM = 15 * mm
CW = W - LM - RM
PW, PH = 18 * mm, 24 * mm


class R:
    def __init__(self):
        self.c = canvas.Canvas(OUTPUT, pagesize=A4)
        self.y = H - TM

    def _sw(self, text, font, size):
        return self.c.stringWidth(text, font, size)

    def _wrap(self, text, font, size, max_w):
        lines, cur = [], ""
        for ch in text:
            if self._sw(cur + ch, font, size) > max_w:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        if cur:
            lines.append(cur)
        return lines

    def header(self):
        # Photo top-right
        self.c.drawImage(ImageReader(PHOTO), W - RM - PW - 2 * mm, self.y - PH + 24, PW, PH)

        # Name - Black, large, centered
        self.c.setFont('Song-Black', 22)
        name = "姓名"
        nw = self._sw(name, 'Song-Black', 22)
        self.c.drawString(LM + (CW - nw) / 2, self.y, name)
        self.y -= 18

        # Contact - Light, small, centered
        self.c.setFont('Song-Light', 8.5)
        self.c.setFillColorRGB(0.3, 0.3, 0.3)
        contact = "手机: xxx  |  邮箱: xxx  |  GitHub: xxx"
        cw = self._sw(contact, 'Song-Light', 8.5)
        self.c.drawString(LM + (CW - cw) / 2, self.y, contact)
        self.c.setFillColorRGB(0, 0, 0)
        self.y -= 14

    def section(self, title):
        self.y -= 10
        self.c.setFont('Song-Black', 11)
        self.c.drawString(LM, self.y, title)
        self.y -= 3
        self.c.setStrokeColorRGB(0.2, 0.2, 0.2)
        self.c.setLineWidth(0.6)
        self.c.line(LM, self.y, W - RM, self.y)
        self.y -= 13

    def entry(self, title, location=""):
        self.c.setFont('Song-Bold', 10)
        self.c.drawString(LM, self.y, title)
        if location:
            self.c.setFont('Song-Light', 9)
            self.c.setFillColorRGB(0.3, 0.3, 0.3)
            lw = self._sw(location, 'Song-Light', 9)
            self.c.drawString(W - RM - lw, self.y, location)
            self.c.setFillColorRGB(0, 0, 0)
        self.y -= 16

    def sub(self, role, date):
        self.c.setFont('Song-Light', 9)
        self.c.setFillColorRGB(0.35, 0.35, 0.35)
        self.c.drawString(LM, self.y, role)
        dw = self._sw(date, 'Song-Light', 9)
        self.c.drawString(W - RM - dw, self.y, date)
        self.c.setFillColorRGB(0, 0, 0)
        self.y -= 14

    def bullet(self, text):
        bx = LM + 5 * mm
        self.c.setFont('Song-Light', 9)
        self.c.drawString(LM + 2 * mm, self.y, "•")
        lines = self._wrap(text, 'Song-Light', 9, CW - 7 * mm)
        for line in lines:
            self.c.drawString(bx, self.y, line)
            self.y -= 13
        self.y -= 2

    def skill_row(self, label, value):
        self.c.setFont('Song-Bold', 9)
        self.c.drawString(LM, self.y, label)
        lw = self._sw(label, 'Song-Bold', 9)
        self.c.setFont('Song-Light', 9)
        self.c.drawString(LM + lw + 1, self.y, value)
        self.y -= 14

    def pub(self, text):
        self.c.setFont('Song-Light', 8)
        lines = self._wrap(text, 'Song-Light', 8, CW)
        for line in lines:
            self.c.drawString(LM, self.y, line)
            self.y -= 11
        self.y -= 3

    def save(self):
        self.c.save()


# ── Build ──
r = R()
r.header()
r.y -= 10

r.section("教育背景")
r.entry("学校名称", "城市")
r.sub("学位，专业", "毕业时间")
r.bullet("核心课程：...")

r.section("技能")
r.skill_row("编程: ", "Python, ...")
r.skill_row("语言: ", "中文（母语）、英文（流利）")

r.section("经历")
r.entry("公司/项目名称", "地点")
r.sub("职位", "时间段")
r.bullet("成就描述...")

r.section("发表论文")
r.pub('[1] Author "Title", venue, year.')

r.save()
print(f"CN: {OUTPUT} ({os.path.getsize(OUTPUT):,} bytes)")
print(f"Y: {r.y:.0f} (bottom: {TM:.0f})")
```

## Common Pitfalls

1. **PingFang font** → PostScript outline error. Always use Songti.
2. **fpdf2 with TTC fonts** → garbled text on page 2. Use reportlab instead.
3. **weasyprint** → requires system pango library. Not available on all macOS.
4. **Thin space `\u2009`** → renders as black square in some fonts. Use regular space.
5. **Photo too large** → overlaps education text. Keep ≤ 22mm × 28mm.
