from fetch_ticket import fetch_all_tickets, choose_ticket
from generate_code import generate_code, save_code_to_file
from update_jira import get_transitions, mark_ticket_done

def main():
    while True:
        tickets = fetch_all_tickets()
        if not tickets:
            print("⚠️ No tickets found or all tickets resolved. Exiting.")
            break

        selected_ticket = choose_ticket(tickets)
        if not selected_ticket:
            print("❌ No ticket selected. Exiting.")
            break

        key = selected_ticket["key"]
        summary = selected_ticket["summary"]
        description = selected_ticket["description"]

        # Generate Python code
        code = generate_code(summary, description)
        print("🧠 Generated code:\n", code)

        # Save to .py file
        filename = save_code_to_file(key, code)

        # Get transitions and mark ticket done
        transitions = get_transitions(key)
        done_transition = next((t for t in transitions if t["name"].lower() == "done"), None)

        if done_transition:
            mark_ticket_done(key, done_transition["id"])
        else:
            print("⚠️ 'Done' transition not available for this ticket.")

        # Ask user if they want to continue resolving tickets
        cont = input("\nDo you want to resolve another ticket? (y/n): ").strip().lower()
        if cont != 'y':
            print("👋 Exiting.")
            break

if __name__ == "__main__":
    main()
