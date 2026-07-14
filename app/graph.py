from langgraph.graph import StateGraph, START, END

from app.state import SDLCState
from app.llm import llm

def call_llm(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content

# =========================================================
# REQUIREMENTS PHASE
# =========================================================

def generate_user_stories(state: SDLCState):

    prompt = f"""
You are a Business Analyst.

Convert the following software requirements into detailed Agile user stories.

For every user story include:
- Title
- As a...
- I want...
- So that...
- Acceptance Criteria

Requirements:
{state["requirements"]}
"""
    
    result = call_llm(prompt)

    return {
        "user_stories": result,
        "current_stage": "product_owner_review"
    }

def product_owner_review(state: SDLCState):

    prompt = f"""
You are a strict Product Owner.

Review these user stories against the original requirements.

ORIGINAL REQUIREMENTS:
{state["requirements"]}

USER STORIES:
{state["user_stories"]}

Return your answer in exactly this format:

STATUS: APPROVED

FEEDBACK:
Your feedback here

OR:

STATUS: FEEDBACK

FEEDBACK:
Explain exactly what must be improved.
"""
    
    result = call_llm(prompt)

    status = (
        "APPROVED"
        if "STATUS: APPROVED" in result.upper()
        else "FEEDBACK"
    )

    return {
        "product_owner_review: result,"
        "product_owner_status": status
    }

def revise_user_stories(state: SDLCState):

    prompt = f"""
You are a Business Analyst.

Revise the user stories according to the Product Owner feedback.

ORIGINAL REQUIREMENTS:
{state["requirements"]}

CURRENT USER STORIES:
{state["user_stories"]}

PRODUCT OWNER FEEDBACK:
{state["product_owner_review"]}

Return the complete revised user stories.
"""
    

    return {
        "user_stories": call_llm(prompt)
    }

# =========================================================
# DESIGN PHASE
# =========================================================
