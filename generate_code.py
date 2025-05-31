from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # Load environment variables from .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_code(summary, description):
    prompt = f"""
You are a senior-level Python developer.

Based on the following details, generate a clean, professional Python program:

Title: {summary}

Description:
{description}

Requirements:
- Write complete, well-structured Python code.
- Include appropriate import statements.
- Add inline comments and docstrings to explain key parts.
- Handle edge cases and potential errors where applicable.
- Use proper function and variable naming conventions.
- Make the code executable (do not leave it partial or pseudocode).
- If it involves user input or file I/O, simulate inputs where needed.
- Enter proper API keys , don't keep it for the user 
- No need to write '''python in starting and ''' in the ending 
- use API from env 
- Make sure your code loads the env variable correctly

Output only the code (do not add explanations or headings).
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert Python developer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def save_code_to_file(ticket_key, code):
    filename = ticket_key.lower().replace("-", "_") + ".py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Code saved to {filename}")
    return filename
