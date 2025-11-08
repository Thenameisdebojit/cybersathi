#!/usr/bin/env bash
# scripts/demo.sh
# Create a demo complaint via the API (Linux / macOS)
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"
ENDPOINT="$API_URL/api/v1/complaints/"

echo "Creating demo complaint at $ENDPOINT"

payload='{
  "name": "Demo User",
  "phone": "+919900000000",
  "language": "en",
  "incident_type": "upi_scam",
  "description": "Demo: lost money via UPI to a scammer",
  "amount": 2500
}'

# prefer curl; check jq for pretty print
if ! command -v curl >/dev/null 2>&1; then
  echo "❌ curl is required to run demo.sh"
  exit 1
fi

if command -v jq >/dev/null 2>&1; then
  curl -s -X POST "$ENDPOINT" -H "Content-Type: application/json" -d "$payload" | jq .
else
  curl -s -X POST "$ENDPOINT" -H "Content-Type: application/json" -d "$payload"
  echo
fi

echo "✅ Demo request sent."
