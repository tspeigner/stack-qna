#!/bin/bash
# start_all.sh - Start backend (Flask), frontend (Flutter), and auto-reload on code changes
# Usage: ./start_all.sh

set -e

# Colors for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
  echo -e "${YELLOW}[INFO]${NC} $1"
}

error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Start Flask backend with auto-reload and logging
start_backend() {
  log "Starting Flask backend on port 8001..."
  cd backend || exit 1
  FLASK_APP=flask_app.py FLASK_ENV=development flask run --host=0.0.0.0 --port=8001 2>&1 | tee ../backend.log &
  cd ..
}

# Start Flutter frontend with hot reload
start_frontend() {
  log "Starting Flutter frontend (macOS, hot reload enabled)..."
  cd frontend || exit 1
  flutter run 2>&1 | tee ../frontend.log &
  cd ..
}

# Watch for code changes and print a reminder
watch_changes() {
  log "Watching for code changes in backend/ and frontend/ (auto-reload enabled by Flask and Flutter)."
  log "Check backend.log and frontend.log for error output."
}

# Main
trap 'error "Script interrupted."; exit 1' INT

start_backend
sleep 2 # Give backend time to start
start_frontend
watch_changes

wait
