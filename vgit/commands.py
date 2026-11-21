"""Cài đặt các lệnh tiếng Việt cho vgit."""

from typing import Callable, Dict, List

from . import config, error_translator, git_runner, ui


def _bridge_enabled() -> bool:
    return bool(config.load_config().get("bridge_mode", True))


def cmd_batdau(args: List[str]) -> int:
    """Khởi tạo kho Git mới (git init)."""
    res = git_runner.run_git(["init", "-b", "main", *args])
    cmd_used = res.cmd_str
    if not res.ok and "unknown switch" in res.stderr.lower():
        res = git_runner.run_git(["init", *args])
        cmd_used = res.cmd_str

    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    ui.success("Đã khởi tạo dự án Git mới!")
    ui.show_bridge(cmd_used, _bridge_enabled())
    git_runner.ensure_git_identity()
    return 0


def cmd_tai(args: List[str]) -> int:
    """Tải dự án từ GitHub hoặc máy chủ về máy (git clone)."""
    if not args:
        url = ui.ask_text("Dán đường dẫn dự án GitHub cần tải (ví dụ: https://github.com/user/repo.git)")
        if not url:
            ui.error("Chưa có đường dẫn để tải.")
            return 1
        args = [url]

    ui.info("Đang tải dự án về máy...")
    res = git_runner.run_git(["clone", *args])
    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    ui.success("Tải dự án thành công!")
    ui.show_bridge(res.cmd_str, _bridge_enabled())
    return 0


def cmd_trangthai(args: List[str]) -> int:
    """Xem trạng thái các file đang thay đổi (git status)."""
    res = git_runner.run_git(["status", "--porcelain=v1", *args])
    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    branch = git_runner.get_current_branch()
    if branch:
        print(ui.paint(f"Nhánh hiện tại: {branch}", ui.Color.CYAN, ui.Color.BOLD))

    if not res.stdout:
        ui.success("Thư mục sạch sẽ, chưa có thay đổi mới!")
        ui.show_bridge("git status", _bridge_enabled())
        return 0

    print("Các thay đổi chưa được lưu:")
    for line in res.stdout.splitlines():
        if len(line) < 4:
            continue
        code = line[:2]
        filepath = line[3:]
        if code == "??":
            label = ui.paint("  [File mới]  ", ui.Color.GREEN)
        elif "D" in code:
            label = ui.paint("  [Đã xóa]    ", ui.Color.RED)
        elif "R" in code:
            label = ui.paint("  [Đổi tên]   ", ui.Color.BLUE)
        elif "U" in code or code == "AA" or code == "DD":
            label = ui.paint("  [Xung đột]  ", ui.Color.RED, ui.Color.BOLD)
        else:
            label = ui.paint("  [Đã sửa]    ", ui.Color.YELLOW)
        print(f"{label} {filepath}")

    ui.info("Gợi ý: Gõ 'vgit luu \"mô tả thay đổi\"' để lưu lại.")
    ui.show_bridge("git status", _bridge_enabled())
    return 0


def cmd_luu(args: List[str]) -> int:
    """Gộp git add . và git commit -m để lưu mã nguồn nhanh chóng."""
    if not git_runner.ensure_git_identity():
        return 1

    status_res = git_runner.run_git(["status", "--porcelain"])
    if not status_res.ok:
        error_translator.translate_and_print_error(status_res)
        return status_res.returncode

    if not status_res.stdout:
        ui.success("Bạn chưa sửa file nào mới kể từ lần lưu trước. Mọi thứ đang gọn gàng!")
        ui.show_bridge("git status", _bridge_enabled())
        return 0

    message = " ".join(args).strip()
    if not message:
        message = ui.ask_text("Bạn muốn ghi chú gì cho lần lưu này? (ví dụ: thêm nút bấm)")
        if not message:
            ui.warn("Đã hủy lệnh lưu vì chưa nhập ghi chú.")
            return 1

    add_res = git_runner.run_git(["add", "."])
    if not add_res.ok:
        error_translator.translate_and_print_error(add_res)
        return add_res.returncode

    commit_res = git_runner.run_git(["commit", "-m", message])
    if not commit_res.ok:
        error_translator.translate_and_print_error(commit_res)
        return commit_res.returncode

    ui.success(f"Đã lưu thay đổi với ghi chú: \"{message}\"")
    ui.show_bridge(f"{add_res.cmd_str} && {commit_res.cmd_str}", _bridge_enabled())
    return 0


