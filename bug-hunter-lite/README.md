# bug-hunter-lite

A quick **destructive-testing** pass over a flow or feature: looks at it through 6 lenses and returns the **top 5 high-impact bugs** that ordinary testing tends to miss — edge cases, timing issues, double actions, broken state, rule abuse, bad-user behavior.

Vietnamese version: [README.vi.md](README.vi.md). The AI agent follows `SKILL.md`.

## Skill structure

```
bug-hunter-lite/
  ├── SKILL.md      ← instructions for the AI agent
  ├── README.md     ← this file
  └── README.vi.md  ← Vietnamese user guide
```

## When to use

- Before writing test cases for risky flows: payment, authentication, promotions/discounts, multi-step transactions, third-party integrations.
- When you want to know "where could this flow break in the most painful way?".

Not for: writing test cases (use `write-quick-test-cases`), writing up a bug you already found (use `bug-report`), or clarifying a raw requirement (use `requirement-clarifier`). Not useful for simple UI text changes or static pages.

## Installation

Copy the `bug-hunter-lite` folder into the skills folder of your AI tool:
- **Claude Code:** `~/.claude/skills/` (all projects) or `<your-project>/.claude/skills/` (one project).
- **Other tools** that support [Agent Skills](https://agentskills.io) (`SKILL.md`): see your tool's documentation for its skills folder.

Restart the tool or start a new session. No extra dependencies.

## How to use

```
Find hidden bugs in this checkout flow: <paste flow>
Act as a bad user and break this voucher feature
Flow này có thể vỡ ở đâu?
```

Add technical context if you have it (APIs, queues, caches, webhooks, third-party services) — the analysis gets sharper. If you only give a feature name, the skill asks up to 2 short questions first; if only some details are missing, it states its assumptions and continues.

## The 6 lenses

| Lens | Key question |
|---|---|
| Break the Flow | What if the user does not finish the flow as designed? |
| Break the Data | What data passes validation but breaks the logic? |
| Break the State | What if the system state is not what we assume? |
| Break the Rules | How could a user get more than they are entitled to? |
| Break Assumptions | What is the system assuming that could be false? |
| Think Like a Bad User | If I wanted to abuse this, how would I do it? |

## Output

Saved in `bug-hunter-analysis/` as `yyyy-mm-dd_hh-mm-ss-feature-name.md`:

1. **Core flow summary** — 3–5 sentences, to confirm the flow is understood correctly, plus a line of assumptions if any were made.
2. **Top 5 bug hypotheses** — table: the lens that found it, hypothesis, why it happens, impact (Critical / High / Medium + the consequence), why it is often missed. Ranked by impact first, then likelihood.
3. **Focus areas** — where to spend test effort first.

## Language

Answers in the language you write in (Vietnamese or English). Impact levels (Critical/High/Medium) and technical terms (race condition, idempotency, cache…) stay in English.

## Author

tuyenvo224
