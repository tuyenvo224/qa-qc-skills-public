# bug-hunter-lite

Rà nhanh một flow hoặc feature theo tư duy **destructive testing**: nhìn qua 6 góc độ và trả về **top 5 bug có ảnh hưởng lớn** mà test thông thường hay bỏ sót, như edge case, lỗi timing, thao tác lặp, trạng thái sai, lách rule, hành vi người dùng xấu.

Bản tiếng Anh: [README.md](README.md). AI agent làm theo `SKILL.md`.

## Cấu trúc skill

```
bug-hunter-lite/
  ├── SKILL.md      ← hướng dẫn cho AI agent
  ├── README.md     ← hướng dẫn tiếng Anh
  └── README.vi.md  ← file này
```

## Khi nào dùng

- Trước khi viết test case cho các flow rủi ro: thanh toán, đăng nhập/xác thực, khuyến mãi/giảm giá, giao dịch nhiều bước, tích hợp bên thứ ba.
- Khi muốn biết "flow này có thể vỡ ở đâu, theo cách gây hậu quả nặng nhất?".

Không dùng cho: viết test case (dùng `write-quick-test-cases`), viết lại bug đã tìm thấy (dùng `bug-report`), làm rõ requirement thô (dùng `requirement-clarifier`). Không hữu ích với thay đổi chữ trên UI hay trang tĩnh.

## Cài đặt

Chép thư mục `bug-hunter-lite` vào thư mục skills của công cụ AI:
- **Claude Code:** `~/.claude/skills/` (mọi project) hoặc `<project>/.claude/skills/` (một project).
- **Công cụ khác** hỗ trợ [Agent Skills](https://agentskills.io) (`SKILL.md`): xem tài liệu của công cụ để biết thư mục skills.

Khởi động lại công cụ hoặc mở phiên mới. Không cần cài thêm gì.

## Cách dùng

```
Tìm bug tiềm ẩn trong flow checkout này: <dán flow>
Flow này có thể vỡ ở đâu?
Đóng vai người dùng xấu và phá tính năng voucher này
```

Nếu có thông tin kỹ thuật (API, queue, cache, webhook, dịch vụ bên thứ ba) thì gửi kèm, phân tích sẽ sát hơn.

## 6 góc nhìn

| Góc nhìn | Câu hỏi chính |
|---|---|
| Break the Flow | Nếu người dùng không đi hết flow như thiết kế thì sao? |
| Break the Data | Dữ liệu nào qua được validate nhưng làm sai logic? |
| Break the State | Nếu trạng thái hệ thống không như ta nghĩ thì sao? |
| Break the Rules | Người dùng có thể nhận nhiều hơn mức được phép bằng cách nào? |
| Break Assumptions | Hệ thống đang giả định điều gì có thể sai? |
| Think Like a Bad User | Nếu muốn lạm dụng hệ thống, tôi sẽ làm thế nào? |

## Kết quả

Lưu trong `bug-hunter-analysis/`, tên `yyyy-mm-dd_hh-mm-ss-ten-feature.md`:

1. **Tóm tắt luồng chính:** 3–5 câu, để xác nhận đã hiểu đúng flow.
2. **Top 5 giả thuyết bug:** bảng gồm góc nhìn đã tìm ra bug, giả thuyết, nguyên nhân, mức ảnh hưởng (Critical / High / Medium kèm hậu quả), vì sao hay bị bỏ sót. Xếp theo mức ảnh hưởng trước, khả năng xảy ra sau.
3. **Vùng nên tập trung:** nên dồn công test vào đâu trước.

## Ngôn ngữ

Trả lời theo ngôn ngữ bạn dùng (tiếng Việt hoặc tiếng Anh). Mức ảnh hưởng (Critical/High/Medium) và thuật ngữ kỹ thuật (race condition, idempotency, cache…) giữ tiếng Anh.

## Tác giả

tuyenvo224
