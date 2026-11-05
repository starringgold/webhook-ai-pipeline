import anthropic
import json

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are an enterprise sales intelligence engine. When given a CRM webhook event payload, analyze it and return ONLY valid JSON in this exact format:

{
  "summary": "One sentence describing what happened and why it matters",
  "signals": ["key signal 1", "key signal 2", "key signal 3"],
  "risk_level": "low",
  "risk_reason": "Brief explanation of the risk assessment",
  "recommended_actions": ["specific action 1", "specific action 2", "specific action 3"]
}

Risk levels: low (healthy, on track), medium (needs attention), high (at risk, act now).
Signals and actions should be specific and actionable, not generic.
Return ONLY the JSON object, no markdown, no explanation."""


def analyze_event(payload: dict) -> dict:
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this CRM event:\n\n{json.dumps(payload, indent=2)}",
            }
        ],
    )

    raw = message.content[0].text.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "summary": "Analysis failed to parse",
            "signals": [],
            "risk_level": "medium",
            "risk_reason": "Could not parse AI response",
            "recommended_actions": ["Review event manually"],
        }
