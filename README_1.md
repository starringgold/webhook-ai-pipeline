# ✦ Webhook to AI Pipeline

> Receive a CRM event. Get an AI-generated risk analysis in Slack within seconds.

Built to show how AI can be dropped into existing enterprise event streams — no rearchitecting required.

---

## What it does

1. Receives a webhook POST (from HubSpot, Salesforce, or any CRM)
2. Passes the payload to Claude for structured signal extraction
3. Posts a formatted risk report to a Slack channel

The result: your team gets instant AI-powered analysis on every deal event, without changing how the CRM works.

---

## Architecture

```
CRM / Webhook Source
        |
        v
  POST /webhook
        |
        v
   analyzer.py  <-->  Claude API (claude-3-5-haiku)
        |
        v
slack_notifier.py  -->  Slack Channel
```

---

## Stack

- **Backend:** Python, Flask
- **AI:** Anthropic Claude (claude-3-5-haiku)
- **Integrations:** Slack Incoming Webhooks
- **Deploy:** Render

---

## Run locally

```bash
git clone https://github.com/starringgold/webhook-ai-pipeline.git
cd webhook-ai-pipeline

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Add your ANTHROPIC_API_KEY and SLACK_WEBHOOK_URL to .env

python server.py
```

Test it:

```bash
bash test_webhook.sh
```

---

## Get a Slack Webhook URL

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app
2. Under "Features", click **Incoming Webhooks** and activate it
3. Click **Add New Webhook to Workspace** and pick a channel
4. Copy the webhook URL into your `.env` as `SLACK_WEBHOOK_URL`

---

## Deploy to Render

1. Push this repo to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Build command: `pip install -r requirements.txt`
4. Start command: `python server.py`
5. Add environment variables: `ANTHROPIC_API_KEY` and `SLACK_WEBHOOK_URL`

Then fire a live test from your terminal:

```bash
curl -X POST https://your-app.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "deal_updated",
    "deal_name": "Acme Corp Enterprise",
    "stage": "Negotiation",
    "notes": "Champion went dark, competitor pressure, procurement now involved"
  }'
```

---

## Example Slack output

**🔴 CRM Alert: Acme Corp Enterprise**

*Event:* Deal Updated
*Analysis:* High-risk deal showing champion disengagement and competitive threat during negotiation phase.

**Key Signals:**
- Champion has been unresponsive for one week
- Procurement involvement signals unexpected internal friction
- Competitor offering 20% discount creates pricing pressure

**Recommended Actions:**
- Re-engage champion with executive sponsor outreach this week
- Prepare ROI analysis and competitive battlecard
- Request internal champion to identify and neutralize procurement blocker

**Risk Assessment:** 🔴 HIGH — Multiple simultaneous risk signals with no mitigation currently in progress

---

## Related projects

- [Escalation Decoder](https://github.com/starringgold/escalation-decoder) — Paste a customer escalation, get root cause, stakeholder emotions, and three response options

---

## Author

**Star Ringgold** — Senior Technical CSM and AI builder  
[Portfolio](https://star-ringgold.dev) · [LinkedIn](https://linkedin.com/in/star-ringgold)
