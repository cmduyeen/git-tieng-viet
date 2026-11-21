"""Dịch các lỗi phổ biến của Git sang tiếng Việt dễ hiểu kèm hướng dẫn sửa."""

import re
from typing import Optional

from . import ui
from .git_runner import GitResult


def translate_and_print_error(res: GitResult) -> None:
    """Phân tích lỗi từ GitResult và in thông báo tiếng Việt thân thiện."""
    text = res.combined
    lower = text.lower()

    if "not a git repository" in lower:
        ui.error("Thư mục này chưa được khởi tạo Git.")
        ui.info("Gợi ý: Gõ 'vgit batdau' để bắt đầu theo dõi thư mục này.")
        return

    if "author identity unknown" in lower or "please tell me who you are" in lower:
        ui.error("Git chưa biết tên và email của bạn.")
        ui.info("Gợi ý: Gõ 'vgit caidat tacgia' để nhập tên và email.")
        return

    if "nothing to commit" in lower or "working tree clean" in lower:
        ui.success("Bạn chưa sửa file nào mới kể từ lần lưu trước. Mọi thứ đang gọn gàng!")
        return

    if "no configured push destination" in lower or "does not appear to be a git repository" in lower:
        ui.error("Chưa kết nối thư mục này với GitHub (hoặc máy chủ từ xa).")
        ui.info("Gợi ý: Gõ 'vgit ketnoi <link-github>' trước khi đẩy code lên.")
        return

    if "has no upstream branch" in lower:
        ui.error("Nhánh này chưa được liên kết với GitHub.")
        ui.info("Gợi ý: Thử chạy lại 'vgit day'; vgit sẽ tự động liên kết giúp bạn.")
        return

    if "rejected" in lower and ("non-fast-forward" in lower or "fetch first" in lower):
        ui.error("Code trên GitHub đang mới hơn code trên máy bạn.")
        ui.info("Gợi ý: Gõ 'vgit keo' để lấy code mới về và gộp lại, sau đó mới 'vgit day'.")
        return

    if "conflict" in lower or "automatic merge failed" in lower:
        conflicts = _extract_conflict_files(text)
        ui.error("Có xung đột (Merge Conflict): Hai người cùng sửa một chỗ giống nhau.")
        if conflicts:
            ui.warn("Các file đang bị trùng:")
            for f in conflicts:
                print(f"  - {f}")
        ui.info(
            "Cách sửa: Mở file bị trùng, tìm đoạn có dấu '<<<<<<<' để chọn phần code đúng,\n"
            "          xóa các dòng '<<<<<<<', '=======', '>>>>>>>', rồi gõ: vgit luu \"sửa xung đột\""
        )
        return

    if "authentication failed" in lower or "permission denied" in lower or "could not read username" in lower:
        ui.error("Không thể đăng nhập vào GitHub hoặc máy chủ.")
        ui.info("Gợi ý: Kiểm tra lại mật khẩu, Personal Access Token hoặc quyền truy cập repo.")
        return

    if "already exists and is not an empty directory" in lower:
        ui.error("Thư mục đích đã tồn tại và không rỗng.")
        ui.info("Gợi ý: Chọn tên thư mục khác hoặc xóa thư mục cũ trước khi 'vgit tai'.")
        return

    if "could not resolve host" in lower or "unable to access" in lower:
        ui.error("Không kết nối được mạng hoặc sai địa chỉ GitHub.")
        ui.info("Gợi ý: Kiểm tra lại Wi-Fi/Internet và đường dẫn repo.")
        return

    if "did not match any file(s) known to git" in lower:
        ui.error("Không tìm thấy file hoặc nhánh bạn vừa nhập.")
        ui.info("Gợi ý: Gõ 'vgit trangthai' hoặc 'vgit nhanh' để kiểm tra lại tên.")
        return

    # Fallback: hien thi thong bao goc kem loi khuyen
    ui.error("Git báo lỗi:")
    if text:
        print(text)


def _extract_conflict_files(text: str) -> list[str]:
    files: list[str] = []
    for line in text.splitlines():
        m = re.search(r"CONFLICT\s*\([^)]+\):\s*Merge conflict in\s+(.+)", line)
        if m:
            files.append(m.group(1).strip())
    return files
