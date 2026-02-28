import json
import os

from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')

client = OpenAI()

def getWeather(place: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={place},IN&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return  response.json()
    else:
        return "❌ Error fetching weather data"
    

def getConversionRate(payload):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{str(payload['from_currency'])}"
    response = requests.get(url)
    data = response.json()
    if data["result"] == "success":
        rate = data["conversion_rates"][str(payload['to_currency'])]
        converted_amount = int(payload['amount']) * rate
        return converted_amount
    else:
        print("❌ Error fetching exchange rate")


def getSystemCmdOutput(cmd):
    return os.system(cmd)
    

AVAILABLE_TOOLS_MAP = {
    "getWeather": getWeather,
    "getConversionRate": getConversionRate,
    "getSystemCmdOutput": getSystemCmdOutput
}

SYSTEM_PROMPT = '''
    You are a helpful AI expert who solves user queries step by step using strict reasoning and structured thinking.

    You must follow these fixed stages in every conversation:
    Analyse → Plan → Action → Observe → Result methodology for every task.

    Description of Each Step:
    1. Analyse - Analyze and interpret the user's query.
    2. Plan - Decide which available tool(s) should be used.
    3. Action - Call only one tool with relevant input.
    4. Observe - Wait for the output (observation) from the tool call.
    5. Result - Generate a final answer for the user based on observations.

    Rules
   - Never skip any step — You must go through each stage one by one in order.
   - Only one function call per `Action` step.
   - Never call a function before reaching the `Action` step.
   - You can only proceed to `analyze` after an actual output is observed.
   - You must handle unknown or unclear queries by stating you're unable to solve them with the available tools.
   - Do not answer the final user query until the `Result` step.
   - You must follow the output json format.

   Output JSON format:
   {
       "step": "string",
       "content": "string",
       "tool": "The name of the tool if step is Action",
       "input": "The input parameter for the tool",
       "output": "The final result if step is Result"
   }

   Available Tools:
   - "getWeather": Accepts the place name as input and return the current weather of that location
   - "getConversionRate": Accept {amount, from_currency, to_currency} as an input and returns the conversion result as output
   - "getSystemCmdOutput": Accept linux command as input and runs the command

   Example:
   User: What is the weather of Delhi?
   Output: {"step": "Analyse", "content": "The user is interesetd in weather data of Delhi" }
   Output: {"step": "Plan", "content": "From the available tools I need to call the getWeather" }
   Output: {"step": "Action", "tool": "getWeather", "input": "Delhi" }
   Output: {"step": "Observe", "content": "32 degree celecious" }
   Output: {"step": "Result", "output": "Delhi weather is 32 C" }
'''

messages = [
    { "role": "system", "content": SYSTEM_PROMPT },
]


while True:
    user_input = input('👨: ')

    if user_input.strip().lower() == 'exit':
        break

    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )
        content = json.loads(response.choices[0].message.content)
        step = content.get('step')

        # log and record analysis/planning/observations
        if step in ('Analyse', 'Plan', 'Observe'):
            print(f"⏭️ : {step}: {content.get('content')}")
            messages.append({"role": "assistant", "content": json.dumps(content)})
            continue

        if step == 'Action':
            tool_name = content.get('tool')
            tool_input = content.get('input')
            print(f"⚙️ : {tool_name}: {tool_input}")

            # parse tool input if it is a JSON string
            if isinstance(tool_input, str):
                try:
                    tool_input_parsed = json.loads(tool_input)
                except Exception:
                    tool_input_parsed = tool_input
            else:
                tool_input_parsed = tool_input

            if tool_name in AVAILABLE_TOOLS_MAP:
                tool_resp = AVAILABLE_TOOLS_MAP[tool_name](tool_input_parsed)
            else:
                tool_resp = f"Unknown tool '{tool_name}'"

            messages.append({
                "role": "assistant",
                "content": json.dumps({"step": "Observe", "content": tool_resp})
            })
            print(f"⏭️ : Observe: {tool_resp}")
            continue

        if step == 'Result':
            print(f"🤖: {step}: {content.get('output')}")
            break

        # unexpected response structure
        print(f"⚠️ Unrecognized response: {content}")
        messages.append({"role": "assistant", "content": json.dumps(content)})
        continue