def cmd_day(args: List[str]) -> int:
    """Đẩy code lên GitHub hoặc máy chủ (git push)."""
    ui.info("Đang đẩy code lên máy chủ...")
    res = git_runner.run_git(["push", *args])
    if res.ok:
        ui.success("Đã đẩy code lên thành công!")
        ui.show_bridge(res.cmd_str, _bridge_enabled())
        return 0

    lower = res.combined.lower()
    if "has no upstream branch" in lower:
        branch = git_runner.get_current_branch() or "main"
        ui.info(f"Lần đầu đẩy nhánh '{branch}', đang tự động liên kết với origin...")
        retry = git_runner.run_git(["push", "-u", "origin", branch])
        if retry.ok:
            ui.success(f"Đã liên kết và đẩy nhánh '{branch}' lên thành công!")
            ui.show_bridge(retry.cmd_str, _bridge_enabled())
            return 0
        error_translator.translate_and_print_error(retry)
        return retry.returncode

    if "rejected" in lower and ("non-fast-forward" in lower or "fetch first" in lower):
        ui.warn("Code trên GitHub đang mới hơn code trên máy bạn.")
        if         ui.ask_yes_no("Bạn có muốn kéo code mới về, gộp lại rồi đẩy luôn không?", default=True):
            pull_code = cmd_keo([])
            if pull_code == 0:
                return cmd_day(args)
            return pull_code
        return res.returncode

    error_translator.translate_and_print_error(res)
    return res.returncode


def cmd_keo(args: List[str]) -> int:
    """Kéo code mới nhất từ GitHub hoặc máy chủ về (git pull)."""
    ui.info("Đang kéo code mới về...")
    res = git_runner.run_git(["pull", *args])
    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    if "already up to date" in res.stdout.lower():
        ui.success("Code trên máy bạn đã là bản mới nhất rồi!")
    else:
        ui.success("Đã kéo và cập nhật code mới thành công!")
    ui.show_bridge(res.cmd_str, _bridge_enabled())
    return 0


def cmd_lichsu(args: List[str]) -> int:
    """Xem lịch sử các lần lưu code gần nhất (git log)."""
    limit = "10"
    if args and args[0].isdigit():
        limit = args[0]

    res = git_runner.run_git(["log", "-n", limit, "--pretty=format:%h|%ar|%s"])
    if not res.ok:
        if "does not have any commits yet" in res.combined.lower():
            ui.info("Chưa có lần lưu code nào. Hãy gõ 'vgit luu \"lần đầu\"' để tạo mốc đầu tiên!")
            return 0
        error_translator.translate_and_print_error(res)
        return res.returncode

    if not res.stdout:
        ui.info("Chưa có lịch sử lưu code.")
        return 0

    print(ui.paint(f"Lịch sử {limit} lần lưu gần nhất:", ui.Color.CYAN, ui.Color.BOLD))
    for line in res.stdout.splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            sha, rel_time, msg = parts
            print(f"  {ui.paint(sha, ui.Color.YELLOW)} - {ui.paint(rel_time, ui.Color.GRAY)} - {msg}")
        else:
            print(f"  {line}")

    ui.show_bridge(f"git log --oneline -n {limit}", _bridge_enabled())
    return 0


def cmd_nhanh(args: List[str]) -> int:
    """Xem, tạo hoặc chuyển nhánh làm việc (git branch / checkout)."""
    if not args:
        res = git_runner.run_git(["branch"])
        if not res.ok:
            error_translator.translate_and_print_error(res)
            return res.returncode
        if not res.stdout:
            ui.info("Chưa có nhánh nào (hãy lưu lần đầu bằng 'vgit luu' trước).")
            return 0
        print(ui.paint("Danh sách các nhánh (* là nhánh đang dùng):", ui.Color.CYAN, ui.Color.BOLD))
        for line in res.stdout.splitlines():
            if line.startswith("*"):
                print(ui.paint(f"  {line}", ui.Color.GREEN, ui.Color.BOLD))
            else:
                print(f"  {line}")
        ui.show_bridge("git branch", _bridge_enabled())
        return 0

    branch_name = args[0]
    exists = git_runner.run_git(["show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"])
    if exists.ok:
        res = git_runner.run_git(["checkout", branch_name])
        if not res.ok:
            error_translator.translate_and_print_error(res)
            return res.returncode
        ui.success(f"Đã chuyển sang nhánh '{branch_name}'.")
        ui.show_bridge(res.cmd_str, _bridge_enabled())
        return 0

    if ui.ask_yes_no(f"Nhánh '{branch_name}' chưa có. Bạn có muốn tạo nhánh mới và chuyển sang luôn không?", default=True):
        res = git_runner.run_git(["checkout", "-b", branch_name])
        if not res.ok:
            error_translator.translate_and_print_error(res)
            return res.returncode
        ui.success(f"Đã tạo và chuyển sang nhánh mới '{branch_name}'!")
        ui.show_bridge(res.cmd_str, _bridge_enabled())
        return 0

    return 0


