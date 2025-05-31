import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")

def get_transitions(issue_key):
    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}/transitions"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Accept": "application/json"}
    )
    if response.status_code == 200:
        data = response.json()
        return data["transitions"]
    else:
        print(f"❌ Failed to fetch transitions: {response.status_code} - {response.text}")
        return []

def mark_ticket_done(issue_key, transition_id):
    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}/transitions"
    payload = {
        "transition": {
            "id": transition_id
        }
    }
    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Accept": "application/json", "Content-Type": "application/json"}
    )
    if response.status_code == 204:
        print(f"✅ Ticket {issue_key} marked as done with transition ID {transition_id}.")
        return True
    else:
        print(f"❌ Failed to update ticket {issue_key}. Status: {response.status_code}, Response: {response.text}")
        return False
