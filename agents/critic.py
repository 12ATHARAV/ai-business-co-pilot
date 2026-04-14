from config.llm import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from memory.memory_manager import store_memory

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     """You are a strict business critic.
     
     IMPORTANT:
        - DO NOT include <think> or internal reasoning
        - DO NOT explain your thinking
        - ONLY return final answer
     """),
    ("human", "Evaluate this:\n{execution}\n\nIs it good? Answer YES or NO and explain.")
])

chain = critic_prompt | llm | StrOutputParser()

def critic_agent(state: dict):
    execution = state.get("execution", "")

    # TOKEN LIMIT FIX
    execution = execution[:2000]

    critique = chain.invoke({
        "execution": execution
    })
    
    critique = critique.split("</think>")[-1]
    
    approved = "yes" in critique.lower()

    return {
        "critique": critique,
        "approved": approved,
        "iteration": state.get("iteration", 0) + 1
    }
