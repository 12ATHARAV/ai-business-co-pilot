from config.llm import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools.search_tool import search_tool

research_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a market research expert.

        You can use the search tool to get real-world information.

        Steps:
        1. Understand the plan
        2. Perform search queries
        3. Summarize findings

        Rules:
        - DO NOT include <think> or internal reasoning
        - DO NOT explain your thinking
        - ONLY return final answer
    """),
            
    ("human", "Plan:\n{plan}\n\nDo research.")
])

chain = research_prompt | llm | StrOutputParser()

def research_agent(state: dict):
    plan = state.get("plan", "")
    
    #generate search query
    query = f"fitness products trends 2026 dropshipping {plan[:100]}"
    
    search_results = search_tool(query)
    
    # combine plan + search results
    result = chain.invoke({
        "plan": plan + "\n\nSearch Results:\n" + search_results
    })
    
    #remove <think> if present
    result = result.split("</think>")[-1]

    return {
        "research": result
    }