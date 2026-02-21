#!/usr/bin/env bash
set +e

cd "$(dirname "$0")/.."

if [ -f .ticket_dashboard.pid ]; then
  PID=$(cat .ticket_dashboard.pid)
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "Stopped Ticket Dashboard API (PID $PID)."
  else
    echo "PID $PID is not running (stale PID file)."
  fi
  rm -f .ticket_dashboard.pid
else
  echo "No PID file found. The API may not be running."
fi
