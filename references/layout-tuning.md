# Layout Tuning Guide — 排版微调指南

## The Goal

```
Final Y position ≈ bottom margin (TM) + 5~15pt
```

- Y > TM + 60pt → too much whitespace, increase spacing
- Y > TM + 15pt → slightly loose, minor adjustments
- TM < Y < TM + 15pt → perfect, done
- Y < TM → content overflows page, decrease spacing or cut content

## Tuning Parameters (Priority Order)

### 1. Section gap (biggest impact)
```python
def section(self, title):
    self.y -= N  # ← tune this (range: 3-12)
    ...
    self.y -= M  # ← and this (range: 8-15)
```
Each section has ~2 gap controls. Changing by 2pt per section × 4 sections = 8pt total swing.

### 2. Entry gap (after bold title line)
```python
self.y -= N  # after entry title (range: 13-17)
```

### 3. Sub gap (after italic role/date line)
```python
self.y -= N  # after sub line (range: 12-15)
```

### 4. Bullet line height
```python
self.y -= N  # per wrapped line (range: 11-14 for 9pt text)
self.y -= M  # after last line of bullet (range: 1-3)
```
This has the largest cumulative effect because there are many bullets.

### 5. Skill row gap
```python
self.y -= N  # per skill row (range: 12-14.5)
```

### 6. Publication line gap
```python
self.y -= N  # per pub line (range: 10-12)
self.y -= M  # between pubs (range: 2-4)
```

## Tuning Algorithm

```
Step 1: Generate PDF, note final Y and bottom margin
Step 2: Calculate delta = Y - bottom
Step 3: Count adjustable elements:
        - N_sections (typically 4)
        - N_entries (typically 5-7)
        - N_bullets (typically 15-20 lines after wrapping)
Step 4: Distribute delta across elements:
        - Section gaps get 30% of delta
        - Entry/sub gaps get 30%
        - Bullet lines get 30%
        - Skill/pub gaps get 10%
Step 5: Regenerate and verify
Step 6: Fine-tune ±1pt if needed
```

## Photo Tuning (CN Only)

### Parameters
```python
PW, PH = 18 * mm, 24 * mm           # Size (width × height)
x = W - RM - PW - offset_x          # X position
y = self.y - PH + offset_y           # Y position
```

### Common issues and fixes

| Issue | Fix |
|-------|-----|
| Photo overlaps text on left | Decrease PW or increase offset_x |
| Photo cut off at top | Increase offset_y |
| Photo cut off at right | Increase offset_x |
| Photo too large relative to header | Reduce PW and PH proportionally |
| Photo blocks location text ("纽黑文") | Shorten location text or shift photo |

### Iteration strategy
- Adjust in 2pt increments
- Check both photo bounds and nearby text
- Keep aspect ratio when resizing (PW:PH ≈ 3:4 for portrait)

## Lessons Learned — 踩坑记录

### Font rendering
1. **PingFang.ttc** has PostScript outlines → reportlab error. Use **Songti.ttc**.
2. **fpdf2** garbles CJK on page 2 with TTC fonts. Use **reportlab**.
3. **weasyprint** needs system pango (not pip-installable on macOS easily).
4. **Thin space `\u2009`** renders as ■ in Helvetica. Use regular space or nothing.
5. Songti subfontIndex: 0=Black, 1=Bold, 3=Light (not 2).

### Layout
6. CN text wraps char-by-char, EN word-by-word. Different `_wrap()` methods.
7. CN bullet points are denser → need more vertical space per line.
8. EN Helvetica is narrower → more text fits per line → fewer wrap lines.
9. Always print `Y: {r.y:.0f} (bottom: {TM:.0f})` after generation for tuning.
10. User says "顶满" = minimize bottom whitespace (Y ≈ TM + 5pt).
11. User says "太密了" = increase spacing between sections.

### Content
12. User's name must be verified — 汪 not 王 (common mistake).
13. EN resumes don't need photos (US convention).
14. Strategy metrics must match what user can actually explain in interview.
15. Don't invent achievements — ask user to confirm every number.
