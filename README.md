# 🌿 git-tieng-viet (`vgit`) — Dùng Git dễ như tiếng Việt

[Tiếng Việt](README.md) · [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Buy%20me%20a%20coffee-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/cmduyeen)

**`vgit`** giúp người mới dùng Git dễ dàng bằng các lệnh tiếng Việt ngắn gọn (`vgit batdau`, `vgit luu`, `vgit day`), đồng thời tự động giải thích lỗi và dạy bạn lệnh Git chuẩn ngay trong lúc làm việc.

## ✨ Điểm nổi bật

- **Không cần nhớ lệnh Git khó:** Thay vì nhớ `git add . && git commit -m "..."`, bạn chỉ cần gõ `vgit luu "nội dung"`.
- **Chế độ Cầu nối (vừa làm vừa học):** Sau mỗi thao tác, `vgit` hiển thị lệnh `git` gốc tương ứng để bạn làm quen dần với quy trình chuẩn quốc tế.
- **Dịch lỗi Git sang tiếng Việt:** Khi gặp xung đột code, chưa cấu hình tên/email hay lỗi push, `vgit` dịch nguyên nhân và gợi ý cách xử lý cụ thể bằng tiếng Việt.
- **An toàn cho người mới:** Các lệnh có nguy cơ mất thay đổi (như `vgit quaylai`) luôn có bước xác nhận rõ ràng trước khi thực hiện.
- **Nhẹ & đa nền tảng:** Chạy mượt trên Windows, macOS, Linux; không cần cài thêm thư viện ngoài.

---

## ⚡ Cài đặt trong 30 giây

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/cmduyeen/git-tieng-viet/main/install.ps1 | iex
```

### macOS / Linux
```bash
curl -fsSL https://raw.githubusercontent.com/cmduyeen/git-tieng-viet/main/install.sh | sh
```

### Hoặc cài từ mã nguồn
```powershell
git clone https://github.com/cmduyeen/git-tieng-viet.git
cd git-tieng-viet
python -m pip install -e .
vgit --version
```

---

## 🚀 Thực hành quy trình 1 phút

```powershell
# 1. Tạo dự án mới
mkdir du-an-cua-toi
cd du-an-cua-toi
vgit batdau

# 2. Kiểm tra & lưu thay đổi
vgit trangthai
vgit luu "Tạo trang chủ đầu tiên"

# 3. Kết nối GitHub và đẩy code lên
vgit ketnoi https://github.com/ten-cua-ban/du-an-cua-toi.git
vgit day
```

---

## 📖 Bảng lệnh `vgit`

| Lệnh `vgit` | Việc thực hiện | Lệnh Git gốc tương ứng |
| :--- | :--- | :--- |
| `vgit batdau` | Khởi tạo dự án Git mới | `git init -b main` |
| `vgit tai <url>` | Tải dự án từ GitHub về máy | `git clone <url>` |
| `vgit trangthai` | Xem file mới, đã sửa hoặc đã xóa | `git status --porcelain=v1` |
| `vgit them [file]` | Chọn file chuẩn bị lưu | `git add` |
| `vgit bothem [file]` | Bỏ chọn file | `git restore --staged` |
| `vgit thaydoi [da-chon]` | Xem chi tiết những gì đã sửa | `git diff` / `git diff --cached` |
| `vgit luu "mô tả"` | Lưu tất cả thay đổi vào lịch sử | `git add . && git commit -m "..."` |
| `vgit lichsu [số-lượng]` | Xem các lần lưu gần nhất | `git log -n <số-lượng>` |
| `vgit nhanh [tên]` | Xem, tạo hoặc chuyển nhánh | `git branch` / `git checkout -b` |
| `vgit ketnoi <url>` | Gắn hoặc đổi đường dẫn GitHub `origin` | `git remote add/set-url origin` |
| `vgit keo` | Tải code mới nhất từ GitHub về | `git pull` |
| `vgit day` | Đẩy code từ máy lên GitHub | `git push` |
| `vgit dongbo` | Kéo code mới rồi đẩy code lên | `git pull && git push` |
| `vgit quaylai [file]` | Hủy thay đổi chưa lưu (có hỏi xác nhận) | `git restore` |
| `vgit vat luu [ghi-chú]` | Cất tạm code đang làm dở | `git stash push --include-untracked` |
| `vgit vat lay` | Lấy lại phần code đã cất tạm | `git stash pop` |
| `vgit vat xem` | Xem danh sách đã cất tạm | `git stash list` |
| `vgit caidat bridge bat\|tat` | Bật/tắt chế độ hiển thị lệnh Git gốc | — |
| `vgit caidat tacgia` | Cài tên và email cho Git | `git config --global user.*` |
| `vgit huongdan` | Xem bảng hướng dẫn nhanh | — |

*(Bạn cũng có thể gõ bất kỳ lệnh Git gốc nào qua `vgit`, ví dụ `vgit diff`, `vgit remote -v`.)*

---

## 🧰 Bộ công cụ lập trình tiếng Việt

| Công cụ | Mô tả | Link |
| :--- | :--- | :--- |
| **python-tieng-viet** | Python tiếng Việt (`vpy`) & trình soạn thảo `vide` | [cmduyeen/python-tieng-viet](https://github.com/cmduyeen/python-tieng-viet) |
| **git-tieng-viet** *(đang xem)* | Git tiếng Việt (`vgit`) cho người mới học | [cmduyeen/git-tieng-viet](https://github.com/cmduyeen/git-tieng-viet) |
| **github-tieng-viet** | GitHub CLI tiếng Việt (`vgh`) | [cmduyeen/github-tieng-viet](https://github.com/cmduyeen/github-tieng-viet) |
| **terminal-tieng-viet** | Windows Terminal / PowerShell tiếng Việt (`vwt`) | [cmduyeen/terminal-tieng-viet](https://github.com/cmduyeen/terminal-tieng-viet) |

---

[MIT License](LICENSE) · Phát triển bởi [cmduyeen](https://github.com/cmduyeen) · ☕ [Mời mình 1 ly cà phê (Ko-fi)](https://ko-fi.com/cmduyeen)
