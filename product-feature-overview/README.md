# product-feature-overview

Reads a large overview document or PRD of a **whole product or system** and builds a **Product Architecture Map**: product overview → Epics (large feature groups) → child Features, as a checkbox mindmap.

Vietnamese version: [README.vi.md](README.vi.md). The AI agent follows `SKILL.md`.

## Skill structure

```
product-feature-overview/
  ├── SKILL.md      ← instructions for the AI agent
  ├── README.md     ← this file
  └── README.vi.md  ← Vietnamese user guide
```

## When to use

- You are new to a product and need the big picture of its structure.
- You want a list of epics and features to plan testing across a whole system.

Not for: analyzing or clarifying **one** feature (use `requirement-clarifier`), or a test-coverage mindmap of one requirement (use `requirement-to-mindmap`).

## Installation

Copy the `product-feature-overview` folder into the skills folder of your AI tool:
- **Claude Code:** `~/.claude/skills/` (all projects) or `<your-project>/.claude/skills/` (one project).
- **Other tools** that support [Agent Skills](https://agentskills.io) (`SKILL.md`): see your tool's documentation for its skills folder.

Restart the tool or start a new session. No extra dependencies.

## How to use

```
Give me a product overview of this PRD
Draw a feature map for this system
Tóm tắt tổng quan sản phẩm và vẽ bản đồ tính năng
```

## Output

| You ask for | Sections | File (in `product-overview/`) |
|---|---|---|
| A "simple" overview | 1. Product overview | `yyyy-mm-dd_hh-mm-ss-product-name-overview.md` |
| A feature map / deep analysis | 1. Product overview + 2. Feature hierarchy map | `yyyy-mm-dd_hh-mm-ss-product-name-feature-map.md` |

- **Product overview:** product purpose, problem solved, target users (personas and their permissions).
- **Feature hierarchy map:** `- [ ] **Epic**` → `- [ ] *Feature*`, each with a one-line description of its role.

## Language

Written in the language you use (Vietnamese or English). The terms `Epic` and `Feature`, the checkbox syntax and the file names stay the same.

## Author

tuyenvo224
