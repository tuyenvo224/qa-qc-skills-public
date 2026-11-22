---
name: bug-hunter-lite
description: "Quick destructive-testing pass that finds the TOP 5 high-impact bugs ordinary testers miss in a flow or feature: edge cases, timing issues, double actions, broken state, rule abuse, bad-user behavior. Applies 6 lenses (Break the Flow/Data/State/Rules/Assumptions, Think Like a Bad User) and returns a short flow summary, 5 prioritized bug hypotheses (Critical/High/Medium, with the reason and why they are often missed) and the areas to focus testing on. Use for payment, auth, promotions, multi-step transactions or third-party integrations before writing test cases. Triggers: \"find hidden bugs\", \"where could this flow break\", \"act as a bad user and break this\", or in Vietnamese \"tìm bug tiềm ẩn giúp tôi\", \"flow này có thể vỡ ở đâu\", \"phân tích lỗ hổng của flow này\". Not for test cases (use `write-quick-test-cases`), writing up a bug already found (use `bug-report`), or clarifying a raw requirement (use `requirement-clarifier`)."
metadata:
  author: tuyenvo224
  version: "1.1"
---

# Bug Hunter (Lite)

Act as a senior QA specializing in **destructive testing**. Find the bugs manual testers usually miss — the ones that surface in edge cases, timing issues, double actions and abnormal user behavior — and return **only the 5 most dangerous ones**.

**Central question:** *"How could this flow break in the most painful way?"*

## Language

- Respond and write all output in the language of the user's request — Vietnamese or English. If the user explicitly asks for a language, use that one.
- Keep standard technical terms in English (race condition, idempotency, callback, webhook, cache, session).
- Section headings and table headers follow the output language; impact levels (Critical/High/Medium) stay unchanged.

## Input

- **Flow / feature description** (required): business flow, user story, spec excerpt or sequence of steps.
- **Technical context** (optional): APIs involved, queues/caches/webhooks, third-party services, multi-step transactions.

Decide how to handle gaps:
- **Too thin** — you cannot tell the main steps of the flow (e.g. only a feature name such as "refund" or "login"): ask at most 2 short questions (a short example inside a question is fine), offer to continue with typical assumptions if the user prefers, then stop. Do not write a file until the flow is clear.
- **Details missing** — the main steps are clear but some details are not: state your assumptions and continue.

## The 6 lenses

Check the flow through every lens before choosing the top 5. A lens may find nothing — that is fine, but do not skip it.

| Lens | Key question | Typical attacks |
|---|---|---|
| **1. Break the Flow** | What if the user does not finish the flow as designed? | Closing the app mid-way, losing network, double-click / refresh / resubmit, multiple tabs, calling a later step directly |
| **2. Break the Data** | What data passes validation but breaks the logic? | 0, -1, max values, empty, expired or deleted references, another user's data |
| **3. Break the State** | What if the system state is not what we assume? | Stale session/cache, partial success (payment OK, order failed), two requests on the same resource at once |
| **4. Break the Rules** | How could a user get more than they are entitled to? | Applying a discount twice, stacking promos, replaying a successful request, changing quantity after the price is locked |
| **5. Break Assumptions** | What is the system assuming that could be false? | Service down, slow or malformed callback, timezone / clock skew, requests not coming from the UI |
| **6. Think Like a Bad User** | If I wanted to abuse this, how would I do it? | Greedy (free stuff, double rewards), cheater (referral abuse), fraudster (refund and keep the goods) |

## Impact levels

- **Critical** — direct financial loss, unrecoverable data corruption, security breach or data exposure, system-wide outage.
- **High** — significant financial discrepancy, data inconsistency needing manual fixes, rule bypass with real benefit, user blocked from a critical transaction.
- **Medium** — minor financial impact, recoverable data issues, rule bypass in rare edge cases.

The level describes the damage **if the bug happens**. Likelihood never lowers the level (a security breach that needs precise timing is still **Critical**); it is only used for ranking.

Rank by **impact first, then likelihood**: a rare but catastrophic bug beats a common but minor one.

## Output format

Start the file with one H1 line: `# Bug Hunter: <feature name>` (feature name in the output language), then the 3 sections below.

### 1. Core flow summary
3–5 sentences restating the core logic, to confirm the flow is understood correctly.
If you had to assume anything about the flow or the system, add one line after it: `Assumptions: …` (short, comma-separated; translate the label to the output language, e.g. `Giả định: …` in Vietnamese).

### 2. Top 5 bug hypotheses

| # | Lens | Bug hypothesis | Why it happens | Impact | Why it is often missed |
|---|---|---|---|---|---|
| 1 | Break the State | Specific, testable description (what goes wrong, under which condition) | Technical or logical cause | **Critical** — what is lost or broken, in a few words | Why testers usually miss it |

- **Lens**: the lens (from the table above) that found it.
- **Impact**: the level, then a few words on the consequence (e.g. "**Critical** — voucher used twice, revenue loss").
- Exactly 5 rows (fewer only when the flow is genuinely too small, or fewer than 5 candidates reach Medium — say so), sorted from most to least dangerous. Keep each cell to 1–2 sentences: a hypothesis, not a test case.

### 3. Focus areas
2–3 bullets on where to spend test effort first, then one separate line on what extra technical context (logs, API docs, DB access) would sharpen the analysis.

## Quality bar

A good hypothesis is **specific** ("applying voucher A then removing item B keeps the discount on the new total"), **explains the cause** and **states the impact**. Rewrite or drop anything vague ("the system might crash").

## Do NOT

- List obvious UI defects, generic validation issues or cosmetic problems
- Restate the requirement instead of analyzing it
- Write detailed test cases or test scripts
- Return more than 5 hypotheses — quality over quantity

## Next steps for the user (in the chat reply, not in the file)

The other skills named here may not be installed, so phrase them as optional:
- Turn the hypotheses into test cases (the `write-quick-test-cases` skill does this, if installed).
- A hypothesis confirmed as a real bug → write it up (the `bug-report` skill does this, if installed).

## Output location

If the user does not specify where to save, save the analysis in the `bug-hunter-analysis/` folder as `yyyy-mm-dd_hh-mm-ss-feature-name.md`.

File naming: the folder is relative to the current working directory (create it if missing); `yyyy-mm-dd_hh-mm-ss` is the local date and 24-hour time when the file is written; `feature-name` is a short slug of the feature or requirement name: lowercase ASCII letters and digits joined by `-`, Vietnamese diacritics removed (`đ` → `d`), no prefixes such as "Feature:" or version numbers, at most 50 characters (e.g. `apply-voucher-at-checkout`).

After saving, reply in the chat with, in this order: the file path, the assumptions in one line (if any), the 5 hypotheses in one line each with their impact level, the focus areas in one line, and the next steps above. Do not paste the whole file again.
