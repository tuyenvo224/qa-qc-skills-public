---
name: bug-report
description: "Writes a ready-to-paste bug report for any tracker (Jira, Redmine, GitHub Issues, Linear…): a one-line title in codeblock 1 and a 7-section body in codeblock 2 (Environment, Preconditions, Steps to Reproduce, Actual Result, Expected Result, Reproducibility, Notes). Takes the tester's description of the failure (cases, observed result, a passing case to compare with), optionally a spec, screenshots or environment info; when a spec is given, cites its rule IDs (BR/FR/UC/AC) as the basis for Expected Result. Runs straight to the result without asking for confirmation and never creates issues itself. Use for \"log a bug\", \"write a bug report\", \"report this bug\", \"rewrite this bug for Jira\", or in Vietnamese \"log bug\", \"viết bug\", \"viết lại bug để post lên Jira/Redmine\", \"đang có bug chỗ này…\". Do NOT use to hypothesize hidden bugs or to write test cases."
metadata:
  author: tuyenvo224
  version: "1.1"
---

# Bug Report

**Input:** the user's description of a failure. Optionally a spec, screenshots, test environment details.
**Output:** a bug title + body following the template, for the user to **copy and paste** into their tracker.

Run straight to the result: do **not** present a plan and do **not** wait for confirmation. Stop only if a spec the user points to cannot be read.
This skill never creates or edits issues in any tracker — the user reviews the report and posts it.

## Language

Reply in the language of the user's request — Vietnamese or English — unless the user explicitly asks for another language. The title, the body and the "Check before posting" list follow that language.

- **Section labels**: use the labels in `references/template.md`. In Vietnamese, keep the English label in parentheses (`**I. Môi trường (Environment)**`); in English, use the English label only.
- **Always kept as-is**: the tags `[UI]` / `[Function]`, the environment tag, rule IDs (`BR-xxx`, `FR-xx`, `UC-xx`, `AC-xx`, `§x.y`), `Always` / `Sometimes` / `Rarely`, and the exact text of buttons, labels and messages from the product or spec.
- Keep the spec's own technical terms (Remember, Session, Active, Blocked…) instead of translating them.

## Step 1 · Gather the facts

From the user's description and the conversation (spec, earlier analysis), identify:
- **Product / Module**: e.g. `DemoShop` / `Login`.
- **Failing case**: conditions, actions, the actual result observed.
- **Passing comparison case** (if any): goes into Notes — it helps developers narrow the cause.
- **Environment**: URL/build, OS, browser/device, test account, and the environment name (STG, UAT, PROD…).
- **Screenshots**: file names or "attachment #n", recorded in Notes so the user remembers to attach them.

Several **independent** failures → several bugs, one pair of codeblocks each. Cases with the same cause that differ in one condition (e.g. ticked / not ticked) → one bug: the failing case is the main one, the passing case goes into Notes.

## Step 2 · Find the basis in the spec

- **Spec given** (pasted text, a local file, or a link you can read with the tools available): read it. If a link cannot be read (login required, tool missing), say so and ask the user to paste the relevant part — then stop.
- **Spec already read in this conversation**: reuse it, do not fetch again.
- Find every rule about the expected behavior; quote the **exact ID** (BR-xxx, FR-xx, UC-xx, AC-xx, §section) with a short summary that keeps the meaning.
- State why the actual result breaks the rule, e.g. "no rule requires condition X".
- **No spec**: write Expected from the user's description and add to Notes: "Expected based on the tester's description, not yet checked against a spec".
- Spec **silent or ambiguous** about this behavior: do not conclude it is a bug. Write in Notes "Spec does not define this clearly — needs BA/PO confirmation", and raise it in the final check.

## Step 3 · Write the bug

Follow **[references/template.md](references/template.md)** exactly: 7 sections I–VII. A full example is in that file.

**Title**
- Format: `[<ENV>][<UI|Function>][<Product>] [<Module>] <condition> → <wrong behavior>` (in Vietnamese the connector may be "thì" instead of `→`).
  - `<ENV>` is the environment the user names (`[STG]`, `[UAT]`, `[PROD]`, `[DEV]`…). If the user does not name one, write `[<ENV>]` and list it in the final check.
  - Right after the environment tag comes **exactly one** bug-type tag: `[UI]` or `[Function]`, no space between tags.
