import os
from flask import Flask, request, jsonify
from tasks import celery, ingest_issue_event

flask = Flask(__name__)

@flask.route("/ingest", methods=["POST"])
def webhook_ingest():

    token = request.headers["X-Gitlab-Token"]

    # Reject if token not present
    if not token:
        return jsonify({"error": "{token}"})

    # Reject if token is not valid
    if token != os.getenv("TOKEN"):
        return jsonify({"error": "token"})

    event = request.headers.get("X-Gitlab-Event")

    if event == "Issue Hook":
        task = ingest_issue_event.delay(request.json)
        return jsonify({"created": task.id})

    return jsonify({"error": "event not supported"})

flask.run(host="0.0.0.0", debug=True)
