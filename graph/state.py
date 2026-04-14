from typing import TypedDict, List

class AgentState(TypedDict):
    user_input: str
    plan: str
    research: str
    execution: str
    critique: str
    approved: bool