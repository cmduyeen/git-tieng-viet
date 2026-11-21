"""Thực thi lệnh Git trong môi trường chuẩn LC_ALL=C."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional

from . import ui


@dataclass
class GitResult:
    returncode: int
    stdout: str
    stderr: str
    cmd_str: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    @property
    def combined(self) -> str:
        return f"{self.stdout}\n{self.stderr}".strip()


def is_git_installed() -> bool:
    return shutil.which("git") is not None


def format_cmd(args: List[str]) -> str:
    parts = ["git"]
    for arg in args:
        if " " in arg or "\t" in arg or arg == "":
            escaped = arg.replace('"', '\\"')
            parts.append(f'"{escaped}"')
        else:
            parts.append(arg)
    return " ".join(parts)


def run_git(args: List[str], interactive: bool = False) -> GitResult:
    """Chạy lệnh Git và trả về GitResult."""
    env = os.environ.copy()
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    cmd = ["git", *args]
    cmd_str = format_cmd(args)

    if interactive:
        proc = subprocess.run(cmd, env=env)
        return GitResult(
            returncode=proc.returncode,
            stdout="",
            stderr="",
            cmd_str=cmd_str,
        )

    proc = subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return GitResult(
        returncode=proc.returncode,
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
        cmd_str=cmd_str,
    )


def get_current_branch() -> Optional[str]:
    res = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    if res.ok and res.stdout and res.stdout != "HEAD":
        return res.stdout.strip()
    return None


def ensure_git_identity() -> bool:
    """Đảm bảo Git đã có user.name và user.email; hỏi người dùng nếu thiếu."""
    name_res = run_git(["config", "--get", "user.name"])
    email_res = run_git(["config", "--get", "user.email"])

    name = os.environ.get("GIT_AUTHOR_NAME") or (name_res.stdout if name_res.ok else "")
    email = os.environ.get("GIT_AUTHOR_EMAIL") or (email_res.stdout if email_res.ok else "")

    if name and email:
        return True

    ui.warn("Đây là lần đầu bạn dùng Git trên máy này. Hãy nhập thông tin ngắn gọn (chỉ hỏi một lần):")
    if not (name_res.ok and name_res.stdout):
        name = ui.ask_text("Tên của bạn (ví dụ: Minh Anh)")
        if not name:
            ui.error("Bạn cần nhập tên để Git ghi nhận người lưu mã nguồn.")
            return False
        run_git(["config", "--global", "user.name", name])

    if not (email_res.ok and email_res.stdout):
        email = ui.ask_text("Email của bạn (ví dụ: minhanh@gmail.com)")
        if not email:
            ui.error("Bạn cần nhập email để Git lưu thông tin tác giả.")
            return False
        run_git(["config", "--global", "user.email", email])

    ui.success("Đã lưu thông tin tác giả cho Git!")
    return True
