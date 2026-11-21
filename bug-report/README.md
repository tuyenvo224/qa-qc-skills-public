# bug-report

Writes a **ready-to-paste bug report** for any tracker (Jira, Redmine, GitHub Issues, Linear…) from your description of a failure: a one-line title and a 7-section body, with the expected result backed by rule IDs from the spec when you have one.

Vietnamese version: [README.vi.md](README.vi.md). The AI agent follows `SKILL.md`.

## Skill structure

```
bug-report/
  ├── SKILL.md              ← instructions for the AI agent
  ├── README.md             ← this file
  ├── README.vi.md          ← Vietnamese user guide
  └── references/
        └── template.md     ← section labels (EN/VI), body frames, short and full examples
```

## When to use

- You found a bug while testing and want it written up clearly and consistently.
- You want to rewrite a rough bug note before posting it.

Not for: guessing hidden bugs (use `bug-hunter-lite`) or writing test cases (use `write-quick-test-cases`).

The skill **never creates or edits issues** in any tracker — you review the report and paste it yourself. It runs straight to the result without asking for confirmation.

## Installation

Copy the `bug-report` folder into the skills folder of your AI tool:
- **Claude Code:** `~/.claude/skills/` (all projects) or `<your-project>/.claude/skills/` (one project).
- **Other tools** that support [Agent Skills](https://agentskills.io) (`SKILL.md`): see your tool's documentation for its skills folder.

Restart the tool or start a new session. No extra dependencies.

## How to use

Describe what happened — the failing case, what you saw, and (if you have one) a similar case that works. Add the environment, screenshots and the spec if available.

```
Log a bug: on STG, login with a password containing "#" shows "Wrong password"
Rewrite this bug for Jira wiki markup: <paste notes>
Viết bug giúp tôi: <mô tả lỗi>
```

## Output

Returned in the chat (no file):

1. **Title** (codeblock 1): `[<ENV>][<UI|Function>][<Product>] [<Module>] <condition> → <wrong behavior>`
   - `<ENV>` is the environment you name (STG, UAT, PROD…); if you do not name one it stays `[<ENV>]`.
   - `[UI]` for display problems, `[Function]` for behavior/logic problems.
2. **Body** (codeblock 2): I. Environment · II. Preconditions · III. Steps to Reproduce · IV. Actual Result · V. Expected Result · VI. Reproducibility · VII. Notes (incl. a mandatory **Attachments** line).
3. **Check before posting** — up to 5 lines: attachments to add, empty `<...>` fields, assumptions to verify, questions for the BA/PO.

Rules the skill follows: Actual Result contains only what you observed; missing details stay as `<...>` (never invented); rule IDs (BR/FR/UC/AC) are quoted exactly; if the spec is silent or ambiguous, it says so instead of calling it a bug. Format is Markdown by default, or Jira wiki markup on request.

## Language

Written in the language you use. In Vietnamese, section labels keep the English name in parentheses (e.g. `I. Môi trường (Environment)`). Tags, rule IDs, `Always/Sometimes/Rarely` and exact UI texts stay as-is.

## Author

tuyenvo224
