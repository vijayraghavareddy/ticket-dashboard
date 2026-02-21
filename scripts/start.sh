#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PORT="${1:-8000}"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

# ---------------------------------------------------------------------------
# Check if our own dashboard process is already running on the target port
# ---------------------------------------------------------------------------
if [ -f .ticket_dashboard.pid ]; then
  OLD_PID=$(cat .ticket_dashboard.pid)
  if kill -0 "$OLD_PID" 2>/dev/null; then
    echo "API already running (PID $OLD_PID) at http://127.0.0.1:${PORT}"
    echo "Open: http://127.0.0.1:${PORT}/"
    exit 0
  else
    # Stale PID file – clean up
    rm -f .ticket_dashboard.pid
  fi
fi

# ---------------------------------------------------------------------------
# Detect if another process occupies the port and offer to pick a free one
# ---------------------------------------------------------------------------
port_in_use() {
  # Returns 0 (true) when the port is occupied
  ss -tlnH "sport = :$1" 2>/dev/null | grep -q "LISTEN" 2>/dev/null \
    || lsof -iTCP:"$1" -sTCP:LISTEN -t >/dev/null 2>&1
}

if port_in_use "$PORT"; then
  echo "WARNING: Port ${PORT} is already in use by another process."
  # Try ports 8001-8020 to find a free one
  for CANDIDATE in $(seq $((PORT + 1)) $((PORT + 20))); do
    if ! port_in_use "$CANDIDATE"; then
      PORT=$CANDIDATE
      echo "Using available port ${PORT} instead."
      break
    fi
  done

  # If still occupied after scanning, abort
  if port_in_use "$PORT"; then
    echo "ERROR: Could not find a free port in range. Free port ${1:-8000} and retry."
    exit 1
  fi
fi

nohup .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port "$PORT" > .ticket_dashboard.log 2>&1 &
echo $! > .ticket_dashboard.pid
echo "API started at http://127.0.0.1:${PORT} (PID $!)"
echo "Open: http://127.0.0.1:${PORT}/"
