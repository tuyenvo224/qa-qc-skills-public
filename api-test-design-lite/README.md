# api-test-design-lite

Reads an OpenAPI/Swagger spec and generates a **core set of API test cases as Markdown tables**, ready for QA review.
This file is the user guide (English). Vietnamese version: [README.vi.md](README.vi.md). The AI agent follows `SKILL.md`.

## Skill structure

```
<skills-folder>/api-test-design-lite/
  ├── SKILL.md      ← instructions for the AI agent
  ├── README.md     ← user guide (English, this file)
  ├── README.vi.md  ← user guide (Vietnamese)
  └── references/
        └── lite-rules.md  ← coverage rules, file layout, columns, assertion clauses, test data, worked example
```

## What it covers

| Test Type | Cases |
|---|---|
| Happy | One success per endpoint; required-only and all-fields on write endpoints; response fields asserted; secrets absent |
| Validation | Missing / wrong type for every required input; format, pattern, enum violations; just outside declared limits; empty `{}` body |
| Auth | Missing and invalid credential per protected endpoint; 403 per denied role |
| NotFound | Non-existent id per path id |
| Boundary | Exactly at each declared limit |

Not covered (listed in every output file): security payloads (injection, XSS, SSRF…), mass assignment, BOLA, expired/tampered tokens, exploratory limits, side-effect checks, business rules, HTTP-level behavior, file uploads.

## Installation

Copy the `api-test-design-lite` folder into the skills folder of your AI tool:
- **Claude Code:** `~/.claude/skills/` (all projects) or `<your-project>/.claude/skills/` (one project).
- **Other tools** that support [Agent Skills](https://agentskills.io) (`SKILL.md`): see your tool's documentation for its skills folder.

Restart the tool or start a new session. No extra dependencies.

## How to use

```
Generate API test cases from ./openapi.yaml
Sinh test case API từ file swagger này: https://example.com/openapi.json
```

Output: one file `test-case-api/yyyy-mm-dd_hh-mm-ss-<api-name>.md` (in your current working directory, unless you name another location). Specs with more than 10 endpoints get a coverage plan first; reply "ok" or adjust it. Without a spec (only a description), no file is created: the skill asks for the spec instead of guessing.

## Language

Free text (Description, Pre-condition, Notes, Assumptions, messages) follows the language you write in. Column headers, Test Type, Priority, assertion clauses and markers stay in English so files stay consistent.

## Output format

14 columns: `TC_ID | Module | Endpoint | Method | Test Type | Priority | Pre-condition | Description | Headers | Path/Query Params | Request Body | Expected Status | Expected Response | Notes`. See the worked example in `references/lite-rules.md`.

## Author

tuyenvo224
