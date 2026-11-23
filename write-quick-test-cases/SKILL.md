---
name: write-quick-test-cases
description: "Quickly writes a basic test case set (Positive/Negative/Boundary/Security) from a short requirement or user story and exports it to an Excel \"TEST SCENARIOS\" sheet (metadata block, cases grouped by Module/Function as \"I.\"/\"II.\" groups, separate Precondition/Test data/Steps/Expected result columns, blank execution columns). Use when the user wants a lightweight, ready-to-use Excel test case sheet without deep coverage analysis, e.g. \"write test cases for this feature\", \"quick test cases for this user story\", \"viết test case nhanh\", \"viết test case cho tính năng này\", \"xuất test case ra Excel\". Do NOT use for converting an arbitrary Markdown file to Excel."
metadata:
  author: tuyenvo224
  version: "1.1"
---

## Language

Respond to the user and write all output — the test case content and the Excel labels — in the language of the user's request (Vietnamese or English). If the user explicitly asks for a specific language, use that one. Keep standard technical terms in English (Positive/Negative, Precondition, Test data, Happy Path...). Pass the matching `--lang en|vi` to the conversion script (see "Output").

### [ROLE & GOAL]
You are a **Senior QA/Software Testing Engineer**. Your task is to take the feature document/requirement (Requirement/User Story) the user provides and quickly write a compact, ready-to-run set of Test Cases covering the main scenario groups below — a practical base set, not an exhaustive coverage analysis.

---

### [FEATURE / REQUIREMENT UNDER TEST]
Take these from the user's message (a pasted description, a file, or the conversation):
- **Feature name** — use it in the H1 heading of the Markdown file (see "Output"). If the user gives none, derive a short name from the requirement.
- **Description / User Story** — the feature description, business flow or Acceptance Criteria to cover.
- **Ticket** (optional) — a ticket URL or ID, written in the H1 heading.

If the requirement is too thin (e.g. only a feature name, with no description, rules or acceptance criteria), ask at most 2 short questions and stop: do not create any file until the user answers or tells you to proceed with assumptions. Otherwise state assumptions and mark them as needing confirmation (see "ADDITIONAL RULES").

---

### [TEST SCOPE]
Cover the following scenario groups:
1. **Positive Cases:** Successful scenarios / main flow (*Happy Path*).
2. **Negative Cases:** Failure scenarios / invalid input / empty fields.
3. **Boundary / Edge Cases:** Boundary scenarios / extreme data sizes.
4. **Security / Permission Cases:** Authorization / basic security scenarios (if applicable).

---

### [OUTPUT FORMAT]
First draft the content as a **Markdown table** with the following columns (this is an intermediate step — the final deliverable to the user is the Excel file, see the "Output" section at the end of this file):

| No. | Module/Function | Test objective | Precondition | Test data | Test steps | Expected result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[Sequence number]` | `[Module/screen/sub-function name]` | `[Positive/Negative/Boundary/Security] [Scenario summary]` | `[Precondition, leave blank if none]` | `[Concrete input data]` | `[Steps, numbered 1. 2. 3... separated by <br>]` | `[Expected result]` |

When writing in Vietnamese, use the Vietnamese column names instead: `STT | Module/Function | Mục đích kiểm thử | Precondition | Test Data | Các bước thực hiện | Kết quả mong muốn`. The script accepts either set of header names.

How to fill it in:
- **Module/Function**: consecutive rows with the same value are merged into one Group when converted to Excel (shown as "I. <name>", "II. <name>"...) — so test cases for the same module/screen must be placed **next to each other**, not interleaved with other modules.
- **Test objective**: always starts with a classification tag in square brackets `[Positive]`/`[Negative]`/`[Boundary]`/`[Security]` (the Excel sheet has no separate Type column; this tag replaces it).
- **Precondition** and **Test data** are 2 separate columns in the Excel sheet — do not merge them into Steps.

**The Excel layout** (sheet `TCs`) is built by the bundled script: a metadata block at the top (Screen/Feature name, Spec link, Ticket link, Prototype, Domain, Account, Tester...), then the test cases grouped as "I. <module>", "II. <module>"... The main table has exactly 10 columns in this order: Test case No. | Test objective | Precondition | Test data | Test steps | Expected result | Actual result | Bug ID | Notes | Tester — **the last 4 columns (Actual result/Bug ID/Notes/Tester) stay blank; they are for the tester to fill in during test execution. Do NOT pre-fill them.** (In Vietnamese output the same columns are labeled STT trường hợp kiểm thử | Mục đích kiểm thử | Precondition | Test data | Các bước thực hiện | Kết quả mong muốn | Kết quả hiện tại | Mã lỗi | Ghi chú | QC thực hiện.)

---

### [ADDITIONAL RULES]
- **Ordering:** Within each Group (module/screen), put *Positive Cases* first, then *Negative*, *Boundary*, *Security*.
- **Language:** follow the "Language" section above.
- **Quality:** Clear and easy to understand so a tester can execute right away without asking follow-up questions.
- **Flag expected results that need confirmation:** If an *Expected result* is based on an assumption or still needs to be confirmed with the PO/BA, always state it explicitly in that cell (or in the Precondition/Test data cell if that is where the assumption lives), in the form `(assumed: <what> – needs confirmation)`, adding the question ID when the user has one from a clarification question list (e.g. `(needs confirmation QH-02)`) — in Vietnamese: `(giả định: <nội dung> – cần confirm)` / `(cần confirm QH-02)`. The script relies on these keywords to highlight the cell in Excel automatically (see "Output"), so do not phrase it any other way without a keyword (e.g. "might be…", "up to DEV") — such a cell will not be highlighted.

# Output

1. **Write the Markdown content** following the table in "OUTPUT FORMAT", and save it in a `test-cases-for-review/` folder in the user's working directory (create it if missing), with the file name:
   - `yyyy-mm-dd_hh-mm-ss-feature-name.md`
   - The first line is an H1 heading of the form `# Test Case: <Feature name> (<ticket>)` — the script reads this line to fill the feature name and the ticket link into the metadata block of the Excel file. `<ticket>` is optional and can be:
     - a full URL (e.g. `https://jira.example.com/browse/PROJ-123`) → written as a clickable link;
     - a bare ID (e.g. `#123` or `PROJ-123`) → written as plain text, unless the user has given a ticket URL pattern, in which case pass it with `--ticket-url-template "https://<tracker>/.../{id}"` to turn the ID into a link.

