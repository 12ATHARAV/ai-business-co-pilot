from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

def search_tool(query: str):
    return search.run(query)