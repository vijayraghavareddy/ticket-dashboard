$repoRoot = Split-Path -Parent $PSScriptRoot

if ($repoRoot -notmatch '^\\\\wsl\.localhost\\[^\\]+\\(.+)$') {
    throw "This script expects the repo to be under \\wsl.localhost\\<Distro>\\..."
}

$linuxPath = "/" + ($Matches[1] -replace '\\', '/')

$bashCommand = @"
set +e
cd '$linuxPath'
if [ -f .demo_api.pid ]; then
  PID=`$(cat .demo_api.pid)
  kill `$PID >/dev/null 2>&1
  rm -f .demo_api.pid
fi
pkill -f "uvicorn app.main:app --host 127.0.0.1 --port 8000" >/dev/null 2>&1
echo "Demo API stopped (if it was running)."
"@

$bashCommand = $bashCommand -replace "`r", ""

wsl -e bash -lc "$bashCommand"
