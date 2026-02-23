from dotenv import load_dotenv
from openai import OpenAI
from collections import Counter

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
    Give me one word answer
"""

user_input = input("👨‍💼")

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": user_input
    },
]

answers = []

def gen_ai(model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=2
    )
    return response.choices[0].message.content

def find_frequency():
    counter = Counter(answers)
    print("🤖 (Final Answer)", counter.most_common(1)[0])

for i in range(5):
    model = "gpt-4.1-mini"
    resp = gen_ai(model)
    print(f"🤖 : {model} - {i+1}", resp)
    answers.append(resp)

for i in range(5):
    model = "gpt-4.1"
    resp = gen_ai(model)
    print(f"🤖 : {model} - {i+1}", resp)
    answers.append(resp)

find_frequency()