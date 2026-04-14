import re

def parse_plan(plan_text: str):
    steps = []
    
    step_blocks = re.split(r"\n\d+\.", plan_text)
    
    for block in step_blocks:
        if not block.strip():
            continue
        
        lines = block.strip().split("\n")
        
        title = lines[0].strip()
        
        agent = "execution_agent" # default
        
        if "research" in block.lower():
            agent = "research_agent"
            
        steps.append({
            "title": title,
            "content": block,
            "agent": agent
        })
    
    return steps