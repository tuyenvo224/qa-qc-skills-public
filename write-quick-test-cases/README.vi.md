# write-quick-test-cases

Viết nhanh **bộ test case cơ bản** (Positive / Negative / Boundary / Security) từ requirement hoặc user story ngắn, rồi xuất ra **file Excel kịch bản kiểm thử dùng được ngay** bằng script đi kèm.

Bản tiếng Anh: [README.md](README.md). AI agent làm theo `SKILL.md`.

## Cấu trúc skill

```
write-quick-test-cases/
  ├── SKILL.md                          ← hướng dẫn cho AI agent
  ├── README.md                         ← hướng dẫn tiếng Anh
  ├── README.vi.md                      ← file này
  └── scripts/
        └── testcase_md_to_xlsx.py      ← chuyển Markdown → Excel (--lang en|vi, --qc-name, --ticket-url-template)
```

## Khi nào dùng

- Cần nhanh một bộ test case gọn, không cần phân tích độ phủ sâu.
- Muốn test case theo layout Excel chuẩn để tester chạy và điền kết quả trực tiếp.

Không dùng cho: chuyển một file Markdown bất kỳ sang Excel (dùng `markdown-to-excel`).

## Cài đặt

Chép thư mục `write-quick-test-cases` vào thư mục skills của công cụ AI:
- **Claude Code:** `~/.claude/skills/` (mọi project) hoặc `<project>/.claude/skills/` (một project).
- **Công cụ khác** hỗ trợ [Agent Skills](https://agentskills.io) (`SKILL.md`): xem tài liệu của công cụ để biết thư mục skills.

Khởi động lại công cụ hoặc mở phiên mới.

**Yêu cầu:** Python 3.8+ và `openpyxl` (`pip install openpyxl`). Công cụ AI phải chạy được lệnh Python (`python`, hoặc `python3` trên macOS/Linux).

## Cách dùng

```
Viết test case nhanh cho tính năng này và xuất ra Excel: <dán user story>
Viết test case cho màn hình đăng nhập, ticket PROJ-123
Write test cases for this feature
```

Tùy chọn: cho biết tên tester, hoặc mẫu link ticket (vd `https://jira.example.com/browse/{id}`) để mã ticket thành link bấm được.

## Kết quả

Hai file:

| File | Mục đích |
|---|---|
| `test-cases-for-review/yyyy-mm-dd_hh-mm-ss-ten-feature.md` | Bản nháp Markdown, để xem nhanh / so sánh |
| Cùng tên, đuôi `.xlsx` | **Sản phẩm chính**: file Excel kịch bản kiểm thử |

File Excel:
- Khối thông tin ở đầu (tên feature, link spec/ticket, tester, ngày tạo dạng `yyyy-mm-dd`…).
- Test case nhóm theo Module/Function thành "I.", "II."…, đánh số liên tục; Positive trước, rồi Negative, Boundary, Security.
- 10 cột: STT · Mục đích kiểm thử · Precondition · Test data · Các bước thực hiện · Kết quả mong muốn · Kết quả hiện tại · Mã lỗi · Ghi chú · QC thực hiện. **4 cột cuối để trống** cho lúc chạy test.
- Tự xuống dòng, chiều cao hàng vừa nội dung; không cố định hàng/cột.
- **Kết quả mong muốn còn chờ PO/BA xác nhận** (vd "cần confirm", "giả định", `QH-xx`) được **tô cam nhạt**; AI agent cũng liệt kê đó là những case nào.

Nếu bạn chỉ đưa tên chức năng (không có mô tả, rule hay acceptance criteria), agent hỏi tối đa 2 câu trước và chưa tạo file cho tới khi bạn trả lời.

## Ngôn ngữ

Trả lời theo ngôn ngữ bạn dùng. Nhãn trong Excel (tiêu đề, khối thông tin, tên cột) tự đổi sang tiếng Việt hoặc tiếng Anh cho khớp. Tag phân loại `[Positive]/[Negative]/[Boundary]/[Security]` và thuật ngữ kỹ thuật giữ tiếng Anh.

## Tác giả

tuyenvo224
