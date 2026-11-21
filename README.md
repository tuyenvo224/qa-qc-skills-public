# QA/QC Agent Skills

A set of skills for QA/QC engineers: clarify requirements, hunt hidden bugs, write test cases (Markdown or Excel), write bug reports, and turn OpenAPI specs into API test cases.

The skills follow the open [Agent Skills](https://agentskills.io) standard (`SKILL.md`), so they work with Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, Antigravity and other AI tools that support `SKILL.md`. Tested mainly on Claude Code.

🇻🇳 Tiếng Việt: [README.vi.md](README.vi.md)

**Bilingual by design:** every skill is written in English but answers in the language you use. Ask in Vietnamese and you get Vietnamese output (analysis, test cases, Excel labels); ask in English and you get English. Technical terms stay in English.

## Skills

### Requirement analysis

| Skill | What it does |
|---|---|
| [`requirement-clarifier`](requirement-clarifier/) | Produces a prioritised list of clarification questions (with a Top 3) for a spec, ready to take into a review meeting with BA/PO. |
| [`requirement-to-mindmap`](requirement-to-mindmap/) | Turns a requirement into a markmap-compatible test-coverage mindmap (scenarios → checkbox test ideas), marking inferred cases as assumptions. |
| [`product-feature-overview`](product-feature-overview/) | Builds a product architecture map (Product → Epics → Features) from a large product overview / PRD. |

### Bug hunting and reporting

| Skill | What it does |
|---|---|
| [`bug-hunter-lite`](bug-hunter-lite/) | Destructive-testing pass over a flow: applies 6 lenses (break the flow, data, state, rules, assumptions, think like a bad user) and returns the top 5 high-impact bug hypotheses. |
| [`bug-report`](bug-report/) | Writes a ready-to-paste bug report for any tracker (Jira, Redmine, GitHub Issues…): title + 7-section body, `[UI]`/`[Function]` tag, expected result backed by spec rule IDs, and a check-before-posting list. |

### Test case design

| Skill | What it does |
|---|---|
| [`write-quick-test-cases`](write-quick-test-cases/) | Quick, lightweight test cases (positive / negative / boundary / security) exported to a standard Excel test-scenario template. |
| [`markdown-to-excel`](markdown-to-excel/) | Converts Markdown files containing tables (test cases, data lists…) into `.xlsx`. |

### API testing

| Skill | What it does |
|---|---|
| [`api-test-design-lite`](api-test-design-lite/) | Generates a core set of API test cases (Markdown tables) from an OpenAPI 3.x / Swagger 2.0 spec: happy paths, validation, declared limits, basic auth and not-found cases. |

## Suggested pipeline

```
requirement
  ─► requirement-clarifier     questions for BA/PO (QH/QM/QL IDs)
  ─► requirement-to-mindmap    test-coverage mindmap
  ─► bug-hunter-lite           top 5 hidden bugs
  ─► write-quick-test-cases    Excel test cases

failure found while testing ─► bug-report ─► (you review and paste into your tracker)

OpenAPI spec ─► api-test-design-lite ─► (you review the .md test cases)
```

Pass the output of one step into the next (questions answered, mindmap branches, bug hypotheses) so the test cases cover what was found earlier. Every skill also works on its own.

## Installation

1. Copy the skill folders you want into the skills folder of your AI tool.
   - **Claude Code:** `~/.claude/skills/` (all your projects) or `<your-project>/.claude/skills/` (that project only).
   - **Other tools:** see your tool's documentation for its skills folder.
2. Restart the tool (or start a new session) so the skills are picked up.
3. Just describe what you need, e.g. *"What should I ask the BA about this spec?"* or *"Viết test case cho chức năng đăng nhập và xuất ra Excel"*. In tools that support it you can also call a skill directly, e.g. `/<skill-name>` in Claude Code.

### Requirements

- An AI tool that supports Agent Skills (`SKILL.md`). The two Excel skills also need the tool to be able to run Python commands.
- Python 3.8+ with `openpyxl` for the Excel skills (`write-quick-test-cases`, `markdown-to-excel`): `pip install openpyxl`.

## Language

| You write in | Output |
|---|---|
| Vietnamese | Vietnamese (technical terms in English) |
| English | English |
| Explicit request (e.g. "output in English") | The language you asked for |

Excel exports switch their fixed labels (title, metadata, column headers) to match the output language.

## Author

tuyenvo224
