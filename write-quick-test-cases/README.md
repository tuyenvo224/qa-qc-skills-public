# write-quick-test-cases

Quickly writes a **basic test case set** (Positive / Negative / Boundary / Security) from a short requirement or user story and exports it to a **ready-to-use Excel test sheet** built from the bundled template.

Vietnamese version: [README.vi.md](README.vi.md). The AI agent follows `SKILL.md`.

## Skill structure

```
write-quick-test-cases/
  ├── SKILL.md                          ← instructions for the AI agent
  ├── README.md                         ← this file
  ├── README.vi.md                      ← Vietnamese user guide
  ├── assets/
  │     └── Template_TCs.xlsx           ← Excel template (layout, styles)
  └── scripts/
        └── testcase_md_to_xlsx.py      ← Markdown → Excel converter (--lang en|vi, --qc-name, --ticket-url-template)
```

## When to use

- You need a lightweight test case sheet fast, without deep coverage analysis.
- You want the cases in a standard Excel layout that testers can execute and fill in directly.

Not for: converting an arbitrary Markdown file to Excel (use `markdown-to-excel`).

## Installation

Copy the `write-quick-test-cases` folder into the skills folder of your AI tool:
- **Claude Code:** `~/.claude/skills/` (all projects) or `<your-project>/.claude/skills/` (one project).
- **Other tools** that support [Agent Skills](https://agentskills.io) (`SKILL.md`): see your tool's documentation for its skills folder.

Restart the tool or start a new session.

**Requirements:** Python 3.8+ and `openpyxl` (`pip install openpyxl`). Your AI tool must be able to run Python commands (`python`, or `python3` on macOS/Linux).

## How to use

```
Write test cases for this feature and export to Excel: <paste user story>
Quick test cases for the login screen, ticket PROJ-123
Viết test case nhanh cho tính năng này
```

Optional: give a tester name, or a ticket URL pattern (e.g. `https://jira.example.com/browse/{id}`) to turn ticket IDs into links.

## Output

Two files:

| File | Purpose |
|---|---|
| `test-cases-for-review/yyyy-mm-dd_hh-mm-ss-feature-name.md` | Markdown draft, for quick review / diff |
| Same name, `.xlsx` | **The deliverable**: the Excel test sheet |

The Excel file:
- A metadata block at the top (feature name, spec/ticket links, tester, creation date as `yyyy-mm-dd`…).
- Test cases grouped by Module/Function as "I.", "II."…, numbered continuously, Positive first, then Negative, Boundary, Security.
- 10 columns: No. · Test objective · Precondition · Test data · Test steps · Expected result · Actual result · Bug ID · Notes · Tester — the **last 4 are left blank** for test execution.
- Wrapped text with row heights fitted to content; no frozen panes.
- **Expected results that still need PO/BA confirmation** (e.g. "needs confirmation", "assumed", `QH-xx`) are **highlighted in light yellow**; the agent also lists which cases they are.

## Language

Answers in the language you write in. The Excel labels (title, metadata, column headers) switch to Vietnamese or English to match. Classification tags `[Positive]/[Negative]/[Boundary]/[Security]` and technical terms stay in English.

## Author

tuyenvo224
