"""
Convert a Markdown test case table into a "TEST SCENARIOS" Excel file (sheet "TCs"):
a metadata block (feature name, spec/ticket links, tester) followed by test cases
grouped into "I. <module>", "II. <module>"... blocks. The whole layout is built in
code, so this script needs no other file (only Python 3.8+ and openpyxl).

Markdown columns (any order, English or Vietnamese names, matched by keyword):
    No. | Module/Function | Test objective | Precondition | Test data | Test steps | Expected result
- Consecutive rows with the same Module/Function form one group.
- The type (Positive/Negative/Boundary/Security) is a "[Type] " prefix in Test objective.
- "No." is optional; cases are renumbered. Every matching table is read in file order.
- Text starting with "=" is written as plain text, never as a formula.
The execution columns (Actual result, Bug ID, Notes, Tester) are left blank.

Ticket: read from the first H1 heading, "# Test Case: <Feature> (<ticket>)". A URL is
made clickable; a bare ID ("#123", "PROJ-123") stays plain text unless
--ticket-url-template (e.g. "https://jira.example.com/browse/{id}") is given.

Usage:
    python testcase_md_to_xlsx.py <input.md> [output.xlsx] [--lang en|vi]
        [--qc-name "Tester name"] [--ticket-url-template "https://.../{id}"]
"""

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

import openpyxl
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

SHEET_NAME = 'TCs'  # same in both languages ("TCs" = test cases)

HEADER_ROW = 10
FIRST_DATA_ROW = 12  # row 11 is an empty spacer row under the header
GROUP_MERGE_COLS = 5  # group header spans columns A..E

DATA_COLS = 10  # A..J
EXPECTED_COL = 6  # F - "Expected result"

# Fixed texts per output language. Keys are cell coordinates, plus a few non-cell
# entries (prefixed with "_").
LABELS = {
    'en': {
        'E1': 'TEST SCENARIOS',
        'E2': 'Screen / Feature name',
        'E3': 'Spec link',
        'E4': 'Ticket link',
        'E5': 'Prototype',
        'E6': 'Domain',
        'E7': 'Account',
        'H2': 'Tester',
        'A10': 'Test case No.',
        'B10': 'Test objective',
        'C10': 'Precondition',
        'D10': 'Test data',
        'E10': 'Test steps',
        'F10': 'Expected result',
        'G10': 'Actual result',
        'H10': 'Bug ID',
        'I10': 'Notes',
        'J10': 'Tester',
        '_change_note': 'Created TCs',
        '_other_group': 'Other',
    },
    'vi': {
        'E1': 'KỊCH BẢN KIỂM THỬ',
        'E2': 'Tên màn hình/Tên chức năng',
        'E3': 'Link spec',
        'E4': 'Link ticket',
        'E5': 'Prototype',
        'E6': 'Domain',
        'E7': 'Account',
        'H2': 'QC thực hiện',
        'A10': 'STT trường hợp kiểm thử',
        'B10': 'Mục đích kiểm thử',
        'C10': 'Precondition',
        'D10': 'Test data',
        'E10': 'Các bước thực hiện',
        'F10': 'Kết quả mong muốn',
        'G10': 'Kết quả hiện tại',
        'H10': 'Mã lỗi',
        'I10': 'Ghi chú',
        'J10': 'QC thực hiện',
        '_change_note': 'Tạo TCs',
        '_other_group': 'Khác',
    },
}

# Header aliases for the Markdown table, matched against the normalize()d header
# (no diacritics, lowercase), tried in order. Short aliases (<= 3 chars, e.g. "no",
# "#", "id") must match the whole header; longer ones may appear anywhere in it.
COLUMN_ALIASES = {
    'stt': ['stt', 'no', 'no.', '#', 'id', 'tc id', 'test case id', 'tc no', 'tc no.'],
    'module': ['module', 'function', 'feature', 'screen', 'chuc nang', 'man hinh'],
    'purpose': ['muc dich', 'objective', 'purpose', 'scenario', 'test title', 'title',
                'summary', 'description'],
    'precondition': ['precondition', 'pre-condition', 'prerequisite', 'dieu kien'],
    'test_data': ['test data', 'du lieu', 'input data', 'data'],
    'steps': ['buoc', 'steps', 'step'],
    'expected': ['ket qua mong muon', 'ket qua mong doi', 'ket qua ky vong', 'expected'],
}
OPTIONAL_COLUMNS = {'stt'}
EXACT_MATCH_MAX_LEN = 3

