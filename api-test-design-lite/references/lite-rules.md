# Lite Rules — Coverage, Format and Example

Read this file when planning and generating test cases. Each rule below becomes **one test case row** (one request, one intent). When a rule does not apply, skip it; when it applies but you cannot write the row, list it under "Not covered" with the reason.

---

## 1. Coverage rules

### Happy (`Happy`)
- Every endpoint: one successful request → the declared 2xx.
- Every write endpoint (POST/PUT/PATCH): one row with **required fields only** and one with **all fields**. If all fields are required, write one row and say so in Notes.
- GET list: one row without filters; one row per declared filter is optional (P3).
- Assert the main response fields with a type (`` `user.id` (integer) ``) and the values the request controls (`` `user.email`="jane@example.com" ``). Use the field paths of the response schema the spec declares — a `user.` wrapper only if the spec has one; never invent a wrapper.
- When a field has a `default` and the request omits it, assert the default (e.g. `` `role`="user" ``).
- Assert `writeOnly`/secret fields are absent (`` `password` not present in response ``).

### Validation (`Validation`, 400)
| Rule | Applies to |
|---|---|
| Missing (omit the field) | every required input (body, query, header) |
| Wrong type (string for integer, integer for string…) | every required input |
| Format violation | every input with `format` (email, uuid, date, date-time, uri…) |
| Pattern violation | every input with `pattern` |
| Enum violation (value outside the list) | every enum input |
| Just outside a declared limit (`minLength - 1`, `maxLength + 1`, `minimum - 1`, `maximum + 1`) | every input with a declared limit |
| Empty object `{}` | every endpoint with a JSON body, once |
| Wrong type in a path id (`id=abc` for an integer id) | every path id — expect `400/404` (frameworks differ); add `[NEEDS REVIEW: status <code> not declared in spec]` for each of the two codes the endpoint does not declare |

### Auth (`Auth`, 401/403)
Per endpoint that requires auth:
- No credential (header/param removed) → 401.
- Invalid credential (`Bearer invalid_token_xyz`, wrong API key) → 401.
- When the spec defines roles/scopes — in `securitySchemes`, or in the endpoint description (e.g. "Admin only") — one row per role that is **not** allowed → 403.

Skip for endpoints the spec marks public (`security: []`, or no security requirement and no global one).

**Login / credential endpoints** (public endpoints that take a username/email + password): add one row with a wrong password → the declared 401 (or 400/401 + `[NEEDS REVIEW]`), Test Type `Auth`.

### NotFound (`NotFound`, 404)
- Every endpoint with an id in the path: well-formed but non-existent id (`99999999`, `00000000-0000-0000-0000-000000000000`) → 404.

### Boundary (`Boundary`)
- Exactly at each **declared** limit: `minLength`, `maxLength`, `minimum`, `maximum` → 2xx.
- On login/credential endpoints the value at the limit is not a real password, so expect the declared 401 (the point is: not 400). Say so in Notes.
- Lite does not test undeclared limits. Path parameters are not tested for "missing" (removing them changes the route).

### Out of scope for Lite — always list under "Not covered"
Security payloads (SQL/NoSQL injection, XSS, path traversal, SSRF, malicious uploads), mass assignment and privilege escalation, BOLA/IDOR, expired/tampered tokens, exploratory limits for fields without declared constraints, null/whitespace/unicode variants, side-effect verification (GET after create/update/delete, double delete), business rules from descriptions, HTTP-level behavior (405, 406, response/security headers, CORS), non-JSON bodies and file uploads, `oneOf`/`anyOf` variants after the first.

Sanity range (guidance only — the rules above always win): ~6–18 rows per write endpoint, ~3–6 per read endpoint.

---

## 2. File layout

```markdown
# API Test Cases — <API Title> v<Version>

**Source spec**: `<path or URL of the spec>`
**Generated**: <YYYY-MM-DD>
**Base URL**: `<chosen server URL>`
**Coverage depth**: Lite
**Total test cases**: <N>

## Summary

| Module | Endpoints | Happy | Validation | Auth | NotFound | Boundary | Total |
|---|---|---|---|---|---|---|---|

## Test data & pre-requisites

- Accounts / tokens / ids the run needs, which row produces them or "fill by hand", e.g. `{{token}}` — admin token from TC_AUTH_POST_001; `{{username}}` / `{{password}}` — fill by hand (an existing account); `{{userToken}}` — fill by hand (a token of a non-admin role).

## Assumptions

- Interpretations made where the spec was silent (status codes chosen by convention…).

---

## Module: <Module Name>

### Endpoint: `<METHOD> <path>`

**Description**: <from spec>
**Auth required**: Yes (<scheme>, roles: <...>) / No
**Inputs**: <field — type, required/optional, constraints; one per line>

| TC_ID | Module | Endpoint | Method | Test Type | Priority | Pre-condition | Description | Headers | Path/Query Params | Request Body | Expected Status | Expected Response | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

---

## Not covered

- What was left out and why (always include the "Out of scope for Lite" items that apply).
```

