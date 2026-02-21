param(
    [switch]$SkipInstall,
    [switch]$NoBrowser,
    [int]$Port = 8000
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

PORT=$Port

# Check for stale PID file
if [ -f .ticket_dashboard.pid ]; then
  OLD_PID=`$(cat .ticket_dashboard.pid)
  if kill -0 "`$OLD_PID" 2>/dev/null; then
    echo "API already running (PID `$OLD_PID) at http://127.0.0.1:`$PORT"
    echo "`$PORT"
    exit 0
  else
    rm -f .ticket_dashboard.pid
  fi
fi

# Detect port conflicts and auto-select a free port
port_in_use() {
  ss -tlnH "sport = :`$1" 2>/dev/null | grep -q "LISTEN" 2>/dev/null \
    || lsof -iTCP:"`$1" -sTCP:LISTEN -t >/dev/null 2>&1
}

if port_in_use "`$PORT"; then
  echo "WARNING: Port `$PORT is already in use by another process."
  for CANDIDATE in `$(seq `$((`$PORT + 1)) `$((`$PORT + 20))); do
    if ! port_in_use "`$CANDIDATE"; then
      PORT=`$CANDIDATE
      echo "Using available port `$PORT instead."
      break
    fi
  done
  if port_in_use "`$PORT"; then
    echo "ERROR: Could not find a free port. Free port $Port and retry."
    exit 1
  fi
fi

nohup .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port "`$PORT" > .ticket_dashboard.log 2>&1 &
echo `$! > .ticket_dashboard.pid
echo "API started on http://127.0.0.1:`$PORT (PID `$!)"
echo "`$PORT"
"@

$bashCommand = $bashCommand -replace "`r", ""

$output = wsl -e bash -lc "$bashCommand"

if ($LASTEXITCODE -ne 0) {
  throw "Failed to start API in WSL. See errors above."
}

# The last line of output is the actual port used
$actualPort = ($output | Select-Object -Last 1).Trim()
$output | Select-Object -SkipLast 1 | ForEach-Object { Write-Host $_ }

Start-Sleep -Seconds 1

if (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:${actualPort}/"
}

Write-Host "API is available at http://127.0.0.1:${actualPort}/"
Write-Host "Logs: .ticket_dashboard.log (inside WSL repo root)"
