from graph.workflow import graph

initial_state = {
    "user_input": "Start a dropshipping store for fitness products",
    "plan": "",
    "execution": "",
    "critique": "",
    "approved": False,
    "iteration": 0
}

result = graph.invoke(initial_state)

print("\n" + "="*50)
print("🧠 BUSINESS OUTPUT")
print("="*50)

print("\n📌 PLAN:\n")
print(result["plan"])

print("\n📊 EXECUTION:\n")
print(result["execution"])

print("\n🧪 CRITIQUE:\n")
print(result["critique"])