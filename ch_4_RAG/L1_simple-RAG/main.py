from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ch_4_RAG.system_prompt import get_system_prompt


load_dotenv()
client = OpenAI()

def readPDF():
    pdf = PdfReader("OOPS_Concepts.pdf")
    no_of_pages = len(pdf.pages)
    output = []
    for page_no in range(no_of_pages):
        output.append({
            "page_no": page_no,
            "page_content": pdf.pages[page_no].extract_text()
        })
    return output


# pass the actual function so the prompt builder can invoke it
SYSTEM_PROMPT = get_system_prompt(readPDF)

messages = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_input = input('👨: ')
    if user_input.strip().lower() == 'exit':
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    print("🤖:", response.choices[0].message.content)