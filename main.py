from fetch_ticket import fetch_ticket
from generate_code import generate_code

ticket = fetch_ticket()
if ticket:
    summary, description = ticket["summary"], ticket["description"]
    code = generate_code(summary, description)
    print("Generated code:\n", code)
else:
    print("No tickets found.")
