#!/bin/bash
# Run locally:   bash test_webhook.sh
# Run deployed:  BASE_URL=https://your-app.onrender.com bash test_webhook.sh

BASE_URL=${BASE_URL:-http://localhost:5000}

echo "Sending test webhook to $BASE_URL..."

curl -s -X POST "$BASE_URL/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "deal_updated",
    "deal_name": "Acme Corp Enterprise",
    "stage": "Negotiation",
    "amount": 125000,
    "close_date": "2026-12-15",
    "owner": "sarah.chen@company.com",
    "notes": "Champion went dark last week. Procurement now involved unexpectedly. Competitor offering 20% discount. Legal review delayed by two weeks."
  }' | python3 -m json.tool
