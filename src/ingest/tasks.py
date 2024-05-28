import os
import requests
from celery import Celery

celery = Celery("tasks", backend=os.getenv("CELERY_BROKER_URL"), broker=os.getenv("CELERY_RESULT_BACKEND"))

@celery.task
def add(x, y):
    return x + y

@celery.task
def ingest_issue_event(event):

    # Config
    base_api_url = "http://clerk_gitlab/api/v4"
    personal_access_token = os.getenv("GITLAB_API_ACCESS_TOKEN")

    # Access properties on passed event
    project_id = event["project"]["id"]
    issue_id = event["object_attributes"]["id"]
    issue_description = event["object_attributes"]["description"]
    issue_description_lines = issue_description.split("\n")

    # Make a comment on the issue that a worker has receieved the event
    comment = "A worker has ingested this issue."
    api_url = f"{base_api_url}/projects/{project_id}/issues/{issue_id}/notes"
    headers = {"PRIVATE-TOKEN": f"{personal_access_token}"}
    data = {"body": comment}
    response = requests.post(api_url, headers=headers, data=data)

    # TODO - Validate the response

    # TODO - Do something with issue_description_lines

    return True
