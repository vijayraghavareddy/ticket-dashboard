#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

if pgrep -f "uvicorn app.main:app --host 127.0.0.1 --port 8000" >/dev/null 2>&1; then
  echo "API already running at http://127.0.0.1:8000"
else
  nohup .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 > .ticket_dashboard.log 2>&1 &
  echo $! > .ticket_dashboard.pid
  echo "API started at http://127.0.0.1:8000"
fi

echo "Open: http://127.0.0.1:8000/"