def cmd_quaylai(args: List[str]) -> int:
    """Hoàn tác các thay đổi chưa lưu (có hỏi xác nhận an toàn)."""
    target = args[0] if args else "."
    label = f"file '{target}'" if args else "TẤT CẢ các thay đổi chưa lưu"

    ui.warn(f"Cảnh báo: Hành động này sẽ xóa bỏ {label} và quay về mốc lưu gần nhất.")
    if not ui.ask_yes_no("Bạn có chắc chắn muốn quay lại không?", default=False):
        ui.info("Đã hủy lệnh quay lại, code của bạn vẫn an toàn.")
        return 0

    res = git_runner.run_git(["restore", target])
    if not res.ok and "not a git command" in res.stderr.lower():
        res = git_runner.run_git(["checkout", "--", target])

    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    ui.success(f"Đã khôi phục {label} về trạng thái trước đó.")
    ui.show_bridge(res.cmd_str, _bridge_enabled())
    return 0


def cmd_them(args: List[str]) -> int:
    """Chọn file để chuẩn bị lưu (git add)."""
    targets = args or ["."]
    res = git_runner.run_git(["add", "--", *targets])
    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    label = "tất cả file" if targets == ["."] else ", ".join(targets)
    ui.success(f"Đã chọn {label} để chuẩn bị lưu.")
    ui.show_bridge(res.cmd_str, _bridge_enabled())
    return 0


def cmd_bothem(args: List[str]) -> int:
    """Bỏ file khỏi khu vực chuẩn bị lưu mà không xóa file."""
    if not args:
        res = git_runner.run_git(["restore", "--staged", "."])
    else:
        res = git_runner.run_git(["restore", "--staged", "--", *args])
    if not res.ok:
        reset_args = ["reset"]
        if args:
            reset_args.extend(["--", *args])
        res = git_runner.run_git(reset_args)
    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    ui.success("Đã bỏ các file đã chọn khỏi lần lưu sắp tới.")
    ui.show_bridge(res.cmd_str, _bridge_enabled())
    return 0


def cmd_thaydoi(args: List[str]) -> int:
    """Hiển thị phần code đã sửa (git diff)."""
    staged = bool(args and args[0].lower() in ("da-chon", "staged", "chuando"))
    git_args = ["diff", "--stat"]
    bridge = "git diff --stat"
    if staged:
        git_args = ["diff", "--cached", "--stat"]
        bridge = "git diff --cached --stat"

    res = git_runner.run_git(git_args)
    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    if not res.stdout:
        ui.success("Chưa có thay đổi nào để xem.")
    else:
        print(ui.paint("Tóm tắt thay đổi:", ui.Color.CYAN, ui.Color.BOLD))
        print(res.stdout)

    ui.show_bridge(bridge, _bridge_enabled())
    return 0


def cmd_dongbo(args: List[str]) -> int:
    """Kéo code mới về rồi đẩy code hiện tại lên (git pull && git push)."""
    ui.info("Đang đồng bộ: kéo code mới về trước, sau đó đẩy code hiện tại...")
    pull_args = ["pull", *args]
    pull = git_runner.run_git(pull_args)
    if not pull.ok:
        error_translator.translate_and_print_error(pull)
        return pull.returncode

    push = git_runner.run_git(["push", *args])
    if not push.ok:
        error_translator.translate_and_print_error(push)
        return push.returncode

    ui.success("Đã đồng bộ thư mục với máy chủ thành công!")
    ui.show_bridge(f"{pull.cmd_str} && {push.cmd_str}", _bridge_enabled())
    return 0


