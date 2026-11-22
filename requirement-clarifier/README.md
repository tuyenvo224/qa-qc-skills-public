# requirement-clarifier

Reviews a spec or feature for gaps, ambiguities and contradictions, and turns them into a **prioritized list of questions** for the BA/PO — ready to take straight into a review meeting.

Vietnamese version: [README.vi.md](README.vi.md). The AI agent follows `SKILL.md`.

## Skill structure

```
requirement-clarifier/
  ├── SKILL.md      ← instructions for the AI agent
  ├── README.md     ← this file
  └── README.vi.md  ← Vietnamese user guide
```

## When to use

- Before development or testing starts, to find what the spec does not say clearly.
- To prepare questions for a review meeting with the BA/PO.
- Input: PRD / SRS, user story, Jira ticket, free-text description, or an image / Figma / screenshot.

Not for: a test-coverage mindmap (use `requirement-to-mindmap`), hunting hidden bugs (use `bug-hunter-lite`), or test cases (use `write-quick-test-cases`).

## Installation

Copy the `requirement-clarifier` folder into the skills folder of your AI tool:
- **Claude Code:** `~/.claude/skills/` (all projects) or `<your-project>/.claude/skills/` (one project).
- **Other tools** that support [Agent Skills](https://agentskills.io) (`SKILL.md`): see your tool's documentation for its skills folder.

Restart the tool or start a new session. No extra dependencies.

## How to use

```
What should I ask the BA about this spec? <paste spec>
Prepare questions for the PO review of the attached user story
Đặt câu hỏi về feature này giúp tôi
```

## Output

A Markdown file in `questions/` named `yyyy-mm-dd_hh-mm-ss-feature-name.md`, with 3 sections:

| Section | Content |
|---|---|
| A. How I understand the feature | 3–5 bullets for the BA/PO to confirm |
| B. Questions for the BA/PO | Grouped by topic; each question has an **ID**, gap type, why it matters and priority |
| C. Top 3 questions | The 3 to ask first when time is short |

- **Question IDs:** `QH-01…` (High), `QM-01…` (Medium), `QL-01…` (Low), numbered continuously across the document — easy to refer to in the meeting ("about QH-02…") and when recording answers.
- **Gap types:** Ambiguity / Missing / Conflict / Assumption / Testability.
- Anything inferred is marked "(assumption)" and turned into a question — never presented as fact.
- If the input has no concrete rule or flow (e.g. only a feature name), no file is created: the skill asks for the spec and lists up to 3 scope questions.

## Language

Answers in the language you write in (Vietnamese or English). Question IDs, gap types and priorities (High/Medium/Low) stay in English.

## Author

tuyenvo224
