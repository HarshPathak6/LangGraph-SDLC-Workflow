from app.state import SDLCState
from app.llm import llm
from app.mem0_client import save_memory

def deployment(state: SDLCState):

    print("===== ENTERED deployment =====")

    prompt = f"""
You are a DevOps engineer.

The backend code has passed all reviews.

Generate a short and concise deployment guide.

Include:

- Environment variables
- Install commands
- Run command

Return plain text only.

Code:

{state["generated_code"]}
"""

    print("Calling Deployment LLM...")

    response = llm.invoke(prompt)

    print("Deployment completed")

    save_memory(
        state["project_id"],
        f"""
    User requirements:
    {state["requirements"]}

    Generated design:
    {state["design_docs"]}

    Important coding style:
    {state["generated_code"][:1000]}
    """
    )
    
    return {

        "deployment_result": response.content,

        "current_stage": "deployment"
    }