def cmd_vat(args: List[str]) -> int:
    """Tạm cất thay đổi (stash) để chuyển việc mà không mất thay đổi."""
    if not args:
        ui.info("Cách dùng:")
        print("  vgit vat luu [ghi-chú]  -> Tạm lưu thay đổi")
        print("  vgit vat lay            -> Lấy lại lần lưu tạm gần nhất")
        print("  vgit vat xem            -> Xem danh sách lần lưu tạm")
        return 0

    action = args[0].lower()
    if action in ("luu", "save", "dat"):
        message = " ".join(args[1:]).strip()
        git_args = ["stash", "push", "--include-untracked"]
        if message:
            git_args.extend(["-m", message])
        res = git_runner.run_git(git_args)
        if not res.ok:
            error_translator.translate_and_print_error(res)
            return res.returncode
        ui.success("Đã tạm lưu thay đổi. Thư mục hiện tại đã trở về sạch sẽ.")
        ui.show_bridge(res.cmd_str, _bridge_enabled())
        return 0

    if action in ("lay", "pop", "phuchoi"):
        res = git_runner.run_git(["stash", "pop"])
        if not res.ok:
            error_translator.translate_and_print_error(res)
            return res.returncode
        ui.success("Đã lấy lại thay đổi tạm và áp dụng vào thư mục.")
        ui.show_bridge(res.cmd_str, _bridge_enabled())
        return 0

    if action in ("xem", "danh-sach", "list"):
        res = git_runner.run_git(["stash", "list"])
        if not res.ok:
            error_translator.translate_and_print_error(res)
            return res.returncode
        if not res.stdout:
            ui.info("Chưa có thay đổi tạm nào.")
        else:
            print(ui.paint("Danh sách thay đổi tạm:", ui.Color.CYAN, ui.Color.BOLD))
            print(res.stdout)
        ui.show_bridge(res.cmd_str, _bridge_enabled())
        return 0

    ui.warn(f"Không hiểu hành động '{action}'. Hãy dùng: luu, lay hoặc xem.")
    return 1


def cmd_ketnoi(args: List[str]) -> int:
    """Kết nối thư mục hiện tại với đường dẫn GitHub (git remote)."""
    url = args[0] if args else ui.ask_text("Dán đường dẫn repo GitHub (ví dụ: https://github.com/user/repo.git)")
    if not url:
        ui.error("Chưa có đường dẫn để kết nối.")
        return 1

    check = git_runner.run_git(["remote", "get-url", "origin"])
    if check.ok:
        res = git_runner.run_git(["remote", "set-url", "origin", url])
    else:
        res = git_runner.run_git(["remote", "add", "origin", url])

    if not res.ok:
        error_translator.translate_and_print_error(res)
        return res.returncode

    ui.success(f"Đã kết nối với máy chủ: {url}")
    ui.show_bridge(res.cmd_str, _bridge_enabled())
    return 0


def cmd_caidat(args: List[str]) -> int:
    """Quản lý cài đặt cho vgit (bridge mode, tác giả)."""
    cfg = config.load_config()
    if not args:
        state = "BẬT" if cfg.get("bridge_mode", True) else "TẮT"
        print(ui.paint("Cài đặt hiện tại của vgit:", ui.Color.CYAN, ui.Color.BOLD))
        print(f"  - Chế độ Cầu nối (hiện lệnh Git gốc): {state}")
        print("Cách đổi:")
        print("  vgit caidat bridge bat   -> Hiện lệnh Git gốc để học dần")
        print("  vgit caidat bridge tat   -> Ẩn lệnh Git gốc cho gọn màn hình")
        print("  vgit caidat tacgia       -> Đổi tên và email tác giả Git")
        return 0

    sub = args[0].lower()
    if sub == "bridge":
        if len(args) < 2:
            ui.info("Hãy chọn: 'vgit caidat bridge bat' hoặc 'vgit caidat bridge tat'")
            return 1
        val = args[1].lower() in ("bat", "on", "true", "1", "co")
        cfg["bridge_mode"] = val
        config.save_config(cfg)
        ui.success(f"Đã {'BẬT' if val else 'TẮT'} chế độ Cầu nối (Bridge Mode).")
        return 0

    if sub == "tacgia":
        name = ui.ask_text("Tên tác giả mới")
        email = ui.ask_text("Email tác giả mới")
        if name:
            git_runner.run_git(["config", "--global", "user.name", name])
        if email:
            git_runner.run_git(["config", "--global", "user.email", email])
        ui.success("Đã cập nhật thông tin tác giả!")
        return 0

    ui.warn(f"Không hiểu tùy chọn '{sub}'. Gõ 'vgit caidat' để xem hướng dẫn.")
    return 1


