param(
    [switch]$SkipInstall,
    [switch]$NoBrowser
)

$repoRoot = Split-Path -Parent $PSScriptRoot

if ($repoRoot -notmatch '^\\\\wsl\.localhost\\[^\\]+\\(.+)$') {
    throw "This script expects the repo to be under \\wsl.localhost\\<Distro>\\..."
}

$linuxPath = "/" + ($Matches[1] -replace '\\', '/')
$installFlag = if ($SkipInstall) { "0" } else { "1" }

$bashCommand = @"
set -e
cd '$linuxPath'
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
if [ '$installFlag' = '1' ]; then
  pip install -r requirements.txt
fi
if pgrep -f "uvicorn app.main:app --host 127.0.0.1 --port 8000" >/dev/null 2>&1; then
  echo "API already running on http://127.0.0.1:8000"
else
  nohup .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 > .ticket_dashboard.log 2>&1 &
  echo $! > .ticket_dashboard.pid
  echo "API started on http://127.0.0.1:8000"
fi
"@

$bashCommand = $bashCommand -replace "`r", ""

wsl -e bash -lc "$bashCommand"

if ($LASTEXITCODE -ne 0) {
  throw "Failed to start API in WSL. See errors above."
}

Start-Sleep -Seconds 1

if (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:8000/"
}

Write-Host "API is available at http://127.0.0.1:8000/"
Write-Host "Logs: .ticket_dashboard.log (inside WSL repo root)"