2. **Convert to Excel with the bundled script** — do NOT build the Excel file by hand and do NOT write a new conversion script:
   ```
   python "<this skill's folder>/scripts/testcase_md_to_xlsx.py" "test-cases-for-review/yyyy-mm-dd_hh-mm-ss-feature-name.md" --lang en
   ```
   If the skill was loaded without a folder on disk, save the script content exactly as received to a temporary file outside the working directory and run that file directly (`python "<temp file>" "<md file>" --lang <en|vi>`, which works in any shell), then delete the temp file; the script needs no other file. If the `python` command is not found (common on macOS/Linux), use `python3` instead. If `openpyxl` is missing, run `python -m pip install openpyxl` (or `python3 -m pip …`) and try again.
   - `--lang en|vi` (default `en`): language of all fixed labels in the Excel file (title, metadata labels, column headers, change-log note, fallback group name). Use `vi` when the user wrote in Vietnamese (or asked for Vietnamese), `en` otherwise.
   - `--qc-name "<name>"` (optional): tester name for the "Tester" metadata cell; leave it out if the user has not given a name.
   - `--ticket-url-template "<url with {id}>"` (optional): see step 1.

   The script builds the whole file itself (no template file needed): labels in the chosen language, the metadata block (feature name, ticket link, tester, creation date), Module/Function groups ("I. ...", "II. ..."), continuous numbering, wrapped text with fitted row heights, and the 4 execution columns left blank. If the Markdown has several test case tables (e.g. one per module), all of them are read in file order.
   **Highlighting cells that need confirmation:** when any column of a test case contains a confirmation keyword, its **Expected result** cell gets a light-orange fill. Keywords — English: `needs confirmation`, `to be confirmed`, `TBC`, `TBD`, `confirm with`, `pending confirmation`, `assumption`, `assumed`, `unclear`, `not finalized`; Vietnamese (with diacritics): `cần confirm`, `confirm lại`, `chờ confirm`, `cần xác nhận`, `chờ xác nhận`, `giả định`, `giả sử`, `tạm dùng`, `tạm hiểu`, `chưa chốt`, `chưa rõ`; question IDs `QH-xx`/`QM-xx`/`QL-xx`. The script prints which test case numbers were highlighted — use that list in your report to the user.
   If the script fails or reports a skipped table, do NOT edit the script or write a separate one: fix the Markdown (column names, table layout) and run it again; if it still fails, tell the user the error message.

   File naming: `yyyy-mm-dd_hh-mm-ss` is the local date and 24-hour time when the file is written; `feature-name` is a short slug of the feature or requirement name: lowercase ASCII letters and digits joined by `-`, Vietnamese diacritics removed (`đ` → `d`), no prefixes such as "Feature:" or version numbers, at most 50 characters (e.g. `apply-voucher-at-checkout`).

3. **Give the user the paths of both files** (a short chat reply — do not paste the whole table) — the `.xlsx` file is the official deliverable; the `.md` file is kept for quick reference/diff when needed. Include the number and test case numbers of the Expected result cells highlighted as needing PO/BA confirmation (taken from the script output).
