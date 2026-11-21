"""Điểm khởi chạy cho lệnh `vgit`."""

import sys
from typing import List, Optional

from . import __version__, commands, git_runner, ui


def main(argv: Optional[List[str]] = None) -> int:
    ui.enable_windows_ansi()
    args = sys.argv[1:] if argv is None else argv

    if not args:
        return commands.cmd_huongdan([])

    cmd_name = args[0].lower()
    rest = args[1:]

    if cmd_name in ("-v", "--version", "phienban"):
        print(f"vgit phiên bản {__version__}")
        return 0

    if cmd_name in ("-h", "--help", "help", "huongdan"):
        return commands.cmd_huongdan(rest)

    if not git_runner.is_git_installed():
        ui.error("Máy của bạn chưa cài đặt Git!")
        ui.info("Hãy tải Git tại: https://git-scm.com/downloads (hoặc chạy 'winget install Git.Git' trên Windows).")
        return 1

    handler = commands.COMMAND_MAP.get(cmd_name)
    if handler is not None:
        return handler(rest)

    # Cho phép dùng lệnh Git gốc trực tiếp qua vgit.
    res = git_runner.run_git(args, interactive=True)
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
