# product-feature-overview

Đọc tài liệu tổng quan hoặc PRD lớn của **cả một sản phẩm / hệ thống** rồi dựng **bản đồ cấu trúc sản phẩm**: tổng quan sản phẩm → Epic (nhóm tính năng lớn) → Feature con, dạng mindmap checkbox.

Bản tiếng Anh: [README.md](README.md). AI agent làm theo `SKILL.md`.

## Cấu trúc skill

```
product-feature-overview/
  ├── SKILL.md      ← hướng dẫn cho AI agent
  ├── README.md     ← hướng dẫn tiếng Anh
  └── README.vi.md  ← file này
```

## Khi nào dùng

- Mới tiếp cận một sản phẩm, cần nắm bức tranh tổng thể.
- Cần danh sách epic và feature để lên kế hoạch test cho cả hệ thống.

Không dùng cho: phân tích hoặc làm rõ **một** feature (dùng `requirement-clarifier`), mindmap test coverage của một requirement (dùng `requirement-to-mindmap`).

## Cài đặt

Chép thư mục `product-feature-overview` vào thư mục skills của công cụ AI:
- **Claude Code:** `~/.claude/skills/` (mọi project) hoặc `<project>/.claude/skills/` (một project).
- **Công cụ khác** hỗ trợ [Agent Skills](https://agentskills.io) (`SKILL.md`): xem tài liệu của công cụ để biết thư mục skills.

Khởi động lại công cụ hoặc mở phiên mới. Không cần cài thêm gì.

## Cách dùng

```
Tóm tắt tổng quan sản phẩm từ PRD này
Vẽ bản đồ tính năng cho hệ thống này
Give me a product overview and a feature map
```

## Kết quả

| Bạn yêu cầu | Nội dung | File (trong `product-overview/`) |
|---|---|---|
| Tổng quan "đơn giản" | 1. Tổng quan sản phẩm | `yyyy-mm-dd_hh-mm-ss-ten-san-pham-overview.md` |
| Bản đồ tính năng / phân tích sâu | 1. Tổng quan sản phẩm + 2. Bản đồ phân cấp tính năng | `yyyy-mm-dd_hh-mm-ss-ten-san-pham-feature-map.md` |

- **Tổng quan sản phẩm:** mục đích, bài toán giải quyết, đối tượng người dùng (persona và quyền của họ).
- **Bản đồ phân cấp tính năng:** `- [ ] **Epic**` → `- [ ] *Feature*`, mỗi mục có một dòng mô tả vai trò.

## Ngôn ngữ

Viết theo ngôn ngữ bạn dùng (tiếng Việt hoặc tiếng Anh). Thuật ngữ `Epic`, `Feature`, cú pháp checkbox và tên file giữ nguyên.

## Tác giả

tuyenvo224
