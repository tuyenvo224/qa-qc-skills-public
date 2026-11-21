# api-test-design-lite

Skill đọc file OpenAPI/Swagger rồi sinh **bộ test case API cốt lõi dạng bảng Markdown**, sẵn sàng để QA review.
File này hướng dẫn người dùng (tiếng Việt). Bản tiếng Anh: [README.md](README.md). AI agent làm theo `SKILL.md`.

## Cấu trúc skill

```
<thư-mục-skills>/api-test-design-lite/
  ├── SKILL.md      ← hướng dẫn cho AI agent
  ├── README.md     ← hướng dẫn cho người dùng (tiếng Anh)
  ├── README.vi.md  ← hướng dẫn cho người dùng (tiếng Việt, file này)
  └── references/
        └── lite-rules.md  ← quy tắc coverage, format file, quy ước cột, cú pháp assertion, dữ liệu mẫu, ví dụ
```

## Phạm vi

| Test Type | Nội dung |
|---|---|
| Happy | Mỗi endpoint một case thành công; endpoint ghi dữ liệu có thêm case chỉ field bắt buộc và case đủ field; kiểm tra field trả về; không lộ field bí mật |
| Validation | Thiếu / sai kiểu cho mọi input bắt buộc; sai format, pattern, enum; vượt giới hạn spec khai báo; body rỗng `{}` |
| Auth | Thiếu và sai credential cho mỗi endpoint cần xác thực; 403 cho mỗi role không được phép |
| NotFound | Id không tồn tại cho mỗi id trên path |
| Boundary | Đúng bằng từng giới hạn spec khai báo |

Không bao gồm (luôn ghi ở mục Not covered của file kết quả): payload bảo mật (injection, XSS, SSRF…), mass assignment, BOLA, token hết hạn / bị sửa, biên thăm dò khi spec không khai báo, kiểm tra side effect, business rule, hành vi mức HTTP, upload file.

## Cài đặt

Chép thư mục `api-test-design-lite` vào thư mục skills của công cụ AI:
- **Claude Code:** `~/.claude/skills/` (mọi project) hoặc `<project>/.claude/skills/` (một project).
- **Công cụ khác** hỗ trợ [Agent Skills](https://agentskills.io) (`SKILL.md`): xem tài liệu của công cụ để biết thư mục skills.

Khởi động lại công cụ hoặc mở phiên mới. Không cần cài thêm gì.

## Cách dùng

```
Sinh test case API từ file ./openapi.yaml
Generate API test cases from https://example.com/openapi.json
```

Kết quả: một file `test-case-api/yyyy-mm-dd_hh-mm-ss-<tên-api>.md` (trong thư mục làm việc hiện tại, trừ khi bạn chỉ định nơi khác). Spec có hơn 10 endpoint thì skill đưa plan coverage trước; bạn trả lời "ok" hoặc chỉnh lại.

## Ngôn ngữ

Phần chữ tự do (Description, Pre-condition, Notes, Assumptions, tin nhắn) theo ngôn ngữ bạn dùng. Tên cột, Test Type, Priority, cú pháp assertion và các marker giữ tiếng Anh để file thống nhất.

## Format kết quả

14 cột: `TC_ID | Module | Endpoint | Method | Test Type | Priority | Pre-condition | Description | Headers | Path/Query Params | Request Body | Expected Status | Expected Response | Notes`. Xem ví dụ trong `references/lite-rules.md`.

## Tác giả

tuyenvo224
