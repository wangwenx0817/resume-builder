# Resume Builder — Claude Code Skill

A Claude Code skill that autonomously generates professional one-page PDF resumes with pixel-perfect layout.

## What It Does

Tell Claude Code "帮我做简历" or "build my resume" and it will:

1. **Collect** your info (education, experience, skills, publications)
2. **Adapt** section order and format to your target role and region
3. **Write** concise, quantified bullet points
4. **Generate** a one-page PDF with proper font hierarchy
5. **Tune** spacing iteratively until the page is perfectly filled

Supports **25+ career roles** (SWE, Marketing, Consulting, Academic, Healthcare, etc.) and **17 regional norms** (US, China, Japan, Germany, UK, etc.).

## Install as Claude Code Skill

```bash
# Copy to your Claude Code skills directory
cp -r resume-builder ~/.claude/skills/resume-builder
```

Then in any Claude Code session, say "帮我做简历" or "build my resume" to trigger the skill.

## Standalone Usage (Without Claude Code)

You can also use the example generators directly:

```bash
pip install reportlab

# Generate CN resume (requires CJK font — macOS Songti built-in)
cd examples
python gen_cn_pdf.py

# Generate EN resume (Helvetica is built into reportlab)
python gen_en_pdf.py
```

Edit the `# ── Build ──` section in each script to fill in your own content.

## Structure

```
resume-builder/
├── SKILL.md                         # Main skill document (4-phase pipeline)
├── references/
│   ├── reportlab-cn.md              # CN PDF generation guide (Songti fonts + photo)
│   ├── reportlab-en.md              # EN PDF generation guide (Helvetica fonts)
│   ├── bullet-writing.md            # Bullet point writing guide (quantify everything)
│   ├── layout-tuning.md             # Layout tuning guide (spacing algorithm)
│   ├── regional-norms.md            # 17 region/country resume norms
│   └── role-templates.md            # 25+ career role templates
├── examples/
│   ├── gen_cn_pdf.py                # Example CN resume generator (placeholder)
│   └── gen_en_pdf.py                # Example EN resume generator (placeholder)
├── requirements.txt
├── LICENSE
└── README.md
```

## Features

- **One page guarantee** — iterative spacing algorithm ensures content fits exactly one A4 page
- **Font hierarchy** — 3-weight system (Black/Bold/Light for CN, Bold/Regular/Italic for EN)
- **Photo support** — for regions that require it (China, Japan, Germany, Korea, UAE)
- **25+ role templates** — SWE, Quant, Marketing, Consulting, Legal, Healthcare, Academic, and more
- **17 regional norms** — US (no photo), China (photo + gender), Japan (standardized format), etc.
- **Thin resume strategy** — guidance for filling a page when experience is limited
- **Cross-platform fonts** — auto-detects CJK fonts on macOS, Linux, and Windows
- **4-gate verification** — content accuracy, layout quality, interview readiness, technical correctness
- **Overflow strategy** — prioritized list of what to cut when content doesn't fit

## Layout Tuning

After generating a PDF, the script prints:

```
CN: Resume_CN.pdf (230,000 bytes)
Y: 62 (bottom: 43)
```

- `Y ≈ bottom + 5~15pt` — perfect, done
- `Y >> bottom` — increase spacing (use "loose" preset in SKILL.md)
- `Y < bottom` — decrease spacing or trim content (use "tight" preset)

See `references/layout-tuning.md` for the full algorithm.

## Font Notes

| Platform | CN Font | Path |
|----------|---------|------|
| macOS | Songti.ttc | `/System/Library/Fonts/Supplemental/Songti.ttc` |
| Linux | Noto Sans CJK | `apt install fonts-noto-cjk` |
| Windows | SimSun | `C:\Windows\Fonts\simsun.ttc` |

EN resumes use Helvetica (built into reportlab) — works everywhere.

## License

MIT
