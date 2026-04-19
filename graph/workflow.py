from langgraph.graph import StateGraph, END
from graph.state import AgentState
from agents.dynamic_executor import dynamic_executor

from agents.planner import planner_agent
from agents.researcher import research_agent
from agents.executor import execution_agent
from agents.critic import critic_agent

# # create graph
# builder = StateGraph(AgentState)

# # Add nodes
# builder.add_node("planner", planner_agent)
# builder.add_node("research", research_agent)
# builder.add_node("execution", execution_agent)
# builder.add_node("critic", critic_agent)

# # define flow
# builder.set_entry_point("planner")

# builder.add_edge("planner","research")
# builder.add_edge("research", "execution")
# builder.add_edge("execution", "critic")

# # conditional loop
# def decision(state):
#     return "end" if state["approved"] else "planner"

# builder.add_conditional_edges(
#     "critic",
#     decision,
#     {
#         "planner": "planner",
#         "end": END
#     }
# )

# # compile graph
# graph = builder.compile()




# Dynamic workflow

builder = StateGraph(AgentState)

builder.add_node("planner", planner_agent)
builder.add_node("executor", dynamic_executor)
builder.add_node("critic", critic_agent)

builder.set_entry_point("planner")

builder.add_edge("planner", "executor")
builder.add_edge("executor", "critic")

MAX_ITERATIONS = 3

def decision(state):
    """Route back to planner if not approved, else end. Cap at MAX_ITERATIONS."""
    if state.get("approved") or state.get("iteration", 0) >= MAX_ITERATIONS:
        return "end"
    return "planner"

builder.add_conditional_edges(
    "critic",
    decision,
    {
        "planner": "planner",
        "end": END
    }
)

graph = builder.compile()