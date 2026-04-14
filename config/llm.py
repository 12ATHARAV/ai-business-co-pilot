# from langchain_community.chat_models import ChatOllama

# llm = ChatOllama(
#     model="deepseek-v3:671b-cloud",
#     temperature=0.7
# )


from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    # model="llama-3.3-70b-versatile"  
    model = "qwen/qwen3-32b"
    # model = "llama-3.1-8b-instant"
)


# from langchain_ollama import ChatOllama

# llm = ChatOllama(
#     model="gpt-oss:20b",
#     temperature=0.7,
#     # other params...
# )