---

## 3. Column conventions

| Column | Format | Example |
|---|---|---|
| TC_ID | `TC_<MODULE>_<METHOD>_<NNN>`; `<MODULE>` = Module uppercased, non-letters removed; 3-digit counter per `<MODULE>_<METHOD>` across the file | `TC_USERS_POST_001` |
| Module | Tag name from the spec, PascalCase | `Users` |
| Endpoint | Path with `{placeholders}` exactly as in the spec | `/api/users/{id}` |
| Method | Uppercase | `POST` |
| Test Type | `Happy`, `Validation`, `Auth`, `NotFound` or `Boundary` | `Validation` |
| Priority | `P1` / `P2` / `P3` (below) | `P1` |
| Pre-condition | Setup needed incl. dependency TC_IDs, or `None` | `{{token}} from TC_AUTH_POST_001` |
| Description | One sentence: action + expected outcome | `Create user without 'email'; expect 400` |
| Headers | `Key: Value` in backticks, separated by `<br>` | `` `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` `` |
| Path/Query Params | `key=value` in backticks, separated by `<br>`; every path placeholder has a value | `` `id={{createdUserId}}` `` |
| Request Body | Single-line JSON in inline backticks, or `N/A` | `` `{"email":"jane@example.com"}` `` |
| Expected Status | One code, or `a/b` when either is acceptable | `201` · `200/204` |
| Expected Response | Assertion clauses separated by `;`, optionally followed by free text and/or `[NEEDS REVIEW: ...]`; or only `[NEEDS REVIEW: ...]` when nothing can be asserted | `` `user.id` (integer); `password` not present in response `` |
| Notes | Assumptions, dependencies, or `N/A` | `Produces {{createdUserId}}` |

Credentials go where the spec's security scheme puts them: `Authorization: Bearer {{token}}` (bearer/JWT/OAuth2), `Authorization: Basic {{username}}:{{password}}` (basic), `X-API-Key: {{apiKey}}` or `api_key={{apiKey}}` (API key, name from the spec).

### Assertion clauses (Expected Response)

| Write | Meaning |
|---|---|
| `` `success`=true `` / `` `message`="Exact text" `` | top-level `success` / `message` equals the value (exact message only when the spec gives it) |
| `` `user.email`="jane@example.com" `` / `` `data.count`=6 `` / `` `user.is_active`=true `` | nested value equals a string / number / boolean / null |
| `` `user.id` (integer) `` | field present with type: `integer`, `number`, `string`, `boolean`, `object`, `array`, `null` |
| `` `users` is an array `` | field is an array |
| `` `password` not present in response `` | the key appears nowhere in the response |
| `Error message indicates email is required` | error mentions the field and the problem (`required`, `invalid`, `not found`) |

Write field names in backticks. When Expected Status lists several codes, only write clauses true for all of them. `{{variables}}` may be used inside equality values (e.g. `` `id`="{{createdUserId}}" ``) when the variable is listed under "Test data & pre-requisites".

### Long strings
Write `<N x 'c'>` inside the JSON string, e.g. `` `{"name":"<101 x 'a'>"}` `` — never `<101-char string>`.

### Table safety
Escape `|` inside a cell as `\|`; no fenced code blocks in cells; `N/A` in every empty cell; exactly 14 cells per row.

---

## 4. Test data

| Kind | Valid | Invalid |
|---|---|---|
| Email | `jane@example.com`, `john.smith@example.com` | `not-an-email`, `jane@`, `@example.com` |
| Name | `Jane Doe`, `Nguyễn Văn An` | `12345` (wrong type as number) |
| Password | `SecurePass123!` | — |
| Phone | `+84901234567` | `abc` |
| Date / date-time | `2026-03-15`, `2026-03-15T10:30:00Z` | `15/03/2026`, `2026-13-01` |
| UUID | `3fa85f64-5717-4562-b3fc-2c963f66afa6` | `not-a-uuid` |
| URL | `https://example.com/avatar.png` | `not a url` |
| Non-existent id | `99999999`, `00000000-0000-0000-0000-000000000000` | — |
| Invalid token | `Bearer invalid_token_xyz` | — |

Prefer the spec's own `example` values when present. Never use real secrets.

---

## 5. Priority guidance

- **P1**: Happy paths, missing required fields, 401/403, 404 on resource lookups.
- **P2**: Wrong type, format/pattern/enum violations, limits (just outside and exactly at) of **required** fields.
- **P3**: Limits of **optional** fields, optional filters and rarely used params.

---

## 6. Worked example

Given:

