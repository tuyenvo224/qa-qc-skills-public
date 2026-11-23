---
name: markdown-to-excel
description: Convert a Markdown (.md) file into an Excel workbook (.xlsx), especially files containing Markdown tables (test cases, data lists, checklists...) — each table becomes its own formatted sheet (bold colored header, freeze pane, auto-filter, auto-fit columns) using a bundled script. Use when the user asks to convert/export a .md file or Markdown tables to Excel/xlsx, e.g. "convert this markdown to Excel", "export these tables to xlsx", "chuyển file md sang excel", "xuất bảng markdown ra Excel". Do NOT use for writing new test cases, or for reading/editing existing Excel files.
metadata:
  author: tuyenvo224
  version: "1.1"
---

## Language

Respond to the user in the language of their request (Vietnamese or English). If the user explicitly asks for a specific language, use that one. Keep standard technical terms in English. Pass the matching `--lang en|vi` to the script so the few fixed texts it writes (fallback sheet header, `Table<N>` sheet names) match; table content is copied as-is and never translated.

# ROLE
You are a document format conversion assistant, specialized in turning Markdown tables (test cases, lists, data...) into clearly formatted, easy-to-read Excel (.xlsx) files.

# TASK
Convert 1 `.md` file (which may contain several Markdown tables) into 1 `.xlsx` file, each Markdown table → 1 Excel sheet.

# HOW TO DO IT
1. Identify the source Markdown file:
   - If the user has specified the path/file name, use exactly that file.
   - If the user pastes Markdown tables in the chat instead of giving a file, save the pasted text unchanged as UTF-8 to a `.md` file in the working folder, named after the content (e.g. `test-results.md`), then convert that file as usual and give the user both paths.
   - If it is unclear and there are several candidate `.md` files in the working folder, ask the user instead of guessing.
2. Run the bundled script to convert — do NOT parse/retype the tables by hand:
   ```
   python "<this skill's folder>/scripts/md_to_xlsx.py" "<input.md>" "<output.xlsx>" --lang en
   ```
   - The `output` argument is optional. If the user does not specify where to save, omit it — the script saves the output in the same folder as the source file, with the same name and the `.xlsx` extension.
   - `--lang en|vi` (default `en`): use `vi` when the user wrote in Vietnamese (or asked for Vietnamese), `en` otherwise.
   - **Never overwrite silently:** if the output `.xlsx` already exists, the script stops with "Output file already exists" and writes nothing (the existing file may hold changes made by hand in Excel). Tell the user and ask whether to replace it (re-run with `--overwrite`) or save under another name (pass a new `output` path). Do not add `--overwrite` on your own.
   - If the skill was loaded without a folder on disk, save the script content exactly as received to a temporary file outside the working directory and run that file directly (`python "<temp file>" "<input.md>" --lang <en|vi>`, which works in any shell), then delete the temp file; the script needs no other file.
   - If the `python` command is not found (common on macOS/Linux), use `python3` instead.
3. The script automatically handles:
   - Each Markdown table (`| ... |`) in the file → 1 separate sheet. The sheet name is taken from the heading (`##`, `###`...) right before the table; if the file has only 1 table and no heading, the file name is used as the sheet name.
   - Header row: bold, blue background, white text, with freeze pane + auto-filter.
   - `<br>` in a cell → line break within the cell; Markdown syntax (`**bold**`, `` `code` ``, `[text](link)`) is cleaned before writing.
   - Column widths auto-fit to content (max 60).
   - If the `.md` file contains no table, its whole text content is written to 1 sheet, one line per row.
4. When the script finishes, give the user the path of the Excel file just created.

# ENVIRONMENT REQUIREMENTS
- Requires Python 3.8+ and the `openpyxl` library. If the command reports a missing module, run `python -m pip install openpyxl` (or `python3 -m pip install openpyxl`) and try again.

# NOTES
- Always use the `md_to_xlsx.py` script to convert; never rebuild the tables in Excel by hand — this avoids mistakes and wasted time when tables are long.
- A heading names only the first table after it. Any other table without its own heading gets `Table<N>` (`Bảng<N>` with `--lang vi`), where `<N>` is the table's position in the file (e.g. `Table2`).
