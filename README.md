# vgit — Git bằng tiếng Việt

[Tiếng Việt](README.md) · [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Buy%20me%20a%20coffee-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/cmduyeen)

**vgit** là công cụ dòng lệnh giúp người mới sử dụng Git dễ dàng bằng các lệnh ngắn gọn tiếng Việt. Khi cần, vgit sẽ dịch lỗi sang tiếng Việt và hiển thị lệnh Git gốc tương ứng để người dùng học dần.

## Yêu cầu

- Git
- Python 3.8 trở lên
- Windows, macOS hoặc Linux

## Cài đặt từ mã nguồn

```powershell
cd D:\Brain2nd\06-Code\vgit
python -m pip install -e .
vgit --version
```

Sau khi cài đặt, gõ `vgit huongdan` để xem danh sách lệnh.

## Cài đặt bằng script

### Windows

Trong PowerShell:

```powershell
irm https://raw.githubusercontent.com/cmduyeen/vgit/main/install.ps1 | iex
```

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/cmduyeen/vgit/main/install.sh | sh
```

## Bắt đầu một dự án mới

```powershell
mkdir du-an-moi
cd du-an-moi
vgit batdau
```

Quy trình lưu thay đổi thường dùng:

```powershell
vgit trangthai
vgit luu "Bổ sung trang chủ"
vgit lichsu
```

## Kết nối GitHub

```powershell
vgit ketnoi https://github.com/ten-tai-khoan/ten-du-an.git
vgit day
```

Lần đầu đẩy nhánh, vgit sẽ tự thử liên kết nhánh hiện tại với `origin`.

## Ví dụ luồng làm việc hàng ngày

```powershell
vgit keo
vgit trangthai
vgit them index.html
vgit thaydoi da-chon
vgit luu "Cập nhật trang chủ"
vgit day
```

## Bảng lệnh

| Lệnh | Việc thực hiện | Git tương ứng |
| :--- | :--- | :--- |
| `vgit batdau` | Khởi tạo dự án Git mới | `git init -b main` |
| `vgit tai <đường-dẫn>` | Tải một dự án về máy | `git clone <đường-dẫn>` |
| `vgit trangthai` | Xem file mới, đã sửa hoặc đã xóa | `git status --porcelain=v1` |
| `vgit them [file]` | Thêm file vào danh sách chuẩn bị lưu | `git add` |
| `vgit bothem [file]` | Bỏ file khỏi danh sách chuẩn bị lưu | `git restore --staged` |
| `vgit thaydoi [da-chon]` | Xem tóm tắt phần đã hoặc chưa thay đổi | `git diff` / `git diff --cached` |
| `vgit luu "mô tả"` | Lưu tất cả thay đổi vào lịch sử Git | `git add . && git commit -m "..."` |
| `vgit lichsu [số-lượng]` | Xem các lần lưu gần nhất | `git log -n <số-lượng>` |
| `vgit nhanh [tên]` | Xem, tạo hoặc chuyển nhánh | `git branch` / `git checkout -b` |
| `vgit ketnoi <đường-dẫn>` | Gắn hoặc cập nhật remote `origin` | `git remote add/set-url origin` |
| `vgit keo` | Tải thay đổi mới nhất về máy | `git pull` |
| `vgit day` | Đẩy thay đổi lên máy chủ | `git push` |
| `vgit dongbo` | Kéo code mới rồi đẩy code hiện tại | `git pull && git push` |
| `vgit quaylai [file]` | Hủy thay đổi chưa lưu, có xác nhận | `git restore` |
| `vgit vat luu [ghi-chú]` | Tạm cất thay đổi để làm việc khác | `git stash push --include-untracked` |
| `vgit vat lay` | Lấy lại thay đổi tạm gần nhất | `git stash pop` |
| `vgit vat xem` | Xem danh sách thay đổi đã tạm cất | `git stash list` |
| `vgit caidat` | Xem các tùy chọn cấu hình | — |
| `vgit huongdan` | Hiển thị hướng dẫn nhanh | — |
| `vgit --version` | Xem phiên bản vgit | — |

Ngoài các lệnh tiếng Việt, vgit cũng cho phép chuyển tiếp lệnh Git gốc. Ví dụ:

```powershell
vgit diff
vgit stash list
vgit remote -v
```

## Cấu hình

### Bật hoặc tắt chế độ Cầu nối

Chế độ Cầu nối hiển thị lệnh Git gốc sau mỗi thao tác:

```powershell
vgit caidat bridge bat
vgit caidat bridge tat
```

### Cấu hình tên và email

```powershell
vgit caidat tacgia
```

Các thông tin này được lưu vào cấu hình Git toàn cục của máy.

## Xử lý lỗi thường gặp

- **Chưa khởi tạo Git**: chạy `vgit batdau`.
- **Chưa kết nối máy chủ**: chạy `vgit ketnoi <đường-dẫn-repo>`.
- **Chưa cấu hình tên/email**: chạy `vgit caidat tacgia`.
- **Code trên máy chủ mới hơn máy local**: chạy `vgit keo`, giải quyết xung đột nếu có, rồi chạy `vgit day`.
- **Không đăng nhập được**: kiểm tra quyền truy cập repo và Personal Access Token nếu dùng GitHub.

## Chạy kiểm thử

```powershell
cd D:\Brain2nd\06-Code\vgit
python -m unittest discover -s tests -v
```

## Bộ công cụ lập trình tiếng Việt

| Công cụ | Mô tả | Link |
| :--- | :--- | :--- |
| **vpy** | Python tiếng Việt (`.vpy`) & trình soạn thảo `vide` | [cmduyeen/vpy](https://github.com/cmduyeen/vpy) |
| **vgit** *(đang xem)* | Git tiếng Việt cho người mới học | [cmduyeen/vgit](https://github.com/cmduyeen/vgit) |
| **vgh** | GitHub CLI (`gh`) tiếng Việt | [cmduyeen/vgh](https://github.com/cmduyeen/vgh) |
| **vwt** | Windows Terminal / PowerShell tiếng Việt | [cmduyeen/vwt](https://github.com/cmduyeen/vwt) |

---

Phát triển bởi [cmduyeen](https://github.com/cmduyeen) · ☕ [Mời mình 1 ly cà phê (Ko-fi)](https://ko-fi.com/cmduyeen)
