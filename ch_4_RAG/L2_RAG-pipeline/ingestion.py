from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# 1. Ingestion
#     a. PDF Load
file_path = "Python_Guide.pdf"
loader = PyPDFLoader(file_path)
docs = loader.load()

#     b. Chunking
text_splitted = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=500
)
splitted_docs = text_splitted.split_documents(docs)

#     c. Vector Embedding
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

#     d. Store in Vector DB (Qdrant DB) - convert "splitted_docs" to vector embedding using "embedding_model" model
doc_store = QdrantVectorStore.from_documents(
    url="http://localhost:6333",
    collection_name="gen-ai",
    embedding=embedding_model,
    documents=splitted_docs
)
print('Ingestion is completed')
