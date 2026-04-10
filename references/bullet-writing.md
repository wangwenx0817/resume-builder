# Bullet Point Writing Guide — 简历子弹点撰写指南

## The Formula — 公式

```
[Action Verb] + [What You Did] + [How/Using What] + [Quantified Result]
```

Examples:
- "Built an SPY Iron Condor strategy exploiting VRP (IV > RV 83%), achieving Sharpe 1.11"
- "构建 5 关验证框架，以隔离 subagent 方式派发，消除回测中的确认偏差"

## Action Verbs — 动词库

### Technical / Engineering
| English | 中文 | When to use |
|---------|------|-------------|
| Built | 构建 | Created something new from scratch |
| Designed | 设计 | Architectural decisions, system design |
| Implemented | 实现 | Coded a specific algorithm or feature |
| Developed | 开发 | End-to-end feature development |
| Architected | 架构设计 | High-level system design |
| Deployed | 部署 | Put into production/multiple environments |
| Optimized | 优化 | Made something faster/better |

### Research / Analysis
| English | 中文 | When to use |
|---------|------|-------------|
| Discovered | 发现 | Found a new insight from data |
| Identified | 筛选/识别 | Selected from candidates via analysis |
| Validated | 验证 | Proved something works (walk-forward, etc.) |
| Achieved | 实现/达到 | Hit a specific metric target |
| Proved | 证明 | Showed one thing beats another |
| Screened | 筛选 | Filtered from larger set |

## Quantification Rules — 量化规则

**Everything that can be a number should be a number.**

| Bad | Good |
|-----|------|
| "Improved strategy performance" | "Improved Sharpe from 0.7 to 1.11" |
| "Reduced risk" | "Max drawdown –9.0% vs. benchmark –33.7%" |
| "Used many factors" | "Screened 38 candidate factors, selected 14" |
| "Fast detection" | "Identified crash within 3 trading days" |
| "High accuracy" | "Accuracy 95.67%" |

### Key metrics by domain

**Quant / Finance:**
- Sharpe Ratio, CAGR, Max Drawdown, Win Rate
- IC (Information Coefficient), IC_IR
- OOS decay %, Walk-Forward window count
- Number of assets, factors, trading days

**ML / AI:**
- Accuracy, F1, AUC
- Compute savings (%), parameter count
- Training time, inference latency

**Engineering / Agent:**
- Pipeline stages, markets covered
- Uptime, error recovery rate
- Lines of code, test coverage

## Length Guidelines — 长度指南

- **Target: 1-2 lines** per bullet when rendered in PDF
- If a bullet wraps to 3+ lines → split into two bullets or trim
- CN text is denser (fewer chars per concept) → tends to be shorter
- EN text wraps more → be concise with prepositions and articles

## The Honesty Rule — 诚实原则

**Every bullet must pass the interview test:**
> "If the interviewer asks you to explain this bullet in detail,
>  can you talk about it for 2-3 minutes confidently?"

If not → rewrite to reflect what you actually did and understand.

This is why auto-generated strategy results (from model testing) should
be replaced with strategies you personally built and can explain.

## CN vs EN Style Differences

| Aspect | CN | EN |
|--------|----|----|
| Articles | None | Drop "a/an/the" where possible |
| Subject | Often omitted | Omit "I" (resume convention) |
| Numbers | 直接写 | Use commas for thousands |
| Parentheses | 全角（）or 半角() | Half-width () |
| Technical terms | 保留英文 (Sharpe, IC, VIX) | Native English |
| En-dash for negatives | Use `\u2013` (–) | Use `\u2013` (–) |

## Section-Specific Tips

### Education bullets
- Lead with coursework (most relevant to target role)
- GPA only if > 3.5 (or top 10%)
- Keep to 1 bullet per school

### Skills bullets
- Group by category (Technical, Domain, Language)
- List most relevant/impressive first
- Don't list basic tools (Excel, Word) unless applying for entry-level

### Experience bullets
- 3-4 bullets per major project
- 1-2 bullets per minor project
- Most impactful bullet first
- Last bullet can be the "so what" — portfolio-level result

### Publication bullets
- Standard citation format
- Bold your name if multiple authors
- Include status (preprint, submitted, published)
