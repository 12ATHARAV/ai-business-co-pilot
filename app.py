import streamlit as 
from graph.workflow import graph
from database.db import save_run, get_history, get_run_by_id
import time
import threading

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Business Co-Pilot",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center;'>🚀 AI Business Co-Pilot</h1>
<p style='text-align: center;'>Chat with AI to build your business using agentic workflows</p>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📜 History")

    # New Chat Button
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    history = get_history()

    if len(history) == 0:
        st.write("No history yet")

    for item in history[:10]:
        run_id = item[0]
        title = item[1][:40] + "..."

        if st.button(title, key=f"history_{run_id}"):

            data = get_run_by_id(run_id)

            st.session_state.messages = [
                {"role": "user", "content": data[1]},
                {
                    "role": "assistant",
                    "content": f"""
                ### 📌 Business Plan
                {data[2]}

                ---

                ### 📊 Execution
                {data[3]}

                ---

                ### 🧪 Critique
                {data[4]}
                """
                }
            ]

            st.rerun()

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("💡 Ask: Start a dropshipping store for fitness products")

# ---------------- HANDLE INPUT ----------------
if user_input:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # DEFINE STATE FIRST 
    initial_state = {
        "user_input": user_input,
        "plan": "",
        "execution": "",
        "critique": "",
        "approved": False,
        "iteration": 0
    }

    # ---------------- ANIMATION ----------------
    status = st.empty()

    result_container = {"result": None}

    def run_graph():
        result_container["result"] = graph.invoke(initial_state)

    # Start background thread
    thread = threading.Thread(target=run_graph)
    thread.start()

    # Animation loop (runs until graph finishes)
    messages = [
        "🧠 Planner Agent working...",
        "📊 Executor Agent running...",
        "🧪 Critic Agent analyzing...",
        "🚀 Optimizing strategy...",
        "📦 Preparing execution plan..."
    ]

    i = 0

    while thread.is_alive():
        status.markdown(messages[i % len(messages)] + "." * (i % 4))
        time.sleep(0.5)
        i += 1

    thread.join()

    status.empty()

    # GET RESULT (ONLY ONCE)
    result = result_container["result"]

    # ---------------- FORMAT RESPONSE ----------------
    ai_response = f"""
    ### 📌 Business Plan
    {result['plan']}

    ---

    ### 📊 Execution
    {result['execution']}

    ---

    ### 🧪 Critique
    {result['critique']}
    """

    # ---------------- DISPLAY RESPONSE ----------------
    with st.chat_message("assistant"):

        with st.expander("📌 Business Plan", expanded=True):
            st.markdown(result["plan"])

        with st.expander("📊 Execution"):
            st.markdown(result["execution"])

        with st.expander("🧪 Critique"):
            st.markdown(result["critique"])

        # Download Button
        full_report = f"""
        BUSINESS PLAN

        {result['plan']}

        ---------------------

        EXECUTION

        {result['execution']}

        ---------------------

        CRITIQUE

        {result['critique']}
        """

        st.download_button(
            "📥 Download Full Report",
            full_report,
            file_name="ai_business_report.txt",
            key=f"download_{len(st.session_state.messages)}"
        )

    # ---------------- SAVE CHAT ----------------
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    # ---------------- SAVE TO DATABASE ----------------
    save_run(
        user_input,
        result["plan"],
        result["execution"],
        result["critique"]
    )