```yaml
paths:
  /api/users:
    post:
      tags: [Users]
      summary: Create a new user
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:    { type: string, format: email }
                password: { type: string, minLength: 8, maxLength: 64, writeOnly: true }
                name:     { type: string, maxLength: 100 }
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:                       # the created user is wrapped in `user`
                    type: object
                    properties:
                      id:    { type: integer }
                      email: { type: string, format: email }
                      name:  { type: string }
        '400': { description: Bad Request }
        '401': { description: Unauthorized }
```

(The `user.` paths in the assertions below come from this declared wrapper. If the spec returns the object at the top level, assert `id`, `email`… directly.)

### Endpoint: `POST /api/users`

**Description**: Create a new user
**Auth required**: Yes (bearerAuth)
**Inputs**: `email` — string/email, required · `password` — string, required, 8–64, writeOnly · `name` — string, optional, max 100

| TC_ID | Module | Endpoint | Method | Test Type | Priority | Pre-condition | Description | Headers | Path/Query Params | Request Body | Expected Status | Expected Response | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC_USERS_POST_001 | Users | /api/users | POST | Happy | P1 | `{{token}}` from TC_AUTH_POST_001 | Create user with required fields only; expect 201 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"jane@example.com","password":"SecurePass123!"}` | 201 | `user.id` (integer); `user.email`="jane@example.com"; `password` not present in response | Produces `{{createdUserId}}` |
| TC_USERS_POST_002 | Users | /api/users | POST | Happy | P1 | `{{token}}` | Create user with all fields; expect 201 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"john@example.com","password":"SecurePass123!","name":"John Smith"}` | 201 | `user.id` (integer); `user.name`="John Smith" | N/A |
| TC_USERS_POST_003 | Users | /api/users | POST | Validation | P1 | `{{token}}` | Create user without 'email'; expect 400 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"password":"SecurePass123!"}` | 400 | Error message indicates email is required | N/A |
| TC_USERS_POST_004 | Users | /api/users | POST | Validation | P1 | `{{token}}` | Create user without 'password'; expect 400 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"jane3@example.com"}` | 400 | Error message indicates password is required | N/A |
| TC_USERS_POST_005 | Users | /api/users | POST | Validation | P2 | `{{token}}` | 'email' as a number; expect 400 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":12345,"password":"SecurePass123!"}` | 400 | Error message indicates email is invalid | N/A |
| TC_USERS_POST_006 | Users | /api/users | POST | Validation | P2 | `{{token}}` | Invalid email format; expect 400 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"not-an-email","password":"SecurePass123!"}` | 400 | Error message indicates email is invalid | N/A |
| TC_USERS_POST_007 | Users | /api/users | POST | Validation | P2 | `{{token}}` | Password of 7 characters (min 8); expect 400 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"jane4@example.com","password":"Pass12!"}` | 400 | Error message indicates password is invalid | N/A |
| TC_USERS_POST_008 | Users | /api/users | POST | Validation | P2 | `{{token}}` | Password of 65 characters (max 64); expect 400 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"jane5@example.com","password":"<65 x 'a'>"}` | 400 | Error message indicates password is invalid | N/A |
| TC_USERS_POST_009 | Users | /api/users | POST | Validation | P2 | `{{token}}` | Empty body object; expect 400 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{}` | 400 | Error message indicates email is required | N/A |
| TC_USERS_POST_010 | Users | /api/users | POST | Auth | P1 | None | Create user without Authorization header; expect 401 | `Content-Type: application/json` | N/A | `{"email":"jane6@example.com","password":"SecurePass123!"}` | 401 | Status code only (no error schema in spec) | N/A |
| TC_USERS_POST_011 | Users | /api/users | POST | Auth | P1 | None | Create user with an invalid token; expect 401 | `Authorization: Bearer invalid_token_xyz`<br>`Content-Type: application/json` | N/A | `{"email":"jane7@example.com","password":"SecurePass123!"}` | 401 | Status code only (no error schema in spec) | N/A |
| TC_USERS_POST_012 | Users | /api/users | POST | Boundary | P2 | `{{token}}` | Password of exactly 8 characters; expect 201 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"min.pass@example.com","password":"Pass123!"}` | 201 | `user.id` (integer) | N/A |
| TC_USERS_POST_013 | Users | /api/users | POST | Boundary | P2 | `{{token}}` | Password of exactly 64 characters; expect 201 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"max.pass@example.com","password":"<64 x 'a'>"}` | 201 | `user.id` (integer) | N/A |
| TC_USERS_POST_014 | Users | /api/users | POST | Boundary | P3 | `{{token}}` | Name of exactly 100 characters; expect 201 | `Authorization: Bearer {{token}}`<br>`Content-Type: application/json` | N/A | `{"email":"long.name@example.com","password":"SecurePass123!","name":"<100 x 'a'>"}` | 201 | `user.id` (integer) | N/A |

Rows 001 and 002 use different emails so a duplicate-email rule (if any) does not interfere.

(A `name` of 101 characters → 400 is also required by the rules; it is omitted here only to keep the example short.)
