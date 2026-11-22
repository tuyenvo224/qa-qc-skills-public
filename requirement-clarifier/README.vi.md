# requirement-clarifier

Rà spec hoặc feature để tìm điểm thiếu, mơ hồ và mâu thuẫn, rồi chuyển thành **danh sách câu hỏi có ưu tiên** cho BA/PO, mang thẳng vào buổi review.

Bản tiếng Anh: [README.md](README.md). AI agent làm theo `SKILL.md`.

## Cấu trúc skill

```
requirement-clarifier/
  ├── SKILL.md      ← hướng dẫn cho AI agent
  ├── README.md     ← hướng dẫn tiếng Anh
  └── README.vi.md  ← file này
```

## Khi nào dùng

- Trước khi bắt đầu dev hoặc test, để tìm những gì spec chưa nói rõ.
- Chuẩn bị câu hỏi cho buổi review với BA/PO.
- Input: PRD / SRS, user story, ticket Jira, mô tả tự do, hoặc ảnh / Figma / screenshot.

Không dùng cho: mindmap test coverage (dùng `requirement-to-mindmap`), săn bug tiềm ẩn (dùng `bug-hunter-lite`), viết test case (dùng `write-quick-test-cases`).

## Cài đặt

Chép thư mục `requirement-clarifier` vào thư mục skills của công cụ AI:
- **Claude Code:** `~/.claude/skills/` (mọi project) hoặc `<project>/.claude/skills/` (một project).
- **Công cụ khác** hỗ trợ [Agent Skills](https://agentskills.io) (`SKILL.md`): xem tài liệu của công cụ để biết thư mục skills.

Khởi động lại công cụ hoặc mở phiên mới. Không cần cài thêm gì.

## Cách dùng

```
Spec này cần hỏi BA những gì? <dán spec>
Đặt câu hỏi về feature này giúp tôi
Chuẩn bị câu hỏi cho buổi review với PO
```

## Kết quả

Một file Markdown trong `questions/`, tên `yyyy-mm-dd_hh-mm-ss-ten-feature.md`, gồm 3 phần:

| Phần | Nội dung |
|---|---|
| A. Cách tôi hiểu feature | 3–5 gạch đầu dòng để BA/PO xác nhận |
| B. Câu hỏi cho BA/PO | Nhóm theo chủ đề; mỗi câu có **mã**, loại vấn đề, lý do cần làm rõ và mức ưu tiên |
| C. Top 3 câu hỏi | 3 câu nên hỏi trước khi thiếu thời gian |

- **Mã câu hỏi:** `QH-01…` (High), `QM-01…` (Medium), `QL-01…` (Low), đánh số liên tục trên toàn tài liệu. Dễ nhắc tới trong buổi họp ("câu QH-02…") và ghi lại câu trả lời.
- **Loại vấn đề:** Ambiguity / Missing / Conflict / Assumption / Testability.
- Điều gì phải suy luận đều được đánh dấu "(giả định)" và chuyển thành câu hỏi, không trình bày như sự thật.
- Nếu input không có quy tắc hay flow cụ thể nào (vd chỉ có tên chức năng) thì skill chưa tạo file, mà hỏi xin spec và nêu tối đa 3 câu hỏi về phạm vi.

## Ngôn ngữ

Trả lời theo ngôn ngữ bạn dùng (tiếng Việt hoặc tiếng Anh). Mã câu hỏi, loại vấn đề và mức ưu tiên (High/Medium/Low) giữ tiếng Anh.

## Tác giả

tuyenvo224
