from flask import Flask, request, jsonify
from analyzer import analyze_event
from slack_notifier import notify_slack
import os

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json()

    if not payload:
        return jsonify({"error": "No JSON payload received"}), 400

    print(f"Received webhook: {payload.get('event', 'unknown event')}")

    analysis = analyze_event(payload)
    notify_slack(payload, analysis)

    return jsonify({"status": "processed", "analysis": analysis})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
