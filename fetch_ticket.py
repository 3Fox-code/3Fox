import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

# Load credentials
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
PROJECT_KEY = os.getenv("PROJECT_KEY")

# JQL Query
jql = f'project = {PROJECT_KEY} AND status = "To Do" ORDER BY created ASC'
url = f"https://{JIRA_DOMAIN}/rest/api/3/search"
headers = {
    "Accept": "application/json"
}
params = {
    "jql": jql,
    "maxResults": 1,
    "fields": "summary,description"
}

# Request
response = requests.get(
    url,
    headers=headers,
    params=params,
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
)

# Output
if response.status_code == 200:
    data = response.json()
    if data["issues"]:
        issue = data["issues"][0]
        key = issue["key"]
        summary = issue["fields"]["summary"]
        description = issue["fields"]["description"]
        print(f"\nTicket: {key}\nSummary: {summary}\n")
    else:
        print("No open tickets found.")
else:
    print(f"Error {response.status_code}: {response.text}")