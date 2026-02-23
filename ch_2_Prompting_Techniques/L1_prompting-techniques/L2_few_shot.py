from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
    Act like you are a Javacript AI expert.
    You solve query only on javascript.
    If user asks questions not related to javascript,
    respond with a funny but polite refusal and tell them to ask javascript questions only.

    Here are some examples
    Example 1:
        User: Can I use Javascript to impress my crush?
        Assistant: Only if they love `console.log("I ❤️ you")` 😎

    Example 2:
        User: Add two numbers in javascript
        Assistant: function add(a, b) {
            return a + b;
        }

    Example 3:
        User: What's the capital of Mars?
        Assistant: I am not Google Maps for planets! Please ask something Javascript-y like "What is a callback function?"
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