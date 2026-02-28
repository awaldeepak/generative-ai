from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ch_4_RAG.system_prompt import get_system_prompt

load_dotenv()
client = OpenAI()

while True:
    # 2. Retrival 
        # a. User Input
    user_input = input('👨>>')
    if user_input.strip().lower() == 'exit':
        break

        # b. Vector Embedding
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

        # c. Retrive from Vector DB
    vector_db = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="gen-ai",
        embedding=embedding_model,
    )

    chunks = vector_db.similarity_search(
        query=user_input
    )

    def get_content():
        output = []
        no_of_chunks = len(chunks)
        for chunk_no in range(no_of_chunks):
            output.append({
                "page_no": chunks[chunk_no].metadata['page_label'],
                "page_content": chunks[chunk_no].page_content
            })
        return output


    # 3. Generate
    # pass the actual function so the prompt builder can invoke it
    SYSTEM_PROMPT = get_system_prompt(get_content)

        # a. User input and retrived chunks put in LLM
    messages = [
        { "role": "system", "content": SYSTEM_PROMPT },
        {"role": "user", "content": user_input}
    ]
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

        # b. Generate output
    print("🤖:", response.choices[0].message.content)