# Cells that rest on an assumption / still need PO-BA confirmation get a
# light-orange fill on the expected result so the tester can spot them at a glance.
CONFIRM_FILL = PatternFill(fill_type='solid', start_color='FFFFE699', end_color='FFFFE699')
# English phrases and IDs: matched against the lowercased text.
CONFIRM_PATTERN_EN = re.compile(
    r'\b('
    r'needs? confirm(ation)?|to be confirmed|tbc|tbd|confirm with|pending confirmation'
    r'|awaiting confirmation|assumption|assumed|assuming|not finali[sz]ed|unclear'
    # Clarification question IDs (QH/QM/QL-xx = high/medium/low priority questions)
    r'|(qh|qm|ql)-\d+'
    r')\b'
)
# Vietnamese phrases: matched WITH diacritics (NFC, lowercased). Without them,
# unrelated words collide: "can confirm" (English) / "cần confirm",
# "gia đình" (family) / "giả định", "tạm dừng" (pause) / "tạm dùng".
CONFIRM_PATTERN_VI = re.compile(
    r'\b('
    r'cần confirm|confirm lại|chờ confirm|cần xác nhận|chờ xác nhận'
    r'|giả định|giả sử|tạm dùng|tạm hiểu|chưa chốt|chưa rõ'
    r')\b'
)

URL_PATTERN = re.compile(r'https?://[^\s)]+')
# "(#123)", "(123)", "(PROJ-123)", or a bare "#123" anywhere in the heading.
TICKET_ID_PATTERN = re.compile(r'\(\s*#?([A-Z][A-Z0-9_]*-\d+|\d+)\s*\)|#(\d+)')


def clean_cell(text: str) -> str:
    text = text.strip()
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', text)
    text = text.replace('\\|', '|')
    return text.strip()


def split_row(line: str):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    cells = re.split(r'(?<!\\)\|', line)
    return [clean_cell(c) for c in cells]


def is_separator(line: str) -> bool:
    stripped = line.strip()
    if not stripped or '-' not in stripped:
        return False
    return bool(re.match(r'^[|\s\-:]+$', stripped))


def find_tables(md_text: str):
    lines = md_text.splitlines()
    tables = []
    current_heading = None
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            current_heading = heading_match.group(2).strip()
            i += 1
            continue
        if line.strip().startswith('|') and i + 1 < n and is_separator(lines[i + 1]):
            header = split_row(line)
            j = i + 2
            rows = []
            while j < n and lines[j].strip().startswith('|'):
                rows.append(split_row(lines[j]))
                j += 1
            tables.append({'heading': current_heading, 'header': header, 'rows': rows})
            i = j
            continue
        i += 1
    return tables


def normalize(text: str) -> str:
    text = text.replace('đ', 'd').replace('Đ', 'D')  # Vietnamese d with stroke
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text.lower().strip()


def needs_confirmation(text) -> bool:
    """True when a cell rests on an assumption or is marked as needing PO/BA
    confirmation (e.g. "(assumed max 50 chars - needs confirmation QH-03)")."""
    if not text:
        return False
    lowered = unicodedata.normalize('NFC', str(text)).lower()
    return bool(CONFIRM_PATTERN_EN.search(lowered) or CONFIRM_PATTERN_VI.search(lowered))


def set_text(cell, value):
    """Write a value as plain text: a string starting with "=" would otherwise be
    stored as an Excel formula (e.g. test data "=1+1" shown as 2)."""
    cell.value = value
    if isinstance(value, str) and value.startswith('='):
        cell.data_type = 's'


