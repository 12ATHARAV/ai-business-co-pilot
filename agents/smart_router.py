from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.llm import llm


router_prompt = ChatPromptTemplate.from_messages([
    ("system",
    """You are an AI router.

    Decide best agent based on TASK:

    - research_agent → market research, trends, analysis
    - execution_agent → building store, setup, implementation
    - marketing_agent → ads, promotion, scaling

    Be accurate.

    Return ONLY:
    research_agent OR execution_agent OR marketing_agent
    """
    ),
    ("human", "Task:\n{task}")
])


router_chain = router_prompt | llm | StrOutputParser()


# def decide_agent(task: str):
#     decision = router_chain.invoke({"task": task}).strip().lower()

#     # safety fallback
#     if "research" in decision:
#         return "research_agent"
#     elif "marketing" in decision:
#         return "marketing_agent"
#     else:
#         return "execution_agent"

def decide_agent(task: str):

    # Rule-based override (FAST + RELIABLE)
    task_lower = task.lower()

    if "build" in task_lower or "setup" in task_lower or "store" in task_lower:
        return "execution_agent"

    if "marketing" in task_lower or "ads" in task_lower:
        return "marketing_agent"

    if "research" in task_lower or "analysis" in task_lower:
        return "research_agent"

    # LLM decision (fallback)
    decision = router_chain.invoke({"task": task}).strip().lower()

    if "research" in decision:
        return "research_agent"
    elif "marketing" in decision:
        return "marketing_agent"
    else:
        return "execution_agent"