from utils.parser import parse_plan
from agents.router import route_step


def dynamic_executor(state: dict):

    plan = state.get("plan", "")
    steps = parse_plan(plan)

    # 🔥 LIMIT STEPS
    steps = steps[:4]

    results = []

    for step in steps:
        print(f"\n⚡ Executing: {step['title']}")

        # output = route_step(step, state)
        step_state = {
            **state,
            "current_step": step["content"]   # KEY
        }

        output = route_step(step, step_state)

        clean_text = (
            output.get("research") or 
            output.get("execution") or 
            ""
        )

        results.append(f"### {step['title']}\n{clean_text}")

    return {
        "execution": "\n\n".join(results)
    }