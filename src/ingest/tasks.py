import os
import requests
from celery import Celery
import re

def isBlank(string):
    return not (myString and myString.strip())

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
    lines = issue_description.split("\n")
    line_count = len(lines)

    # Make a comment on the issue that a worker has receieved the event
    comment = "A worker has ingested this issue."
    api_url = f"{base_api_url}/projects/{project_id}/issues/{issue_id}/notes"
    headers = {"PRIVATE-TOKEN": f"{personal_access_token}"}
    data = {"body": comment}
    response = requests.post(api_url, headers=headers, data=data)

    # TODO - Validate the response

    # Create the regex processor

    # https://regex101.com/r/3re90c/1
    pattern = r"{{\s*(\w*)\s*}}|{{\s*(\S+\.\w+)\s*}}|{{\s*(\S+\.\w+)\[(\d*\:?\d*)\]\s*}}|{{\s*(\w+)\s+(\w+)\s+([\S\s]*?)\s*}}|{#\s*(.*?)\s*#}"
    compiled_pattern = re.compile(pattern)

    # Variable lookup storage
    lookup = {}

    for line_index in range(line_count):

        matches = compiled_pattern.finditer(lines[line_index])
        
        for match in matches:

            # Get start and end index for full match
            start = match.start(0)
            end = match.end(0)

            # Variable substitution
            if match.group(1):
                lines[line_index][start:end] = lookup[match.group(1)]

            # File substitution
            if match.group(2):

                # TODO: Get file context
                # TODO: Get file line count

                # Single index slice
                if match.group(4):
                    pass
                # Dual index slice
                elif match.group(5) and match.group(6):
                    pass
                # Start index slice + assumed end of file
                elif match.group(5) and not match.group(6):
                    pass
                # End index slice + assumed start of file
                elif not match.group(5) and match.group(6):
                    pass
                # Error
                else:
                    print("Unhandled file substitution")
            

            # Command substitution
            if match.group(7):

                command = match.group(7)
                variable_name = match.group(8)
                content = match.group(9)
            
            # Comment
            if match.group(10):

                # Remove
                lines[line_index][start:stop] = ""

            # File output operation
            if match.group(11):

                output_file_path = match.group(11)
                content = match.group(12)

            groups = result.groups()
            

        # full_match = match[0]
        # groups = match.groups

        # # Variable substitution
        # if matches[0][0]:
        #     line.replace(matches[0][0], lookup[])

    processed_issue_description = "\n".join(lines) 

    # Pass processed issue description to ollama

    return True
