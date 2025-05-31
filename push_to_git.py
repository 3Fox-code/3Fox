from fetch_ticket import fetch_all_tickets, choose_ticket
from generate_code import generate_code, save_code_to_file
from update_jira_status import mark_ticket_done, get_transitions

# Step 1: Fetch available Jira tickets
tickets = fetch_all_tickets()

if tickets:
    selected_ticket = choose_ticket(tickets)
    if selected_ticket:
        key = selected_ticket["key"]
        summary = selected_ticket["summary"]
        description = selected_ticket["description"]

        # Step 2: Generate Python code for the selected ticket
        code = generate_code(summary, description)
        print("🧠 Generated code:\n", code)

        # Step 3: Save to .py file
        filename = save_code_to_file(key, code)

        # Step 4: Mark ticket as Done in Jira
        transitions = get_transitions(key)
        done_transition = next((t for t in transitions if t["name"].lower() == "done"), None)

        if done_transition:
            mark_ticket_done(key, done_transition["id"])
        else:
            print("⚠️ 'Done' transition not available for this ticket.")

    else:
        print("❌ No ticket selected.")
else:
    print("⚠️ No tickets found.")
