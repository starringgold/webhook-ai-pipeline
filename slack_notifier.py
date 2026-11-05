import requests
import os

RISK_EMOJI = {
    "low": "🟢",
    "medium": "🟡",
    "high": "🔴",
}

RISK_LABEL = {
    "low": "LOW",
    "medium": "MEDIUM",
    "high": "HIGH",
}


def notify_slack(payload: dict, analysis: dict) -> None:
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("No SLACK_WEBHOOK_URL set — skipping Slack notification")
        return

    risk = analysis.get("risk_level", "medium")
    emoji = RISK_EMOJI.get(risk, "🟡")
    label = RISK_LABEL.get(risk, "MEDIUM")

    deal_name = payload.get("deal_name", payload.get("account", "Unknown"))
    event_type = payload.get("event", "crm_event").replace("_", " ").title()

    signals = "\n".join(f"• {s}" for s in analysis.get("signals", []))
    actions = "\n".join(f"• {a}" for a in analysis.get("recommended_actions", []))

    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} CRM Alert: {deal_name}",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Event:* {event_type}\n*Analysis:* {analysis.get('summary', '')}",
                },
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Key Signals:*\n{signals or '• None identified'}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Recommended Actions:*\n{actions or '• No actions required'}",
                    },
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Risk Assessment:* {emoji} {label} — {analysis.get('risk_reason', '')}",
                },
            },
            {"type": "divider"},
        ]
    }

    response = requests.post(webhook_url, json=message)

    if response.status_code != 200:
        print(f"Slack error {response.status_code}: {response.text}")
    else:
        print(f"Slack notification sent for: {deal_name}")
