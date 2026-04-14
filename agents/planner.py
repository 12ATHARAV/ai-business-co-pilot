from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.llm import llm
from memory.memory_manager import retrieve_memory

# Prompt Template
planner_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are an expert business planner AI.

        Break the goal into MAXIMUM 4 steps.

        Rules:
        - Each step must be concise (2–3 lines)
        - No repetition
        - DO NOT include <think> or internal reasoning
        - Clear actionable steps
    """
    ),
    ("human", "{input}")
])



# Chain (modern LCEL style)
planner_chain = planner_prompt | llm | StrOutputParser()



import re

def clean_output(text: str):
    # remove <think>...</think>
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def planner_agent(state: dict):
    """
    Planner Agent:
    - Reads user input
    - Generates plan
    - Updates state
    """

    user_input = state["user_input"]
    
    #retrieve memory
    memory = retrieve_memory(user_input)[:500]  # LIMIT MEMORY

    plan = planner_chain.invoke({
        "input": f"{user_input}\n\nPast Knowledge:\n{memory}"
    })

    plan = clean_output(plan)  # clean it

    return {
        "plan": plan
    }