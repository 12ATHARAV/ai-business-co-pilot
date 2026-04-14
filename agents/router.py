# from agents.researcher import research_agent
# from agents.executor import execution_agent

# def route_step(step, state):
#     if step["agent"] == "research_agent":
#         return research_agent(state)
    
#     elif step["agent"] == "execution_agent":
#         return execution_agent(state)
    
#     return {}

from agents.researcher import research_agent
from agents.executor import execution_agent
from agents.smart_router import decide_agent


def route_step(step, state):
    task_text = step["content"]
    agent_type = decide_agent(task_text)

    print(f"🤖 LLM selected: {agent_type}")

    if agent_type == "research_agent":
        return research_agent(state)

    elif agent_type == "execution_agent":
        return execution_agent(state)

    # fallback
    return execution_agent(state)