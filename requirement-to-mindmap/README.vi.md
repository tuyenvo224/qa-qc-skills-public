# requirement-to-mindmap

Chuyển **một requirement** thành **mindmap test coverage** dạng Markdown tương thích markmap: Feature → nhóm scenario → test case dạng checkbox, các case suy luận được đánh dấu rõ.

Bản tiếng Anh: [README.md](README.md). AI agent làm theo `SKILL.md`.

## Cấu trúc skill

```
requirement-to-mindmap/
  ├── SKILL.md      ← hướng dẫn cho AI agent
  ├── README.md     ← hướng dẫn tiếng Anh
  └── README.vi.md  ← file này
```

## Khi nào dùng

- Muốn có cây test trực quan cho một requirement, để rà độ phủ hoặc tick dần khi chạy test.
- Chỉ dùng khi bạn yêu cầu rõ **mindmap / sơ đồ tư duy / markmap / cây test case**.

Không dùng cho: yêu cầu chung "phân tích requirement này" (dùng `requirement-clarifier`), bản đồ tính năng toàn sản phẩm (dùng `product-feature-overview`), bảng test case (dùng `write-quick-test-cases`).

## Cài đặt

Chép thư mục `requirement-to-mindmap` vào thư mục skills của công cụ AI:
- **Claude Code:** `~/.claude/skills/` (mọi project) hoặc `<project>/.claude/skills/` (một project).
- **Công cụ khác** hỗ trợ [Agent Skills](https://agentskills.io) (`SKILL.md`): xem tài liệu của công cụ để biết thư mục skills.

Khởi động lại công cụ hoặc mở phiên mới. Không cần cài thêm gì.

## Cách dùng

```
Vẽ mindmap test coverage cho requirement này: <dán requirement>
Chuyển requirement này thành sơ đồ tư duy
Draw a test coverage mindmap for this feature
```

## Kết quả

Một file Markdown `mindmap/yyyy-mm-dd_hh-mm-ss-ten-feature.md`. Mở bằng [markmap](https://markmap.js.org) (extension VS Code hoặc bản web) để xem dạng mindmap tương tác.

```
# <Hệ thống / requirement>
## <Feature>
### Happy path
- [ ] <test case kèm kết quả mong đợi>
### Negative
### Boundary / Edge
### UI/UX
(+ Security / Performance / Compatibility khi liên quan)
```

- Đúng 4 cấp (gốc → feature → nhóm scenario → test case), để mindmap dễ đọc.
- Dữ liệu test và giá trị biên để trong `inline code`.
- Case requirement không nói tới được đánh dấu `❓(giả định)` (`❓(assumed)` khi viết tiếng Anh).
- Output chỉ có mindmap, không có phần mở đầu hay giải thích.

## Ngôn ngữ

Viết theo ngôn ngữ bạn dùng (tiếng Việt hoặc tiếng Anh). Cú pháp markmap, tên nhóm scenario (Happy path, Negative, Boundary / Edge, UI/UX…) và thuật ngữ kỹ thuật giữ tiếng Anh.

## Tác giả

tuyenvo224
