import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_code(summary, description):
    prompt = f"""
Title: {summary}
Description:
{description}

Please generate code for the above requirements...
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert React developer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
