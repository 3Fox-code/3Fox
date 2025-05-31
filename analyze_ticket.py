import openai  # or use anthropic / local LLMs
import json
import os

# Load OpenAI key (you can also store it in .env)
openai.api_key = os.getenv("OPENAI_API_KEY")

if description:
    system_prompt = "You are a senior developer helping extract implementation details from Jira tickets."
    user_prompt = f"""
    Jira Ticket:
    Summary: {summary}
    Description: {description}

    Please extract:
    1. Code Requirements (what code needs to be written)
    2. Acceptance Criteria (how we know it works)

    Respond in this JSON format:
    {{
      "code_requirements": [...],
      "acceptance_criteria": [...]
    }}
    """

    chat_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    response_text = chat_response['choices'][0]['message']['content']

    try:
        result = json.loads(response_text)
        print("\nCode Requirements:")
        for item in result["code_requirements"]:
            print(f"✅ {item}")
        print("\nAcceptance Criteria:")
        for item in result["acceptance_criteria"]:
            print(f"🎯 {item}")
    except json.JSONDecodeError:
        print("⚠️ GPT response could not be parsed as JSON. Here’s what it returned:")
        print(response_text)