def locate_columns(header):
    normalized = [normalize(h) for h in header]
    idx = {}
    taken = set()

    def matches(h, alias):
        if len(alias) <= EXACT_MATCH_MAX_LEN:
            return h == alias
        return alias in h

    for key, aliases in COLUMN_ALIASES.items():
        idx[key] = None
        # Aliases are tried in priority order so specific names win over generic ones.
        for alias in aliases:
            for i, h in enumerate(normalized):
                if i not in taken and matches(h, alias):
                    idx[key] = i
                    break
            if idx[key] is not None:
                taken.add(idx[key])
                break

    missing = [k for k, v in idx.items() if v is None and k not in OPTIONAL_COLUMNS]
    if missing:
        raise ValueError(
            f'Required column(s) not found: {missing}. Header received: {header}. '
            'Accepted names (EN/VI, case- and diacritic-insensitive): '
            + '; '.join(f'{k}={COLUMN_ALIASES[k]}' for k in missing)
        )
    return idx


FIELDS = ('module', 'purpose', 'precondition', 'test_data', 'steps', 'expected')


def collect_test_rows(tables):
    """Read every test case table in the file (the agent may write one table per
    module) into dicts keyed by FIELDS. Tables without the required columns are
    skipped and reported; if none qualifies, the first table's error is raised."""
    records, skipped, first_error = [], [], None
    for ti, table in enumerate(tables, start=1):
        try:
            idx = locate_columns(table['header'])
        except ValueError as e:
            first_error = first_error or e
            skipped.append(ti)
            continue
        for row in table['rows']:
            records.append({k: (row[idx[k]] if idx[k] < len(row) else '') for k in FIELDS})
    if len(skipped) == len(tables):
        raise first_error
    return records, skipped


def group_rows(records):
    groups = []
    for row in records:
        module_name = row['module']
        if groups and groups[-1][0] == module_name:
            groups[-1][1].append(row)
        else:
            groups.append([module_name, [row]])
    return groups


def to_roman(n: int) -> str:
    values = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'),
    ]
    result = []
    for value, symbol in values:
        count, n = divmod(n, value)
        result.append(symbol * count)
    return ''.join(result)


def extract_feature_info(md_text: str, input_path: Path, ticket_url_template=None):
    """Return (feature_name, ticket_value, ticket_is_url) from the first H1 heading."""
    heading = ''
    for line in md_text.splitlines():
        m = re.match(r'^#\s+(.*)', line)
        if m:
            heading = m.group(1).strip()
            break
    if not heading:
        heading = input_path.stem

    heading = re.sub(r'^Test Case:\s*', '', heading, flags=re.IGNORECASE).strip()

    def without(span_match):
        """Feature name = heading minus the ticket part (and the brackets/separators left around it)."""
        name = heading[:span_match.start()] + heading[span_match.end():]
        name = re.sub(r'\(\s*\)', '', name)
        return re.sub(r'\s+', ' ', name).strip(' -–—:|') or heading

    url_match = URL_PATTERN.search(heading)
    if url_match:
        url = url_match.group(0).rstrip(').,;')
        bracketed = re.search(r'\(\s*' + re.escape(url) + r'\s*\)', heading)
        return without(bracketed or url_match), url, True

    id_match = TICKET_ID_PATTERN.search(heading)
    if id_match:
        ticket_id = id_match.group(1) or id_match.group(2)
        feature = without(id_match)
        if ticket_url_template:
            return feature, ticket_url_template.replace('{id}', ticket_id), True
        plain = f'#{ticket_id}' if ticket_id.isdigit() else ticket_id
        return feature, plain, False

    return heading, None, False


# ---- Sheet layout and styles -------------------------------------------------
FONT_NAME = 'Times New Roman'
THIN = Side(style='thin', color='FF000000')
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def solid(rgb):
    return PatternFill(fill_type='solid', start_color=rgb, end_color=rgb)


HEADER_FILL = solid('FF00B050')  # green column header row
TESTER_FILL = solid('FFFFC000')  # orange "Tester" metadata block
GROUP_FILL = solid('FFFFFF00')   # yellow "I. <module>" group rows
COL_WIDTHS = {'A': 17.1, 'B': 42.3, 'C': 35, 'D': 35, 'E': 53.4, 'F': 60.9,
              'G': 24.7, 'H': 20.7, 'I': 22.6, 'J': 30.4}
