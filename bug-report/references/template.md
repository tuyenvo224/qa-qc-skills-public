# Bug Report Template

The output always has 2 codeblocks: **codeblock 1** is the title, **codeblock 2** is the body.

The title always starts with the environment tag (`[STG]`, `[UAT]`, `[PROD]`… or `[<ENV>]` when unknown) + one bug-type tag `[UI]` or `[Function]` (classification rules in `SKILL.md`), then `[Product] [Module]`.

## Section labels

| # | English output | Vietnamese output |
|---|---|---|
| I | `**I. Environment**` | `**I. Môi trường (Environment)**` |
| — | `**URL / Build:**` · `**OS:**` · `**Browser / Device:**` · `**Test account:**` | `**URL / Build:**` · `**OS:**` · `**Browser / Device:**` · `**Tài khoản test:**` |
| II | `**II. Preconditions**` | `**II. Điều kiện tiên quyết (Preconditions)**` |
| III | `**III. Steps to Reproduce**` | `**III. Các bước tái hiện (Steps to Reproduce)**` |
| IV | `**IV. Actual Result**` | `**IV. Kết quả thực tế (Actual Result)**` |
| V | `**V. Expected Result**` | `**V. Kết quả mong đợi (Expected Result)**` |
| VI | `**VI. Reproducibility**` | `**VI. Tần suất (Reproducibility)**` |
| VII | `**VII. Notes**` | `**VII. Ghi chú (Notes)**` |
| — | `- Attachments:` | `- Ảnh đính kèm:` |
| — | `Based on <spec>:` | `Căn cứ <spec>:` |

## Body frame (codeblock 2) — English

```
**I. Environment**
- **URL / Build:**
- **OS:**
- **Browser / Device:**
- **Test account:**

**II. Preconditions**
-

**III. Steps to Reproduce**
1.
2.
3.

**IV. Actual Result**
-

**V. Expected Result**
-

**VI. Reproducibility**
Always / Sometimes / Rarely

**VII. Notes**
-
- Attachments: <file name> (<what it shows>) · <file name> (<…>)
```

## Body frame (codeblock 2) — Vietnamese

```
**I. Môi trường (Environment)**
- **URL / Build:**
- **OS:**
- **Browser / Device:**
- **Tài khoản test:**

**II. Điều kiện tiên quyết (Preconditions)**
-

**III. Các bước tái hiện (Steps to Reproduce)**
1.
2.
3.

**IV. Kết quả thực tế (Actual Result)**
-

**V. Kết quả mong đợi (Expected Result)**
-

**VI. Tần suất (Reproducibility)**
Always / Sometimes / Rarely

**VII. Ghi chú (Notes)**
-
- Ảnh đính kèm: <tên file> (<ảnh cho thấy gì>) · <tên file> (<…>)
```

The **Attachments** line is always in section VII (a fixed line of the frame): the user only copies codeblock 2 into the tracker, so this is the only place that reminds them to attach files. Without screenshots write `- Attachments: none (<reason, e.g. the evidence is an API response — attach the .json file>)`.

## Short example

**Title:**
```
[STG][Function][DemoShop] [Login] Password containing special characters → login fails with "Wrong password"
```

**Body:**
```
**I. Environment**
- **URL / Build:** https://staging.example.com
- **OS:** Windows 11
- **Browser / Device:** Chrome 1xx
- **Test account:** test01@example.com

**II. Preconditions**
- Account `test01@example.com` exists, status Active, password `Abc@123#`

**III. Steps to Reproduce**
1. Open the Login page
2. Enter email `test01@example.com`
3. Enter password `Abc@123#`
4. Click "Log in"

**IV. Actual Result**
- The message "Wrong password" is shown and the user stays on the Login page

**V. Expected Result**
- Login succeeds and the user is redirected to the Dashboard

**VI. Reproducibility**
Always

