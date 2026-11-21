# markdown-to-excel

Converts a **Markdown file into an Excel workbook** (.xlsx) with a bundled script — each Markdown table becomes its own formatted sheet.

Vietnamese version: [README.vi.md](README.vi.md). The AI agent follows `SKILL.md`.

## Skill structure

```
markdown-to-excel/
  ├── SKILL.md            ← instructions for the AI agent
  ├── README.md           ← this file
  ├── README.vi.md        ← Vietnamese user guide
  └── scripts/
        └── md_to_xlsx.py ← converter (input.md [output.xlsx] --lang en|vi)
```

## When to use

- You have test cases, data lists or checklists as Markdown tables and need them in Excel.

Not for: writing new test cases (use `write-quick-test-cases`, which has its own Excel export), or reading/editing existing Excel files.

## Installation

Copy the `markdown-to-excel` folder into the skills folder of your AI tool:
- **Claude Code:** `~/.claude/skills/` (all projects) or `<your-project>/.claude/skills/` (one project).
- **Other tools** that support [Agent Skills](https://agentskills.io) (`SKILL.md`): see your tool's documentation for its skills folder.

Restart the tool or start a new session.

**Requirements:** Python 3.8+ and `openpyxl` (`pip install openpyxl`). Your AI tool must be able to run Python commands (`python`, or `python3` on macOS/Linux).

## How to use

```
Convert test-cases/login.md to Excel
Export these tables to xlsx
Chuyển file md này sang excel
```

If several `.md` files could match, the agent asks which one instead of guessing.

## Output

One `.xlsx` file — by default next to the source file, same name. You can also give an output path.

- Each Markdown table → one sheet, named after the heading right before it. A table without its own heading gets the file name (if it is the only table) or `Table<N>` by its position (e.g. `Table2`).
- Header row: bold, blue background, white text, frozen, with auto-filter.
- `<br>` → line break inside the cell; Markdown formatting (`**bold**`, `` `code` ``, links) cleaned.
- Column widths auto-fit (max 60).
- A file with no table → its text is written to one sheet, one line per row.
- Table content is copied as-is, never translated.

## Language

Answers in the language you write in. `--lang vi` only changes the few fixed texts the script writes (fallback header, `Bảng1`… sheet names).

## Author

tuyenvo224
