from urllib import response

from click import prompt

from app import state
from app.state import SDLCState
from app.llm import llm


def generate_code(state: SDLCState):

    print("===== ENTERED generate_code =====")
    """
    Generates the initial project code using the approved
    technical design document.
    """

    prompt = f"""
You are a Senior Backend Software Engineer.

Based on the approved project requirements, user stories, and design document, generate the backend implementation.

PROJECT REQUIREMENTS:
{state["requirements"]}

APPROVED USER STORIES:
{state["user_stories"]}

APPROVED DESIGN DOCUMENT:
{state["design_docs"]}

Generate all the necessary backend files, including (where applicable):
- main.py
- models.py
- schemas.py
- crud.py
- database.py

Requirements:
- Use FastAPI.
- Use SQLAlchemy ORM.
- Use Pydantic models.
- Follow clean architecture and clean coding practices.
- Include proper validation and error handling.
- Generate only the source code.
- Do not explain the code.
- Do not use Markdown or code fences.
- Keep the implementation minimal. (IMPORTANT)
"""

    print("Calling LLM...")
    # Send the prompt to the LLM
    response = llm.invoke(prompt)
    print("LLM returned")
    print("Generated code length:", len(response.content))
    print(response.content[:500])
    # response is the full AI message object.
    # response.content contains only the generated text.
    print(type(response))
    print(response)

    return {
    "generated_code": response.content,
    "current_stage": "code_generated"
}

#------------------------------------------
#CODE REVIEW
#------------------------------------------


def code_review(state: SDLCState):

    print("===== ENTERED code_review =====")
    print("Generated code exists:", "generated_code" in state)
    print("Generated code length:", len(state.get("generated_code", "")))
    print(state.get("generated_code", "")[:300])
    prompt = f"""
Review the following backend code.

{state['generated_code']}

Return only:

STATUS: APPROVED

or

STATUS: FEEDBACK

FEEDBACK:
...
"""

    print("Calling Code Review LLM...")

    attempts = state.get("code_review_attempts", 0) + 1

    # Auto-approve after 3 failed review attempts
    if attempts >= 3:
        print("Maximum review attempts reached. Auto-approving.")

        return {
            "code_review": "Auto-approved after maximum attempts.",
            "code_review_status": "APPROVED",
            "code_review_attempts": attempts,
            "current_stage": "code_review"
        }

    # Run the LLM ONLY if we're still below the limit
    response = llm.invoke(prompt)

    print("\n========== RAW LLM RESPONSE ==========")
    print(response.content)
    print("======================================\n")

    review = response.content

    # Determine status
    if "STATUS: APPROVED" in review.upper():
        status = "APPROVED"
        feedback = ""
    else:
        status = "FEEDBACK"

        if "FEEDBACK:" in review.upper():
            feedback = review.split("FEEDBACK:", 1)[1].strip()
        else:
            feedback = review

    print("==============================")
    print("Review Attempt:", attempts)
    print("Status:", status)
    print("==============================")

    return {
        "code_review": feedback,
        "code_review_status": status,
        "code_review_attempts": attempts,
        "current_stage": "code_review"
    }

def fix_code_after_review(state: SDLCState):

    print("===== ENTERED fix_code_after_review =====")

    prompt = f"""
You are a Senior Backend Developer.

The previous code has been reviewed.

Original Requirements

{state["requirements"]}

Design Document

{state["design_docs"]}

Current Code

{state["generated_code"]}

Reviewer Feedback

{state["code_review_feedback"]}

Modify the existing code according to the review feedback.

Return ONLY the updated source code.

Do not explain anything.
"""

    print("Calling Fix Code LLM...")

    response = llm.invoke(prompt)

    print("Fix completed")

    return {

        "generated_code":response.content,

        "current_stage":"code_fixed_after_review"

    }