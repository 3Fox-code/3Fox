import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

def readable_description(desc):
    if not desc or 'content' not in desc:
        return "No description available."
    
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

def fetch_all_tickets():
    # Load variables and validate
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
    PROJECT_KEY = os.getenv("PROJECT_KEY")

    if not all([JIRA_EMAIL, JIRA_API_TOKEN, JIRA_DOMAIN, PROJECT_KEY]):
        print("❌ Missing one or more environment variables. Please check your .env file.")
        return []

    print("✅ Environment variables loaded.")

    jql = f'project = {PROJECT_KEY} AND status = "To Do" ORDER BY created ASC'
    url = f"https://{JIRA_DOMAIN}/rest/api/3/search"
    headers = {
        "Accept": "application/json"
    }
    params = {
        "jql": jql,
        "maxResults": 50,
        "fields": "summary,description"
    }

    print(f"📡 Fetching tickets from: {url}")

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
        )
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

    if response.status_code == 200:
        data = response.json()
        issues = data.get("issues", [])
        if not issues:
            print("⚠️ No open tickets found.")
            return []

        print(f"✅ {len(issues)} tickets fetched.")
        tickets = []
        for issue in issues:
            key = issue["key"]
            summary = issue["fields"]["summary"]
            description = readable_description(issue["fields"].get("description", {}))
            tickets.append({"key": key, "summary": summary, "description": description})
        return tickets
    else:
        print(f"❌ API Error {response.status_code}: {response.text}")
        return []

def choose_ticket(tickets):
    print("\n🎫 Available Tickets:\n")
    for idx, ticket in enumerate(tickets):
        print(f"{idx + 1}. [{ticket['key']}] {ticket['summary']}")

    try:
        choice = int(input("\n🔍 Enter the number of the ticket you want to work on: ")) - 1
        if 0 <= choice < len(tickets):
            return tickets[choice]
        else:
            print("⚠️ Invalid selection. Out of range.")
            return None
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")
        return None

# Entry point
if __name__ == "__main__":
    print("🚀 Starting ticket fetch process...")
    all_tickets = fetch_all_tickets()
    if all_tickets:
        chosen = choose_ticket(all_tickets)
        if chosen:
            print(f"\n✅ You selected:\n🆔 Ticket: {chosen['key']}\n📝 Summary: {chosen['summary']}\n📄 Description:\n{chosen['description']}")
        else:
            print("❌ No ticket selected.")
    else:
        print("❌ No tickets to choose from.")
