# vgit — Git in Vietnamese

[Tiếng Việt](README.md) · [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Buy%20me%20a%20coffee-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/cmduyeen)

**vgit** is a beginner-friendly CLI wrapper that makes Git approachable with short Vietnamese commands, Vietnamese error translations, and a **Bridge Mode** that shows the underlying `git` command after each action so learners naturally pick up standard Git.

## Requirements

- Git
- Python 3.8+
- Windows, macOS, or Linux

## Quick Install

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/cmduyeen/git-tieng-viet/main/install.ps1 | iex
```

### macOS / Linux
```bash
curl -fsSL https://raw.githubusercontent.com/cmduyeen/git-tieng-viet/main/install.sh | sh
```

### From Source
```powershell
git clone https://github.com/cmduyeen/git-tieng-viet.git
cd git-tieng-viet
python -m pip install -e .
vgit --version
```

## Common Commands

| Command | Action | Equivalent Git Command |
| :--- | :--- | :--- |
| `vgit batdau` | Initialize a new Git repository | `git init -b main` |
| `vgit tai <url>` | Clone a repository | `git clone <url>` |
| `vgit trangthai` | Check working tree status | `git status --porcelain=v1` |
| `vgit them [file]` | Stage files | `git add` |
| `vgit bothem [file]` | Unstage files | `git restore --staged` |
| `vgit thaydoi [da-chon]` | View unstaged or staged diff | `git diff` / `git diff --cached` |
| `vgit luu "msg"` | Stage all and commit | `git add . && git commit -m "..."` |
| `vgit lichsu [n]` | View recent commits | `git log -n <n>` |
| `vgit nhanh [name]` | List, create, or switch branches | `git branch` / `git checkout -b` |
| `vgit ketnoi <url>` | Add or update `origin` remote | `git remote add/set-url origin` |
| `vgit keo` | Pull latest changes | `git pull` |
| `vgit day` | Push commits to remote | `git push` |
| `vgit dongbo` | Pull then push | `git pull && git push` |
| `vgit quaylai [file]` | Discard unstaged changes (with confirmation) | `git restore` |
| `vgit huongdan` | Show quick reference | — |

## Vietnamese CLI Ecosystem

| Tool | Description | Repository |
| :--- | :--- | :--- |
| **vpy** | Vietnamese Python (`.vpy`) & `vide` editor | [cmduyeen/python-tieng-viet](https://github.com/cmduyeen/python-tieng-viet) |
| **vgit** *(current)* | Vietnamese Git CLI for beginners | [cmduyeen/git-tieng-viet](https://github.com/cmduyeen/git-tieng-viet) |
| **vgh** | Vietnamese GitHub CLI (`gh`) | [cmduyeen/github-tieng-viet](https://github.com/cmduyeen/github-tieng-viet) |
| **vwt** | Vietnamese Windows Terminal / PowerShell commands | [cmduyeen/terminal-tieng-viet](https://github.com/cmduyeen/terminal-tieng-viet) |

---

Developed by [cmduyeen](https://github.com/cmduyeen) · ☕ [Buy me a coffee (Ko-fi)](https://ko-fi.com/cmduyeen)
