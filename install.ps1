$ErrorActionPreference = "Stop"

Write-Host "[vgit] Dang kiem tra moi truong..." -ForegroundColor Cyan

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[!] May chua co Git. Dang thu cai qua winget..." -ForegroundColor Yellow
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "[Loi] Vui long cai Git tai https://git-scm.com/downloads roi chay lai lenh nay." -ForegroundColor Red
        exit 1
    }
}

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $py) {
    Write-Host "[!] May chua co Python. Dang thu cai Python 3 qua winget..." -ForegroundColor Yellow
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Python.Python.3.12 -e --source winget --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "[Loi] Vui long cai Python tai https://www.python.org/downloads/ roi chay lai." -ForegroundColor Red
        exit 1
    }
}

$RepoUrl = if ($env:VGIT_REPO_URL) { $env:VGIT_REPO_URL } else { "git+https://github.com/cmduyeen/git-tieng-viet.git" }
Write-Host "[vgit] Dang cai dat vgit..." -ForegroundColor Cyan
python -m pip install --user --upgrade $RepoUrl

$UserScripts = python -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))"
$CurrentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserScripts -and ($CurrentUserPath -notlike "*$UserScripts*")) {
    [Environment]::SetEnvironmentVariable("Path", "$CurrentUserPath;$UserScripts", "User")
    $env:Path += ";$UserScripts"
    Write-Host "[vgit] Da tu dong them thu muc lenh vao PATH." -ForegroundColor Green
}

Write-Host "[OK] Cai dat thanh cong! Hay mo terminal moi va go: vgit huongdan" -ForegroundColor Green