ROW_HEIGHTS = {1: 24.6, 3: 67.5, 4: 26.25, 5: 35.25, 7: 30, 8: 24, HEADER_ROW: 45}
LINK_ROWS = (3, 4, 5, 6)  # spec / ticket / prototype / domain values look like links
META_ROWS = range(2, 9)   # metadata block: labels in E, values in F, tester in H..J


def font(size=11, bold=False, **kw):
    return Font(name=FONT_NAME, sz=size, bold=bold, **kw)


def style_cell(cell, fnt=None, fill=None, border=None, horizontal=None, wrap=False):
    cell.font = fnt or font()
    if fill:
        cell.fill = fill
    if border:
        cell.border = border
    cell.alignment = Alignment(horizontal=horizontal, vertical='center', wrap_text=wrap)


def build_layout(ws):
    """Draw the fixed part of the sheet: title, metadata block, column header."""
    ws.sheet_view.showGridLines = False
    for letter, width in COL_WIDTHS.items():
        ws.column_dimensions[letter].width = width
    for row, height in ROW_HEIGHTS.items():
        ws.row_dimensions[row].height = height

    style_cell(ws['E1'], font(20, bold=True), horizontal='center', wrap=True)
    for row in META_ROWS:
        style_cell(ws.cell(row, 5), font(bold=True), border=BOX, wrap=True)
        link = row in LINK_ROWS
        style_cell(ws.cell(row, 6), font(underline='single' if link else None,
                                         color='FF0563C1' if link else None),
                   border=BOX, wrap=True)
        for col in (8, 9, 10):
            style_cell(ws.cell(row, col), font(bold=(row == 2)),
                       fill=TESTER_FILL if row == 2 else None, border=BOX)

    for col in range(1, DATA_COLS + 1):
        style_cell(ws.cell(HEADER_ROW, col), font(bold=True), fill=HEADER_FILL,
                   border=BOX, horizontal='center', wrap=True)
        ws.cell(HEADER_ROW + 1, col).border = BOX


def style_group_row(ws, row):
    for col in range(1, DATA_COLS + 1):
        style_cell(ws.cell(row, col), font(bold=True), fill=GROUP_FILL, border=BOX,
                   horizontal='left' if col == 1 else None)


def style_data_row(ws, row):
    for col in range(1, DATA_COLS + 1):
        style_cell(ws.cell(row, col), font(bold=(col == 1)), border=BOX,
                   horizontal='center' if col == 1 else 'left', wrap=True)


def add_result_colors(ws, first_row, last_row):
    """Actual result column: "F" (failed) in red, "PE" (pending) in blue."""
    rng = f'G{first_row}:G{max(first_row, last_row) + 300}'
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"F"'], font=Font(color='FFFF0000')))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"PE"'], font=Font(color='FF0000FF')))


MAX_ROW_HEIGHT = 409  # Excel's hard limit for a row height (points)


