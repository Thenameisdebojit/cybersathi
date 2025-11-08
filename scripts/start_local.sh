#!/usr/bin/env bash
# scripts/start_local.sh
# Start CyberSathi local stack via docker-compose (Linux / macOS)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/infra/docker-compose.yml"

echo "🔎 Repo root: $REPO_ROOT"
if [ ! -f "$COMPOSE_FILE" ]; then
  echo "❌ docker-compose file not found at $COMPOSE_FILE"
  exit 1
fi

cd "$REPO_ROOT/infra"

echo "🚀 Building and starting services with docker-compose..."
docker-compose -f docker-compose.yml up --build -d

echo "⏳ Waiting for services to become healthy..."
# short wait; adjust if needed
sleep 6

echo "✅ Services started:"
echo "  Backend: http://localhost:8000"
echo "  Rasa:    http://localhost:5005"
echo "  Frontend: http://localhost:5173 (or http://localhost if nginx on port 80)"
echo ""
echo "To view logs: docker-compose -f $COMPOSE_FILE logs -f backend"
