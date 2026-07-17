from app.state import SDLCState
from app.llm import llm


def generate_code(state: SDLCState):

    print("===== ENTERED generate_code =====")
    """
    Generates the initial project code using the approved
    technical design document.
    """

    prompt = f"""
You are a senior backend developer.
Based on the following Software Design Document, generate clean and production ready backend code

ORIGINAL REQUIREMENTS:
{state["requirements"]}

APPROVED USER STORIES:
{state["user_stories"]}

APPROVED DESIGN DOCUMENT:
{state["design_docs"]}

Your task is to generate the core implementation files needed
to build this project.

VERY IMPORTANT: KEEP THE RESPONSE CONCISE AND NOT UNNECESSARILY LONG.
Requirements:
    - Use the required language to generate code
    - Use FastAPI for endpoints
    - Follow clean coding practice
    - Add meaningfull comments
    - Organize the code logically
    
    Rules:
    - Generate only the Source Code.
    - Do not use Markdown.
    - No need to explain the code.
    - Keep the response concise.
"""

    print("Calling LLM...")
    # Send the prompt to the LLM
    response = llm.invoke(prompt)
    print("LLM returned")
    # response is the full AI message object.
    # response.content contains only the generated text.
    return {
        "generated_code": response.content,
        "current_stage": "code_generated"
    }

    