from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
    Act like you are an expert AI agent that solves user problems step by step using strict reasoning.
    
    Follow these 5 steps, one at a time:
    1. ANALYSIS - Understand the user's question and intent.
    2. THINK - Think through the problem carefully and logically.
    3. SUGGEST - Suggest a possible answer or solution approach.
    4. VERIFY - Re-check and verify your reasoning.
    5. RESULT - Give the final answer clearly.

    Rule:
    - DO NOT skip any steps.
    - DO NOT output multiple steps at once.
    - Wait for user to provide the next input before continuing.

    Output:
    - Output only one step per response.
    - Always use JSON format:
        { "step": "string", "content": "string" }

    Example 1:
    Input: What is 15 * 3?

    Output: { "step": "ANALYSIS", "content": "The user is asking a multiplication problem. Let's get those math muscles working!" }
    Output: { "step": "THINK", "content": "Multiply 15 with 3. That means adding 15 three times or 3 fifteen times." }
    Output: { "step": "SUGGEST", "content": "Suggested output is 30" }
    Output: { "step": "VERIFY", "content": "Double-checked: 15 times 3 is 45. which is incorrectly re-evaluated in Step SUGGEST" }
    Output: { "step": "SUGGEST", "content": "Suggested output is 45" }
    Output: { "step": "VERIFY", "content": "Double-checked: 15 times 3 is 45." }
    Output: { "step": "RESULT", "content": "Final result is 15 * 3 = 45" }
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

while True:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    # Robustly parse the assistant's JSON response. Sometimes the model
    # may return JSON encoded as a string (double-encoded), so keep
    # decoding until we get a dict or fail.
    content = response.choices[0].message.content
    try:
        resp = json.loads(content)
        # If it's still a string, decode again (handles double-encoded JSON)
        while isinstance(resp, str):
            resp = json.loads(resp)
    except Exception:
        print("Failed to parse assistant response as JSON:\n", content)
        raise

    if resp["step"] == "RESULT":
        print("🤖", resp["step"] + " : " + resp["content"])
        break

    # Append the assistant reply as a single JSON string (no double-encoding)
    messages.append({
        "role": "assistant",
        "content": json.dumps(resp)
    })

    print("🤖", resp["step"] + " : " + resp["content"])