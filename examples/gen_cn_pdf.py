"""
Example: Generate CN resume PDF with proper font hierarchy using reportlab.

Usage:
  1. Replace placeholder content with your own info
  2. Put your photo as "photo.jpg" in the same directory
  3. Run: python gen_cn_pdf.py

Requirements:
  - macOS with Songti.ttc (built-in), or Linux with fonts-noto-cjk
  - pip install reportlab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(DIR, "photo.jpg")
OUTPUT = os.path.join(DIR, "Resume_CN.pdf")

# ── Font Setup ────────────────────────────────────────────────────────────────
def find_cjk_font():
    """Auto-detect CJK font across platforms."""
    candidates = [
        ('/System/Library/Fonts/Supplemental/Songti.ttc', 0, 1, 3),
        ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 0, 2, 4),
        ('/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc', 0, 2, 4),
        ('C:\\Windows\\Fonts\\simsun.ttc', 0, 0, 0),
        ('C:\\Windows\\Fonts\\msyh.ttc', 0, 1, 0),
    ]
    for path, black, bold, light in candidates:
        if os.path.exists(path):
            return path, black, bold, light
    return None, 0, 0, 0

FONT_PATH, _IDX_BLACK, _IDX_BOLD, _IDX_LIGHT = find_cjk_font()
if not FONT_PATH:
    print("No CJK font found. Install fonts-noto-cjk (Linux) or update FONT_PATH.")
    sys.exit(1)

pdfmetrics.registerFont(TTFont('Song-Black', FONT_PATH, subfontIndex=_IDX_BLACK))
pdfmetrics.registerFont(TTFont('Song-Bold',  FONT_PATH, subfontIndex=_IDX_BOLD))
pdfmetrics.registerFont(TTFont('Song-Light', FONT_PATH, subfontIndex=_IDX_LIGHT))

# ── Page Layout ───────────────────────────────────────────────────────────────
W, H = A4
LM = 18 * mm
RM = 18 * mm
TM = 15 * mm
CW = W - LM - RM
PW, PH = 18 * mm, 24 * mm  # photo size


class R:
    def __init__(self):
        self.c = canvas.Canvas(OUTPUT, pagesize=A4)
        self.y = H - TM

    def _sw(self, text, font, size):
        return self.c.stringWidth(text, font, size)

    def _wrap(self, text, font, size, max_w):
        """Character-level wrapping for CJK text."""
        lines, cur = [], ""
        for ch in text:
            test = cur + ch
            if self._sw(test, font, size) > max_w:
                if cur:
                    lines.append(cur)
                cur = ch
            else:
                cur = test
        if cur:
            lines.append(cur)
        return lines

    def header(self):
        # Photo (top-right corner)
        if os.path.exists(PHOTO):
            img = ImageReader(PHOTO)
            self.c.drawImage(img, W - RM - PW - 2 * mm, self.y - PH + 22,
                             width=PW, height=PH, preserveAspectRatio=True, mask='auto')

        # Name - Black weight, large, centered
        self.c.setFont('Song-Black', 22)
        name = "Your Name"  # ← Replace
        nw = self._sw(name, 'Song-Black', 22)
        self.c.drawString((W - nw) / 2, self.y, name)
        self.y -= 16

        # Contact
        self.c.setFont('Song-Light', 9)
        self.c.setFillColorRGB(0.3, 0.3, 0.3)
        contact = "Tel: 138-xxxx-xxxx  |  Email: your@email.com  |  GitHub: github.com/yourname"
        cw = self._sw(contact, 'Song-Light', 9)
        self.c.drawString((W - cw) / 2, self.y, contact)
        self.c.setFillColorRGB(0, 0, 0)
        self.y -= 12

    def section(self, title):
        self.y -= 8
        self.c.setFont('Song-Black', 11)
        self.c.drawString(LM, self.y, title)
        self.y -= 3
        self.c.setStrokeColorRGB(0.2, 0.2, 0.2)
        self.c.setLineWidth(0.6)
        self.c.line(LM, self.y, W - RM, self.y)
        self.y -= 12

    def entry(self, title, location=""):
        self.c.setFont('Song-Bold', 10)
        self.c.drawString(LM, self.y, title)
        if location:
            self.c.setFont('Song-Light', 9)
            self.c.setFillColorRGB(0.3, 0.3, 0.3)
            lw = self._sw(location, 'Song-Light', 9)
            self.c.drawString(W - RM - lw, self.y, location)
            self.c.setFillColorRGB(0, 0, 0)
        self.y -= 15

    def sub(self, role, date):
        self.c.setFont('Song-Light', 9)
        self.c.setFillColorRGB(0.35, 0.35, 0.35)
        self.c.drawString(LM, self.y, role)
        dw = self._sw(date, 'Song-Light', 9)
        self.c.drawString(W - RM - dw, self.y, date)
        self.c.setFillColorRGB(0, 0, 0)
        self.y -= 13

    def bullet(self, text):
        bx = LM + 5 * mm
        self.c.setFont('Song-Light', 9)
        self.c.drawString(LM + 2 * mm, self.y + 0.5, "\u2022")
        lines = self._wrap(text, 'Song-Light', 9, CW - 7 * mm)
        for line in lines:
            self.c.drawString(bx, self.y, line)
            self.y -= 12
        self.y -= 2

    def skill_row(self, label, value):
        self.c.setFont('Song-Bold', 9)
        self.c.drawString(LM, self.y, label)
        lw = self._sw(label, 'Song-Bold', 9)
        self.c.setFont('Song-Light', 9)
        self.c.drawString(LM + lw + 1, self.y, value)
        self.y -= 13.5

    def pub(self, text):
        self.c.setFont('Song-Light', 8)
        lines = self._wrap(text, 'Song-Light', 8, CW)
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

r.section("\u6559\u80b2\u7ecf\u5386")  # 教育经历
r.entry("\u6e05\u534e\u5927\u5b66", "\u5317\u4eac")  # 清华大学, 北京
r.sub("\u8ba1\u7b97\u673a\u79d1\u5b66\u4e0e\u6280\u672f \u7855\u58eb", "2022.09 \u2013 2025.06")
r.bullet("\u6838\u5fc3\u8bfe\u7a0b\uff1a\u673a\u5668\u5b66\u4e60\u3001\u6df1\u5ea6\u5b66\u4e60\u3001\u5206\u5e03\u5f0f\u7cfb\u7edf\u3001\u7b97\u6cd5\u8bbe\u8ba1\u4e0e\u5206\u6790")
r.entry("\u5317\u4eac\u5927\u5b66", "\u5317\u4eac")  # 北京大学
r.sub("\u6570\u5b66\u4e0e\u5e94\u7528\u6570\u5b66 \u5b66\u58eb", "2018.09 \u2013 2022.06")
r.bullet("GPA 3.8/4.0\uff0c\u4e13\u4e1a\u6392\u540d\u524d5%\uff0c\u83b7\u56fd\u5bb6\u5956\u5b66\u91d12\u6b21")

r.section("\u4e13\u4e1a\u6280\u80fd")  # 专业技能
r.skill_row("\u7f16\u7a0b\u8bed\u8a00\uff1a", "Python, C++, Java, SQL, JavaScript")
r.skill_row("\u6280\u672f\u6808\uff1a", "PyTorch, TensorFlow, Docker, Kubernetes, Redis")
r.skill_row("\u8bed\u8a00\u80fd\u529b\uff1a", "\u82f1\u8bed\uff08CET-6 580\u5206\uff09\u3001\u666e\u901a\u8bdd\uff08\u6bcd\u8bed\uff09")

r.section("\u5de5\u4f5c\u4e0e\u5b9e\u4e60\u7ecf\u5386")  # 工作与实习经历
r.entry("\u5b57\u8282\u8df3\u52a8 \u2013 \u63a8\u8350\u7cfb\u7edf\u7ec4", "\u5317\u4eac")
r.sub("\u540e\u7aef\u5f00\u53d1\u5b9e\u4e60\u751f", "2024.06 \u2013 2024.12")
r.bullet("\u4f18\u5316\u63a8\u8350\u6a21\u578b\u5728\u7ebf\u63a8\u7406\u670d\u52a1\uff0c\u5c06P99\u5ef6\u8fdf\u4ece120ms\u964d\u81f345ms\uff0cQPS\u63d0\u53872.5\u500d")
r.bullet("\u8bbe\u8ba1\u5e76\u5b9e\u73b0\u7528\u6237\u7279\u5f81\u5b9e\u65f6\u8ba1\u7b97\u7ba1\u9053\uff0c\u65e5\u5747\u5904\u740610\u4ebf+\u7528\u6237\u884c\u4e3a\u4e8b\u4ef6")

r.entry("\u5f00\u6e90\u9879\u76ee\uff1aGo-Cache\uff08\u5206\u5e03\u5f0f\u7f13\u5b58\u7cfb\u7edf\uff09")
r.sub("\u72ec\u7acb\u5f00\u53d1\u8005", "2023.09 \u2013 \u81f3\u4eca")
r.bullet("\u57fa\u4e8e\u4e00\u81f4\u6027\u54c8\u5e0c\u5b9e\u73b0\u5206\u5e03\u5f0f\u7f13\u5b58\uff0c\u652f\u6301LRU/LFU\u6dd8\u6c70\u7b56\u7565\uff0c\u8bfb\u5199\u541e\u5410\u8fbe50K QPS")
r.bullet("GitHub 800+ stars\uff0c\u88ab3\u5bb6\u521d\u521b\u516c\u53f8\u7528\u4e8e\u751f\u4ea7\u73af\u5883")

r.section("\u7814\u7a76\u6210\u679c")  # 研究成果
r.pub('[1] M. Li, X. Zhang, "Efficient Graph Neural Networks for Large-Scale Recommendation", WWW 2025.')

r.save()
print(f"CN: {OUTPUT} ({os.path.getsize(OUTPUT):,} bytes)")
print(f"Y: {r.y:.0f} (bottom: {TM:.0f})")
