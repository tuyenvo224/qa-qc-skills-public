# markdown-to-excel

Chuyển **file Markdown sang file Excel** (.xlsx) bằng script có sẵn. Mỗi bảng Markdown thành một sheet đã định dạng.

Bản tiếng Anh: [README.md](README.md). AI agent làm theo `SKILL.md`.

## Cấu trúc skill

```
markdown-to-excel/
  ├── SKILL.md            ← hướng dẫn cho AI agent
  ├── README.md           ← hướng dẫn tiếng Anh
  ├── README.vi.md        ← file này
  └── scripts/
        └── md_to_xlsx.py ← script chuyển đổi (input.md [output.xlsx] --lang en|vi [--overwrite])
```

## Khi nào dùng

- Bạn có test case, danh sách dữ liệu hoặc checklist dạng bảng Markdown và cần chuyển sang Excel.

Không dùng cho: viết test case mới (dùng `write-quick-test-cases`, skill này tự xuất Excel), đọc hoặc sửa file Excel có sẵn.

## Cài đặt

Chép thư mục `markdown-to-excel` vào thư mục skills của công cụ AI:
- **Claude Code:** `~/.claude/skills/` (mọi project) hoặc `<project>/.claude/skills/` (một project).
- **Công cụ khác** hỗ trợ [Agent Skills](https://agentskills.io) (`SKILL.md`): xem tài liệu của công cụ để biết thư mục skills.

Khởi động lại công cụ hoặc mở phiên mới.

**Yêu cầu:** Python 3.8+ và `openpyxl` (`pip install openpyxl`). Công cụ AI phải chạy được lệnh Python (`python`, hoặc `python3` trên macOS/Linux).

## Cách dùng

```
Chuyển file test-cases/login.md sang Excel
Xuất bảng markdown này ra Excel
Convert this markdown to Excel
```

Bạn cũng có thể dán bảng Markdown thẳng vào chat: agent lưu nguyên văn vào một file `.md` trong thư mục làm việc (đặt tên theo nội dung) rồi chuyển file đó sang Excel.

Nếu có nhiều file `.md` có thể khớp, AI agent sẽ hỏi lại thay vì tự đoán.

## Kết quả

Một file `.xlsx`, mặc định nằm cạnh file nguồn, cùng tên. Bạn cũng có thể chỉ định đường dẫn lưu. Nếu file đó đã có, không có gì bị ghi đè: agent hỏi bạn muốn thay thế hay lưu tên khác (phần bạn đã sửa trong Excel được giữ nguyên).

- Mỗi bảng Markdown → một sheet, đặt tên theo heading ngay trước bảng. Bảng không có heading riêng thì lấy tên file (nếu là bảng duy nhất) hoặc `Bảng<N>` theo vị trí (vd `Bảng2`).
- Dòng tiêu đề: chữ đậm, nền xanh, chữ trắng, cố định khi cuộn, có bộ lọc.
- `<br>` → xuống dòng trong ô; định dạng Markdown (`**đậm**`, `` `code` ``, link) được làm sạch.
- Độ rộng cột tự canh theo nội dung (tối đa 60).
- File không có bảng → toàn bộ chữ được ghi vào một sheet, mỗi dòng một hàng.
- Nội dung bảng chép nguyên văn, không dịch.

## Ngôn ngữ

Trả lời theo ngôn ngữ bạn dùng. `--lang vi` chỉ đổi vài chữ cố định do script ghi ra (tiêu đề dự phòng, tên sheet `Bảng1`…).

## Tác giả

tuyenvo224
