# QA/QC Agent Skills

Bộ skill dành cho QA/QC: làm rõ requirement, săn bug tiềm ẩn, viết test case (Markdown hoặc Excel), viết bug report, và chuyển spec OpenAPI thành test case API.

Các skill theo chuẩn mở [Agent Skills](https://agentskills.io) (`SKILL.md`), nên dùng được với Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, Antigravity và các công cụ AI khác hỗ trợ `SKILL.md`. Đã kiểm thử chủ yếu trên Claude Code.

🇬🇧 English: [README.md](README.md)

**Song ngữ:** skill viết bằng tiếng Anh nhưng trả lời theo ngôn ngữ bạn dùng. Hỏi tiếng Việt thì kết quả (bản phân tích, test case, nhãn trong file Excel) bằng tiếng Việt; hỏi tiếng Anh thì ra tiếng Anh. Thuật ngữ kỹ thuật giữ nguyên tiếng Anh.

## Danh sách skill

### Phân tích requirement

| Skill | Chức năng |
|---|---|
| [`requirement-clarifier`](requirement-clarifier/) | Sinh danh sách câu hỏi làm rõ có ưu tiên (kèm Top 3) cho một spec, mang thẳng vào buổi review với BA/PO. |
| [`requirement-to-mindmap`](requirement-to-mindmap/) | Chuyển requirement thành mindmap test coverage tương thích markmap (scenario → ý test dạng checkbox), đánh dấu rõ case suy luận là giả định. |
| [`product-feature-overview`](product-feature-overview/) | Dựng bản đồ cấu trúc sản phẩm (Sản phẩm → Epic → Feature) từ tài liệu tổng quan / PRD lớn. |

### Săn bug và báo bug

| Skill | Chức năng |
|---|---|
| [`bug-hunter-lite`](bug-hunter-lite/) | Rà flow theo tư duy destructive testing: áp 6 góc nhìn (phá flow, dữ liệu, trạng thái, rule, giả định, đóng vai người dùng xấu) và trả về top 5 giả thuyết bug có ảnh hưởng lớn. |
| [`bug-report`](bug-report/) | Viết bug report sẵn để copy lên mọi tracker (Jira, Redmine, GitHub Issues…): tiêu đề + nội dung 7 mục, tag `[UI]`/`[Function]`, kết quả mong đợi có căn cứ rule ID trong spec, kèm danh sách kiểm tra trước khi post. |

### Thiết kế test case

| Skill | Chức năng |
|---|---|
| [`write-quick-test-cases`](write-quick-test-cases/) | Viết nhanh bộ test case gọn (positive / negative / boundary / security), xuất ra template Excel kịch bản kiểm thử chuẩn. |
| [`markdown-to-excel`](markdown-to-excel/) | Chuyển file Markdown có bảng (test case, danh sách dữ liệu…) sang `.xlsx`. |

### Test API

| Skill | Chức năng |
|---|---|
| [`api-test-design-lite`](api-test-design-lite/) | Sinh bộ test case API cốt lõi (bảng Markdown) từ spec OpenAPI 3.x / Swagger 2.0: happy path, validate, giới hạn spec khai báo, auth cơ bản và not-found. |

## Quy trình gợi ý

```
requirement
  ─► requirement-clarifier     câu hỏi cho BA/PO (mã QH/QM/QL)
  ─► requirement-to-mindmap    mindmap test coverage
  ─► bug-hunter-lite           top 5 bug tiềm ẩn
  ─► write-quick-test-cases    test case Excel

lỗi phát hiện khi test ─► bug-report ─► (bạn review rồi dán lên tracker)

OpenAPI spec ─► api-test-design-lite ─► (bạn review file test case .md)
```

Đưa kết quả của bước trước vào bước sau (câu hỏi đã được trả lời, các nhánh mindmap, giả thuyết bug) để test case phủ được những gì đã phát hiện. Từng skill cũng dùng riêng lẻ được.

## Cài đặt

1. Chép các thư mục skill cần dùng vào thư mục skills của công cụ AI bạn dùng.
   - **Claude Code:** `~/.claude/skills/` (dùng cho mọi project) hoặc `<project>/.claude/skills/` (chỉ project đó).
   - **Công cụ khác:** xem tài liệu của công cụ để biết thư mục skills.
2. Khởi động lại công cụ (hoặc mở phiên mới) để nạp skill.
3. Mô tả việc cần làm, ví dụ *"Spec này cần hỏi BA những gì?"* hoặc *"Viết test case cho chức năng đăng nhập và xuất ra Excel"*. Công cụ nào hỗ trợ thì có thể gọi trực tiếp skill, ví dụ `/<tên-skill>` trong Claude Code.

### Yêu cầu

- Một công cụ AI hỗ trợ Agent Skills (`SKILL.md`). Hai skill xuất Excel cần công cụ chạy được lệnh Python.
- Python 3.8+ và `openpyxl` cho các skill xuất Excel (`write-quick-test-cases`, `markdown-to-excel`): `pip install openpyxl`.

## Ngôn ngữ

| Bạn viết bằng | Kết quả |
|---|---|
| Tiếng Việt | Tiếng Việt (thuật ngữ kỹ thuật giữ tiếng Anh) |
| Tiếng Anh | Tiếng Anh |
| Yêu cầu rõ (vd "xuất bằng tiếng Anh") | Theo ngôn ngữ bạn yêu cầu |

File Excel xuất ra tự đổi các nhãn cố định (tiêu đề, khối thông tin, tên cột) theo ngôn ngữ kết quả.

## Tác giả

tuyenvo224
