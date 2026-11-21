#!/usr/bin/env sh
set -eu

echo "[vgit] Dang kiem tra moi truong..."

if ! command -v git >/dev/null 2>&1; then
    echo "[Loi] May chua co Git. Hay cai Git truoc roi chay lai."
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "[Loi] May chua co Python 3. Hay cai Python 3 truoc roi chay lai."
    exit 1
fi

REPO_URL="${VGIT_REPO_URL:-git+https://github.com/cmduyeen/git-tieng-viet.git}"

if command -v pipx >/dev/null 2>&1; then
    pipx install --force "$REPO_URL"
else
    python3 -m pip install --user --upgrade "$REPO_URL"
fi

echo "[OK] Cai dat thanh cong! Hay go: vgit huongdan"
