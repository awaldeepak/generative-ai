from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
    Act like you are a Javacript AI expert.
    You solve query only on javascript.
    If user asks questions not related to javascript, tell them to ask javascript questions only.
"""

while True:
    user_input = input("👨‍💼")

    if user_input.lower() == 'exit':
        break

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("🤖", response.output_text)