def cmd_huongdan(args: List[str]) -> int:
    """Hiển thị bảng lệnh vgit dễ hiểu."""
    print(ui.paint("=== vgit - Git tiếng Việt cho người mới ===", ui.Color.CYAN, ui.Color.BOLD))
    rows = [
        ("vgit batdau", "Khởi tạo Git cho thư mục dự án mới (git init)"),
        ("vgit tai <đường-dẫn>", "Tải một dự án từ GitHub về máy (git clone)"),
        ("vgit trangthai", "Xem file vừa sửa, vừa tạo hoặc đã xóa (git status)"),
        ("vgit luu \"mô tả\"", "Lưu lại tất cả thay đổi (git add . && git commit)"),
        ("vgit ketnoi <đường-dẫn>", "Gắn link GitHub cho thư mục này (git remote add)"),
        ("vgit day", "Đẩy code từ máy lên GitHub (git push)"),
        ("vgit keo", "Lấy code mới từ GitHub về máy (git pull)"),
        ("vgit lichsu", "Xem lại các mốc đã lưu (git log)"),
        ("vgit nhanh [tên]", "Xem hoặc tạo/chuyển nhánh code (git branch)"),
        ("vgit quaylai [file]", "Hủy bỏ sửa đổi chưa lưu (git restore)"),
        ("vgit caidat", "Bật/tắt chế độ Cầu nối và đổi tên/email"),
        ("vgit them [file]", "Chọn file để chuẩn bị lưu (git add)"),
        ("vgit bothem [file]", "Bỏ file khỏi lần lưu sắp tới (git restore --staged)"),
        ("vgit thaydoi [da-chon]", "Xem tóm tắt thay đổi (git diff)"),
        ("vgit dongbo", "Kéo code mới về rồi đẩy code lên (git pull && git push)"),
        ("vgit vat luu [ghi-chú]", "Tạm cất thay đổi để chuyển việc (git stash)"),
        ("vgit vat lay", "Lấy lại thay đổi tạm gần nhất (git stash pop)"),
        ("vgit vat xem", "Xem danh sách thay đổi tạm"),
    ]
    for cmd, desc in rows:
        print(f"  {ui.paint(cmd.ljust(22), ui.Color.GREEN)} {desc}")
    print()
    print(ui.paint("Mẹo: Bạn cũng có thể gõ các lệnh Git gốc như 'vgit diff' hoặc 'vgit stash'.", ui.Color.GRAY))
    return 0


COMMAND_MAP: Dict[str, Callable[[List[str]], int]] = {
    "batdau": cmd_batdau,
    "tao": cmd_batdau,
    "khoitao": cmd_batdau,
    "tai": cmd_tai,
    "clone": cmd_tai,
    "trangthai": cmd_trangthai,
    "xem": cmd_trangthai,
    "luu": cmd_luu,
    "commit": cmd_luu,
    "them": cmd_them,
    "chon": cmd_them,
    "bothem": cmd_bothem,
    "bo-chon": cmd_bothem,
    "day": cmd_day,
    "push": cmd_day,
    "keo": cmd_keo,
    "pull": cmd_keo,
    "dongbo": cmd_dongbo,
    "sync": cmd_dongbo,
    "lichsu": cmd_lichsu,
    "nhanh": cmd_nhanh,
    "branch": cmd_nhanh,
    "quaylai": cmd_quaylai,
    "restore": cmd_quaylai,
    "ketnoi": cmd_ketnoi,
    "remote": cmd_ketnoi,
    "thaydoi": cmd_thaydoi,
    "diff": cmd_thaydoi,
    "vat": cmd_vat,
    "stash": cmd_vat,
    "caidat": cmd_caidat,
    "huongdan": cmd_huongdan,
    "help": cmd_huongdan,
    "-h": cmd_huongdan,
    "--help": cmd_huongdan,
}
