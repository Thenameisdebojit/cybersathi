#!/usr/bin/env bash
# scripts/stop_services.sh
# Stop CyberSathi docker-compose stack (Linux / macOS)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/infra/docker-compose.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "❌ docker-compose.yml not found at $COMPOSE_FILE"
  exit 1
fi

cd "$REPO_ROOT/infra"
echo "🛑 Stopping docker-compose stack..."
docker-compose -f docker-compose.yml down --volumes --remove-orphans

echo "✅ Stack stopped."
