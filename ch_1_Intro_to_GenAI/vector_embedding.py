from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.embeddings.create(
    input="I am Deepak",
    model="text-embedding-3-small"
)

resp = response.data[0].embedding

print(resp)
print(len(resp))