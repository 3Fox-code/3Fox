import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

def readable_description(desc):
    if not desc or 'content' not in desc:
        return ""
    
    def extract_text(contents):
        result = ""
        for item in contents:
            if item["type"] == "text":
                result += item.get("text", "")
            elif "content" in item:
                result += extract_text(item["content"])
            if item["type"] == "paragraph":
                result += "\n"
            elif item["type"] == "heading":
                level = item.get("attrs", {}).get("level", 1)
                result += "\n" + ("#" * level) + " "
                result += extract_text(item["content"]) + "\n"
            elif item["type"] == "listItem":
                result += "- " + extract_text(item["content"]) + "\n"
            elif item["type"] == "bulletList":
                result += extract_text(item["content"])
            elif item["type"] == "orderedList":
                result += extract_text(item["content"])
        return result

    return extract_text(desc.get("content", []))

def fetch_ticket():
    # Load credentials inside function or globally (your choice)
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
    PROJECT_KEY = os.getenv("PROJECT_KEY")

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

    response = requests.get(
        url,
        headers=headers,
        params=params,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    )

    if response.status_code == 200:
        data = response.json()
        if data["issues"]:
            issue = data["issues"][0]
            key = issue["key"]
            summary = issue["fields"]["summary"]
            description = issue["fields"]["description"]
            readable_desc = readable_description(description)
            return {"key": key, "summary": summary, "description": readable_desc}
        else:
            print("No open tickets found.")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


# If you want to test standalone:
if __name__ == "__main__":
    ticket = fetch_ticket()
    if ticket:
        print(f"\nTicket: {ticket['key']}\nSummary: {ticket['summary']}\nDescription:\n{ticket['description']}")