**VII. Notes**
- Expected based on the tester's description, not yet checked against a spec
- Attachments: login-error.png (the "Wrong password" message after step 4)
```

## Full example (checked against a spec, with a passing comparison case)

User input (in Vietnamese): *"Browser 1 login có tick remember rồi tắt browser 1. Case 1: browser 2 login KHÔNG tick thì remember của browser 1 vẫn còn hiệu lực (bug). Case 2: browser 2 login có tick thì remember của browser 1 mất hiệu lực (ok). Môi trường STG."* Spec: "Login FRD v1.4" pasted by the user.

The output follows the user's language (Vietnamese):

**Tiêu đề:**
```
[STG][Function][DemoShop] [Login] Đăng nhập ở trình duyệt khác mà không tick "Ghi nhớ đăng nhập" thì Remember của trình duyệt cũ không bị vô hiệu hóa
```

**Nội dung:**
```
**I. Môi trường (Environment)**
- **URL / Build:** <URL môi trường STG / build>
- **OS:** <vd: Windows 11>
- **Browser / Device:** TD1: <vd: Chrome 1xx> · TD2: <vd: Edge 1xx / máy khác>
- **Tài khoản test:** <email tài khoản test>

**II. Điều kiện tiên quyết (Preconditions)**
- Có tài khoản DemoShop, trạng thái Active
- Chuẩn bị 2 trình duyệt/thiết bị khác nhau: TD1 và TD2
- Cả 2 trình duyệt chưa đăng nhập tài khoản này

**III. Các bước tái hiện (Steps to Reproduce)**
1. Mở TD1, vào trang Login
2. Nhập Email + Password đúng, **tick** "Ghi nhớ đăng nhập", bấm "Đăng nhập" → đăng nhập thành công
3. Đóng hẳn TD1
4. Mở TD2, vào trang Login
5. Nhập cùng Email + Password, **KHÔNG tick** "Ghi nhớ đăng nhập", bấm "Đăng nhập" → đăng nhập thành công
6. Mở lại TD1, vào DemoShop

**IV. Kết quả thực tế (Actual Result)**
- TD1 vẫn tự đăng nhập bằng Remember, không yêu cầu nhập lại Email + Password
- Tức là Remember của TD1 **không bị vô hiệu hóa** sau khi tài khoản đăng nhập thành công ở TD2

**V. Kết quả mong đợi (Expected Result)**
- Ở bước 5, khi đăng nhập thành công ở TD2 thì phiên và Remember của TD1 phải bị vô hiệu hóa, **dù TD2 có tick hay không tick** "Ghi nhớ đăng nhập"
- Ở bước 6, TD1 không được tự đăng nhập, phải hiện màn Login và yêu cầu nhập Email + Password
- Căn cứ Login FRD v1.4:
  - BR-SESSION-04: Khi Login mới thành công, trạng thái Ghi nhớ đăng nhập trên device cũ cũng phải bị vô hiệu hóa
  - FR-27: Vô hiệu hóa Remember của browser/device cũ khi Account Login thành công trên device khác
  - UC-09: Chỉ được Auto Login khi "Không có Login mới hơn trên browser/device khác"
  - AC-29: Device A có Remember → Login thành công Device B → Remember Device A mất hiệu lực
  → Không rule nào yêu cầu TD2 phải tick Remember thì mới vô hiệu hóa Remember của TD1

**VI. Tần suất (Reproducibility)**
Always

**VII. Ghi chú (Notes)**
- Case so sánh: làm y hệt các bước trên nhưng ở bước 5 **có tick** "Ghi nhớ đăng nhập" → Remember của TD1 bị vô hiệu hóa đúng như mong đợi (PASS)
- Nghi ngờ: logic vô hiệu hóa Remember của device cũ đang chỉ chạy khi tạo Remember mới, thay vì chạy mỗi khi Login thành công
- Cần kiểm tra thêm: sau khi TD1 tự đăng nhập lại ở bước 6, phiên của TD2 có bị thay thế không (theo BR-SESSION-01, mỗi Account chỉ có 1 phiên hoạt động)
- Spec tham khảo: Login FRD v1.4 (người dùng dán vào hội thoại)
- Ảnh đính kèm: không có (người dùng chưa gửi ảnh)
```

**Kiểm tra trước khi post:**
- Ảnh cần đính kèm: không có ảnh. Nên chụp màn hình TD1 tự đăng nhập ở bước 6.
- Điền các ô `<...>` ở mục I.
- Bước 6 đang ghi là TD1 tự đăng nhập vào được. Nếu thực tế khác thì sửa mục IV.
- Nếu đã thấy TD2 bị đá ra khi TD1 tự đăng nhập lại thì chuyển ý đó từ Ghi chú lên Kết quả thực tế.