- One line that tells what is wrong without opening the bug. Never generic ("Remember bug").
- Examples:
  - `[STG][UI][DemoShop] [Login] Selecting text in the "Work email" field → selection highlight is too faint to see which text is selected`
  - `[STG][Function][DemoShop] [Login] Logging in on another browser without ticking "Remember me" → Remember on the old browser is not revoked`

**Choosing `[UI]` / `[Function]`**
- `[UI]`: display problem, logic is correct — colors, fonts, sizes, alignment, layout, icons, spelling/wording of labels, responsive, hover/focus/selection states.
- `[Function]`: behavior/logic problem — validation, data handling, navigation, session/Remember, permissions, a message shown in the wrong situation or not shown, wrong API response.
- Borderline:
  - Message shown **at the right time but with wrong text** → `[UI]`.
  - Message shown **at the wrong time, or not shown** → `[Function]`.
  - Unsure → still pick one, and give the reason in "Check before posting".

**Body**
- **I. Environment**: anything the user did not give stays `<...>` with a hint (e.g. `<e.g. Chrome 1xx>`). Never fill it in yourself. If the user gave only part of a value, keep that part and add a placeholder for the rest (e.g. `Chrome <version>`).
- **II. Preconditions**: account state, data, number of browsers/devices needed.
- **III. Steps to Reproduce**: numbered, one action per step. State the data entered, what is **ticked / NOT ticked**, and intermediate results when useful (`→ login succeeds`). The last step is the one that reveals the bug.
- **IV. Actual Result**: **only what the user observed**. No inferred consequences.
- **V. Expected Result**: the correct behavior, then a line "Based on <spec name + version>:" followed by the rule IDs. If the spec has no version, write its name followed by "(no version)" — never invent one.
- **VI. Reproducibility**: Always / Sometimes / Rarely as the user says. If unknown, write `Always` and list it in the final check.
- **VII. Notes**:
  - The passing comparison case (marked PASS).
  - Suspected cause: labelled "Suspected", one sentence.
  - Unverified consequences: "Needs further checking: …".
  - Spec referenced: name, source, version, date — write "(no version)" / "(no date)" for anything the spec does not state.
  - **Mandatory** line `- Attachments: <file name> (<what it shows>) · …` — a fixed line of the template. Without screenshots write `- Attachments: none (<reason>)`. Attachments mentioned outside codeblock 2 will not reach the tracker.

**Style:** short sentences; button names, labels and messages in double quotes, verbatim.

**Tracker format:** Markdown by default (works in GitHub Issues, Linear, GitLab, Redmine with Markdown, and the Jira Cloud editor when pasted). If the user asks for **Jira wiki markup**, convert: `**bold**` → `*bold*`, numbered list → `#`, bullets → `*`, inline code → `{{code}}`.

## Step 4 · Return the result

In this order, with no long introduction (labels such as **Title:** / **Body:** / "Check before posting" follow the user's language, e.g. **Tiêu đề:** / **Nội dung:** / "Kiểm tra trước khi post"):

1. One line: `Written for: developers/testers reading the tracker. Fill in the <...> fields.` — in Vietnamese: `Viết cho: dev/tester đọc trên tracker. Điền các ô <...> còn trống.`
2. `**Title:**` + codeblock 1 containing **only** the title.
3. `**Body:**` + codeblock 2 containing all 7 sections.
   - If the body has a line starting with ``` (logs, code), use `~~~` for codeblock 2 so it does not break.
4. A short **"Check before posting"** list (max 5 lines; merge related items if there are more): **the first line is always "Attachments to add: <file names + folder>"** — in Vietnamese "Ảnh cần đính kèm: …"; write `<folder>` if the user did not say where the files are, or "no attachments" / "không có ảnh"; then the empty `<...>` fields (including `[<ENV>]`), any assumption about the observed behavior, any "Needs further checking" item that should move to Actual once confirmed, and spec questions for BA/PO.

Several bugs → repeat items 2–3 for each, numbered `Bug 1`, `Bug 2`, then one combined check list at the end.

## Do NOT
- Do not create or edit issues in any tracker, or call any write API.
- Do not invent observed behavior, environment details or rule IDs.
- Do not print tokens, passwords or API keys — replace them with `<...>`.
