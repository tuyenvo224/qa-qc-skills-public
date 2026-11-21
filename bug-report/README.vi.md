# bug-report

Viết **bug report sẵn để dán** lên mọi tracker (Jira, Redmine, GitHub Issues, Linear…) từ mô tả lỗi của bạn: một dòng tiêu đề và nội dung 7 mục. Nếu có spec thì kết quả mong đợi được dẫn căn cứ bằng rule ID.

Bản tiếng Anh: [README.md](README.md). AI agent làm theo `SKILL.md`.

## Cấu trúc skill

```
bug-report/
  ├── SKILL.md              ← hướng dẫn cho AI agent
  ├── README.md             ← hướng dẫn tiếng Anh
  ├── README.vi.md          ← file này
  └── references/
        └── template.md     ← nhãn mục (EN/VI), khung nội dung, ví dụ ngắn và ví dụ đầy đủ
```

## Khi nào dùng

- Bạn vừa tìm thấy bug khi test và muốn viết lại rõ ràng, thống nhất.
- Muốn viết lại ghi chú bug sơ sài trước khi post.

Không dùng cho: đoán bug tiềm ẩn (dùng `bug-hunter-lite`), viết test case (dùng `write-quick-test-cases`).

Skill **không bao giờ tạo hay sửa issue** trên tracker. Bạn review rồi tự dán. Skill chạy thẳng tới kết quả, không hỏi xác nhận.

## Cài đặt

Chép thư mục `bug-report` vào thư mục skills của công cụ AI:
- **Claude Code:** `~/.claude/skills/` (mọi project) hoặc `<project>/.claude/skills/` (một project).
- **Công cụ khác** hỗ trợ [Agent Skills](https://agentskills.io) (`SKILL.md`): xem tài liệu của công cụ để biết thư mục skills.

Khởi động lại công cụ hoặc mở phiên mới. Không cần cài thêm gì.

## Cách dùng

Mô tả chuyện đã xảy ra: case bị lỗi, bạn thấy gì, và nếu có thì một case tương tự đang chạy đúng. Gửi kèm môi trường, ảnh chụp và spec nếu có.

```
Viết bug giúp tôi: trên STG, đăng nhập với mật khẩu có ký tự "#" thì báo "Sai mật khẩu"
Viết lại bug này để post lên Jira: <dán ghi chú>
Log a bug: <failure description>
```

## Kết quả

Trả về ngay trong khung chat (không tạo file):

1. **Tiêu đề** (codeblock 1): `[<ENV>][<UI|Function>][<Sản phẩm>] [<Module>] <điều kiện> thì <hành vi sai>`
   - `<ENV>` là môi trường bạn nêu (STG, UAT, PROD…); không nêu thì để `[<ENV>]`.
   - `[UI]` cho lỗi hiển thị, `[Function]` cho lỗi hành vi / logic.
2. **Nội dung** (codeblock 2): I. Môi trường · II. Điều kiện tiên quyết · III. Các bước tái hiện · IV. Kết quả thực tế · V. Kết quả mong đợi · VI. Tần suất · VII. Ghi chú (có dòng **Ảnh đính kèm** bắt buộc).
3. **Kiểm tra trước khi post:** tối đa 5 dòng, gồm ảnh cần đính kèm, các ô `<...>` còn trống, giả định cần kiểm lại, câu hỏi cho BA/PO.

Quy tắc skill tuân theo: Kết quả thực tế chỉ ghi điều bạn đã quan sát; thông tin thiếu để `<...>`, không tự bịa; rule ID (BR/FR/UC/AC) trích đúng nguyên văn; spec không quy định hoặc mơ hồ thì ghi rõ, không tự kết luận là bug. Mặc định là Markdown, có thể đổi sang Jira wiki markup nếu bạn yêu cầu.

## Ngôn ngữ

Viết theo ngôn ngữ bạn dùng. Khi viết tiếng Việt, nhãn mục giữ tên tiếng Anh trong ngoặc (vd `I. Môi trường (Environment)`). Tag, rule ID, `Always/Sometimes/Rarely` và chữ trên giao diện giữ nguyên văn.

## Tác giả

tuyenvo224
