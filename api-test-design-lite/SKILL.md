---
name: api-test-design-lite
description: "Generates a core set of API test cases as Markdown tables (14 fixed columns) from an OpenAPI 3.x / Swagger 2.0 spec (JSON/YAML, file or URL): happy paths, required-field and type/format/enum validation, declared length/range limits, basic authentication (401/403) and not-found (404) cases, ready for QA review. Use whenever the user provides an OpenAPI/Swagger spec and asks for API test cases, API test scenarios or API QA documentation, e.g. \"design test cases for this API\", \"generate test cases from this Swagger\", \"create API tests for this spec\", or in Vietnamese \"sinh test case API\", \"viết test case API\", \"sinh test case từ swagger\". Do NOT use for UI/business test cases from a requirement without an API spec — use `write-quick-test-cases`."
metadata:
  author: tuyenvo224
  version: "1.1"
---

# API Test Design (Lite)

Generate a structured, **core-coverage** set of API test cases in Markdown table format from an OpenAPI/Swagger specification. The output is reviewed by a QA engineer and used as the base test set for an API, so it must be clear, traceable and consistent.

Lite covers the cases every API needs: happy paths, input validation, declared limits, basic auth and not-found. It does **not** cover security payloads (injection, mass assignment, BOLA), exploratory limits, side-effect verification, business-rule rows or HTTP-level behavior — list those under "Not covered" so the reader knows the scope.

## Language

Reply to the user, and write the free-text parts of the output file, in the language of the user's request — Vietnamese or English. If the user explicitly asks for a language, use that one.

**Follows the user's language**: the prose in `Description`, `Pre-condition` and `Notes`, free text in `Expected Response`, the reason inside `[NEEDS REVIEW: <reason>]`, the bullets under Test data / Assumptions / Not covered, and your messages to the user.

**Always stays in English, exactly as written in `references/lite-rules.md`** — so files stay consistent and can be processed by tools: the header lines, section headings, the 14 column headers and their order, the TC_ID format, Test Type values (`Happy`, `Validation`, `Auth`, `NotFound`, `Boundary`), Priority (`P1`/`P2`/`P3`), `N/A`, `None`, the assertion clauses, `[NEEDS REVIEW`, `<N x 'c'>` and `{{variables}}`. Request data (headers, params, bodies) and exact API messages are test data — keep them as the spec has them.

## When to use this skill

- User provides an OpenAPI 3.x or Swagger 2.0 spec (JSON or YAML, file or URL)
- User asks to generate, design or write test cases for API endpoints
- User is preparing API test documentation for QA review

## Core principles

1. **Faithful to the spec** — Never invent endpoints, fields, response schemas or limits. Lite only tests limits the spec declares.
2. **Rule-driven coverage** — Coverage comes from the rules in `references/lite-rules.md`, applied per input field and per endpoint. Every rule either becomes a row or is listed under "Not covered" with a reason.
3. **Realistic test data** — Plausible values (`jane@example.com`, not `"string"`); the spec's own `example` values when present.
4. **One intent per row** — Each row is one request testing one thing.
5. **Clear expectations** — Write `Expected Response` with the assertion clauses in `references/lite-rules.md`, so a reader (or a tool) knows exactly what to check.
6. **Traceable IDs** — `TC_<MODULE>_<METHOD>_<NNN>`; `<NNN>` is a running counter per `<MODULE>_<METHOD>` across the whole file (it does not restart per endpoint).
7. **Safe tables** — 14 cells per row, `|` inside a cell escaped as `\|`, `N/A` in empty cells, single-line JSON in inline backticks.

## Workflow

### Step 1: Parse the spec and list the inputs

Read the spec (file or URL; OpenAPI 3.x or Swagger 2.0, JSON or YAML). Extract the API metadata (title, version, servers), every endpoint (path + method), the security scheme(s) and roles, and tags (used as Module).

For every endpoint list each input (path, query, header, body — including nested fields): location, type/format, required or optional, declared constraints (`minLength`/`maxLength`, `minimum`/`maximum`, `pattern`, `enum`), and `writeOnly` fields. Resolve `$ref` and merge `allOf`; for `oneOf`/`anyOf` use the first variant and note the others under "Not covered".

Pick the base URL: the non-localhost server if several are listed; say which one in the file header.

### Step 2: Plan coverage

Apply the rules in `references/lite-rules.md` and count the rows per endpoint and per Test Type.

- **Specs with more than 10 endpoints** — show a short plan (one line per endpoint with its counts, plus the grand total), then STOP and wait for the user to approve or adjust it.
- **Smaller specs** — skip showing the plan, but still follow it.

### Step 3: Generate test cases

Read `references/lite-rules.md` (rules, file layout, columns, assertion clauses, worked example). Generate one table per endpoint, grouped under `## Module: <name>`, with the 14 columns in this order:

