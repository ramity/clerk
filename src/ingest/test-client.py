import requests
import json
import os

url = "http://localhost:5000/ingest"
payload_path = "issue-create-request.json"

with open(payload_path, "r") as file:
    data = json.load(file)

headers = { "X-Gitlab-Token": os.getenv("TOKEN"), "X-Gitlab-Event": "Issue Hook" }
response = requests.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
