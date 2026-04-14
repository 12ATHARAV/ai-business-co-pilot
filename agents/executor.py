from config.llm import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

execution_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a business execution expert."),
    ("human", "Context:\n{context}\n\nExecute this step.")
])

chain = execution_prompt | llm | StrOutputParser()

# def execution_agent(state: dict):
#     result = chain.invoke({"research": state["research"]})
#     return {"execution": result}

def execution_agent(state: dict):

    context = state.get("current_step", "")

    result = chain.invoke({
        "context": context
    })

    result = result.split("</think>")[-1]

    return {
        "execution": result
    }