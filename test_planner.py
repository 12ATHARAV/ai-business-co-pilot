from agents.planner import planner_agent

state = {
    "user_input": "Start a dropshipping store for fitness products"
}

result = planner_agent(state)

print("\nGenerated Plan:\n")
print(result["plan"])