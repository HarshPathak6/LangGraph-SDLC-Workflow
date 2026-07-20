from app.state import SDLCState
from app.llm import llm


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

    return {

        "deployment_result": response.content,

        "current_stage": "deployment"
    }