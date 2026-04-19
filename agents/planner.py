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
    - Generates/re-generates plan (with critic feedback if available)
    - Updates state
    """

    user_input = state["user_input"]
    critique = state.get("critique", "")
    iteration = state.get("iteration", 0)

    # retrieve memory
    memory = retrieve_memory(user_input)[:500]  # LIMIT MEMORY

    # Build input — include critic feedback on re-plan attempts
    if critique and iteration > 0:
        prompt_input = (
            f"{user_input}\n\n"
            f"Past Knowledge:\n{memory}\n\n"
            f"⚠️ Previous plan was rejected by the critic. Critic feedback:\n{critique}\n\n"
            f"Please create an improved plan addressing the issues above."
        )
    else:
        prompt_input = f"{user_input}\n\nPast Knowledge:\n{memory}"

    plan = planner_chain.invoke({"input": prompt_input})
    plan = clean_output(plan)  # clean it

    return {
        "plan": plan
    }