| TC_ID | Module | Endpoint | Method | Test Type | Priority | Pre-condition | Description | Headers | Path/Query Params | Request Body | Expected Status | Expected Response | Notes |

Order: login/setup endpoints first; inside a module, endpoints in lifecycle order (create → read → update → delete).

Values a later row needs (token, created id) are named as variables — `{{token}}`, `{{createdUserId}}` — and listed under "Test data & pre-requisites" with the row that produces them or "fill by hand".

### Step 4: Self-check, save and present

Run the checklist below and fix every failure before saving. Save **exactly one file** (see "Output").

End by telling the user (a short chat reply — do not paste the whole file):
1. The file path and totals per Test Type.
2. The `[NEEDS REVIEW]` items that block running (credentials, sample ids).
3. "Review the test cases — mark any rows you want to change, add or remove."

## Status codes not declared in the spec

When a row needs a status code the spec does not declare for that endpoint, use the conventional code (400 validation, 401 missing/invalid credential, 403 insufficient permission, 404 missing resource) and add `[NEEDS REVIEW: status <code> not declared in spec]` to `Expected Response` (after any assertion clauses that still apply). Never guess other codes (409, 422, 429) unless the spec declares them.

## Output quality checklist

**Coverage**
- [ ] Every endpoint has ≥1 Happy row; every write endpoint has a required-only and an all-fields Happy row (one row if all fields are required)
- [ ] Every required input has a "missing" row (except path parameters) and a "wrong type" row
- [ ] Every input with a declared format, enum or pattern has a violation row
- [ ] Every input with a declared min/max has a just-outside row (Validation) and an exactly-at-limit row (Boundary)
- [ ] Every write endpoint with a body has an empty-object `{}` row
- [ ] Every endpoint that requires auth has a missing-credential and an invalid-credential row, plus a 403 row per denied role when the spec defines roles
- [ ] Every path id has a non-existent-id row
- [ ] Happy rows assert `writeOnly`/secret fields (e.g. `password`) are absent from the response
- [ ] "Not covered" lists what Lite leaves out (see `references/lite-rules.md`)

**Format**
- [ ] TC_IDs unique across the file; Test Type is one of the five values; Priority is P1/P2/P3
- [ ] Every row has exactly 14 cells; every `|` inside a cell is `\|`; no blank cells (use `N/A`)
- [ ] Every path `{placeholder}` has a value in Path/Query Params
- [ ] Long strings use `<N x 'c'>`, never descriptions like `<65-char string>`
- [ ] Every `{{variable}}` used is listed under "Test data & pre-requisites"
- [ ] All modules are in a single output file

## What to do when the spec is incomplete

- **No error response schema** — Generate the rows anyway and keep the `Error message indicates …` clause where it applies; when nothing can be asserted (typical for 401/403), write `Status code only (no error schema in spec)`. Do NOT tag every row: add ONE bullet under Assumptions instead, e.g. "The spec defines no error response schema — error rows check the status code and, where possible, the error message."
- **No examples** — Synthesize realistic data (`references/lite-rules.md` "Test data").
- **No auth scheme defined** — Ask the user once, then assume Bearer token if no answer.
- **Credentials / sample ids unknown** — Use variables and list them under "Test data & pre-requisites" as fill by hand: login body `{{username}}` / `{{password}}` (or per role, e.g. `{{adminEmail}}` / `{{adminPassword}}`), tokens of other roles `{{userToken}}`, existing ids `{{existingUserId}}`. Never invent real-looking credentials.
- **Vague descriptions** — Generate the obvious rows; put the open question in `Notes` with `[NEEDS REVIEW]`.

## What NOT to do

- Do not invent endpoints, fields, limits or non-conventional status codes
- Do not write vague rows ("Test the endpoint works") or combine several intents in one row
- Do not use real secrets or production credentials
- Do not split the output into one file per module

## Reference files

- `references/lite-rules.md` — Coverage rules per Test Type, file layout, column conventions, assertion clauses, test data, priority guidance, worked example

## Output

Unless the user specifies another location, create a new Markdown file in the `test-case-api/` directory, named `yyyy-mm-dd_hh-mm-ss-feature-name.md`, where `feature-name` comes from the API title or spec filename (e.g. `test-case-api/2026-10-03_14-30-00-user-service.md`).

File naming: the folder is relative to the current working directory (create it if missing); `yyyy-mm-dd_hh-mm-ss` is the local date and 24-hour time when the file is written; `feature-name` is a short slug of the API title (or spec filename): lowercase ASCII letters and digits joined by `-`, Vietnamese diacritics removed (`đ` → `d`), no prefixes such as "Feature:" or version numbers, at most 50 characters (e.g. `demoshop-users-api`).

If the user names a different directory/filename, follow that instead — do not write to both.
