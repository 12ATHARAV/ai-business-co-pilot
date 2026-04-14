from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# ollama pull llama3
embedding = OllamaEmbeddings(model="llama3")

# ollama pull nomic-embed-text
# nomic-embed-text is optimized for similarity search
# embedding = OllamaEmbeddings(model="nomic-embed-text")

vector_db = Chroma(
    collection_name="business_memory",
    embedding_function=embedding,
    persist_directory="./chroma_db"
)