def wrapped_line_count(text, col_width):
    """Estimate how many visual lines `text` occupies in a column of `col_width`
    (Excel width units ~= characters), counting both explicit newlines and the
    soft wraps Excel applies to long lines when wrap_text is on."""
    # ~10% safety margin: diacritics/uppercase letters render wider than '0'.
    chars_per_line = max(1, int(col_width * 0.9))
    total = 0
    for line in str(text).split('\n'):
        total += max(1, -(-len(line) // chars_per_line))
    return total


def fit_row_to_text(ws, row):
    """Turn on wrap_text for every data cell in `row` and grow the row height so
    the full text of the tallest cell is visible (no clipped content)."""
    max_height = 15
    for col in range(1, DATA_COLS + 1):
        cell = ws.cell(row=row, column=col)
        a = cell.alignment
        cell.alignment = Alignment(horizontal=a.horizontal, vertical=a.vertical, wrap_text=True)
        if cell.value in (None, ''):
            continue
        letter = cell.column_letter
        width = ws.column_dimensions[letter].width or 8.43
        font_size = cell.font.sz or 11
        line_height = font_size * 1.4
        lines = wrapped_line_count(cell.value, width)
        max_height = max(max_height, lines * line_height + 4)
    ws.row_dimensions[row].height = min(MAX_ROW_HEIGHT, max_height)


def apply_labels(ws, labels):
    for coord, text in labels.items():
        if not coord.startswith('_'):
            ws[coord] = text


def build_workbook(records, feature_name, ticket, ticket_is_url, qc_name, lang):
    labels = LABELS[lang]
    groups = group_rows(records)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = SHEET_NAME
    build_layout(ws)

    apply_labels(ws, labels)
    ws['F2'] = feature_name
    if ticket:
        ws['F4'] = ticket
        if ticket_is_url:
            ws['F4'].hyperlink = ticket
    ws['H3'] = qc_name or None
    ws['I3'] = date.today()
    ws['I3'].number_format = 'yyyy-mm-dd'
    ws['J3'] = labels['_change_note']

    r = FIRST_DATA_ROW
    stt = 1
    highlighted = []
    for gi, (module_name, items) in enumerate(groups, start=1):
        style_group_row(ws, r)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=GROUP_MERGE_COLS)
        set_text(ws.cell(row=r, column=1), f'{to_roman(gi)}. {module_name or labels["_other_group"]}')
        r += 1
        for row in items:
            style_data_row(ws, r)
            purpose = row['purpose']
            precondition = row['precondition']
            test_data = row['test_data']
            steps = row['steps']
            expected = row['expected']
            ws.cell(row=r, column=1, value=stt)
            for col, value in enumerate((purpose, precondition, test_data, steps, expected), start=2):
                set_text(ws.cell(row=r, column=col), value)
            fit_row_to_text(ws, r)
            # The assumption may sit in any column (e.g. a max length assumed in
            # Precondition) - the whole case is then unconfirmed, but only the
            # expected result cell is highlighted.
            if any(needs_confirmation(v) for v in (purpose, precondition, test_data, steps, expected)):
                ws.cell(row=r, column=EXPECTED_COL).fill = CONFIRM_FILL
                highlighted.append(stt)
            stt += 1
            r += 1

    add_result_colors(ws, FIRST_DATA_ROW, r - 1)
    return wb, highlighted


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', help='Path to the source .md file (write-quick-test-cases output)')
    parser.add_argument('output', nargs='?', help='Path to the output .xlsx file (default: alongside input, same name)')
    parser.add_argument('--lang', choices=sorted(LABELS), default='en',
                        help='Language of the fixed labels/headers in the Excel file (default: en)')
    parser.add_argument('--qc-name', default='',
                        help='Tester name written into the "Tester" metadata cell (default: blank)')
    parser.add_argument('--ticket-url-template', default=None,
                        help='Turn a bare ticket ID from the H1 heading into a link, e.g. '
                             '"https://jira.example.com/browse/{id}" (default: keep the ID as plain text)')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f'Input file not found: {input_path}', file=sys.stderr)
        sys.exit(1)
    if args.ticket_url_template and '{id}' not in args.ticket_url_template:
        print('--ticket-url-template must contain the "{id}" placeholder.', file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_suffix('.xlsx')

    md_text = input_path.read_text(encoding='utf-8')
    tables = find_tables(md_text)
    if not tables:
        print('No test case table (Markdown table) found in the input file.', file=sys.stderr)
        sys.exit(1)

    feature_name, ticket, ticket_is_url = extract_feature_info(md_text, input_path, args.ticket_url_template)

    try:
        records, skipped = collect_test_rows(tables)
        wb, highlighted = build_workbook(records, feature_name, ticket, ticket_is_url,
                                         args.qc_name, args.lang)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    if len(tables) > 1:
        print(f'Read {len(tables) - len(skipped)} of {len(tables)} Markdown tables ({len(records)} test cases).')
    if skipped:
        print('WARNING: skipped table(s) without the test case columns - No. in file order: '
              + ', '.join(str(s) for s in skipped))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f'Excel file created: {output_path}')
    if highlighted:
        print(f'Highlighted {len(highlighted)} "Expected result" cell(s) needing PO/BA confirmation - No.: '
              + ', '.join(str(s) for s in highlighted))
    else:
        print('No "Expected result" cell needs PO/BA confirmation.')


if __name__ == '__main__':
    main()
