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

## Use with Other AI Models — 其他模型使用教程

Not using Claude Code? This skill works with any AI that can write Python code.

### ChatGPT

1. Open ChatGPT, start a new conversation
2. Copy the entire content of `SKILL.md` and paste it as your first message, prefixed with: "Follow these instructions to help me build a resume:"
3. Also copy and paste the relevant `references/` files when needed:
   - `role-templates.md` — when ChatGPT asks about your target role
   - `regional-norms.md` — when deciding photo/format for your region
   - `bullet-writing.md` — when writing bullet points
4. ChatGPT will follow the 4-phase pipeline and generate Python code
5. **Copy the generated .py file and run it locally** — ChatGPT's Code Interpreter may not have reportlab installed

### DeepSeek / Kimi / 通义千问 / 豆包

1. 新建对话，把 `SKILL.md` 全文贴进去，开头加一句："请按照以下指令帮我制作简历"
2. 按需贴入 `references/` 下的文件（角色模板、地区规范、bullet写法等）
3. 模型会按4阶段流程走：问你信息→组织结构→生成代码→调排版
4. **生成的 .py 文件需要本地运行**：`pip install reportlab` 然后 `python gen_xx_pdf.py`
5. 把运行结果（Y值和bottom值）贴回对话，模型会帮你调spacing

### Cursor / Windsurf

1. Copy `SKILL.md` content into `.cursorrules` (Cursor) or `.windsurfrules` (Windsurf)
2. Copy `references/` folder into your project
3. Say "帮我做简历" in the AI chat — it will follow the skill pipeline

### Copilot CLI / Gemini CLI

These support skill-like formats natively. Place the files in your project and reference them in your config.

### Key Differences by Platform

| Capability | Claude Code | ChatGPT | DeepSeek/Kimi | Cursor |
|-----------|------------|---------|---------------|--------|
| Auto-load skill | Native | Manual paste | Manual paste | Via rules file |
| Run Python & generate PDF | Direct | Limited (sandbox) | No (local only) | Direct |
| Iterative spacing tuning | Automatic | Manual copy-paste results | Manual copy-paste results | Semi-auto |
| Read references/ files | Automatic | Manual paste when needed | Manual paste when needed | Automatic |

**The core value is in the prompt itself** — the 4-phase pipeline, bullet writing rules, role templates, and regional norms work with any model. The difference is automation: Claude Code is fully automatic, others need you to copy-paste between the AI and your terminal.

---

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
