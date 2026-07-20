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

Generate only:

- main.py
- one SQLAlchemy model
- one CRUD function
- one API endpoint

Keep the total code under 250 lines.

Do not generate comments or explanations.
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
You are a senior software code reviewer.

Review the backend code.

If the code is functional and only has minor issues, respond exactly with:

STATUS: APPROVED

Only return FEEDBACK if there are serious problems that would prevent deployment.

If feedback is needed, respond exactly like:

STATUS: FEEDBACK

FEEDBACK:
- issue 1
- issue 2

Return nothing else.
"""

    print("Calling Code Review LLM...")

    attempts = state.get("code_review_attempts", 0) + 1

    # Auto-approve after 3 failed review attempts
    if attempts >= 3:
        print("Maximum review attempts reached. Auto-approving.")

        return {
        "code_review_feedback": "",
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
        "code_review_feedback": feedback,
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


def security_review(state: SDLCState):

    print("===== ENTERED security_review =====")

    print("Generated code exists:", "generated_code" in state)
    print("Generated code length:", len(state.get("generated_code", "")))

    prompt = f"""
You are a software security reviewer.

Review the backend code.

Current Code:

{state["generated_code"]}

Only reject the code if there are serious security vulnerabilities.

Minor improvements should still be approved.

Return exactly one of these.

STATUS: APPROVED

or

STATUS: FEEDBACK

FEEDBACK:
- issue 1
- issue 2

Return nothing else.
"""

    print("Calling Security Review LLM...")

    attempts = state.get("security_review_attempts", 0) + 1

    # Auto approve after 3 attempts
    if attempts >= 3:

        print("Maximum security review attempts reached. Auto-approving.")

        return {
            "security_review_feedback": "",
            "security_review_status": "APPROVED",
            "security_review_attempts": attempts,
            "current_stage": "security_review"
        }

    response = llm.invoke(prompt)

    print("\n========== RAW SECURITY REVIEW ==========")
    print(response.content)
    print("=========================================\n")

    review = response.content

    review_upper = review.upper()

    if "STATUS: APPROVED" in review_upper:

        status = "APPROVED"
        feedback = ""

    else:

        status = "FEEDBACK"

        idx = review_upper.find("FEEDBACK:")

        if idx != -1:
            feedback = review[idx + len("FEEDBACK:"):].strip()
        else:
            feedback = review

    print("==============================")
    print("Security Review Attempt:", attempts)
    print("Status:", status)
    print("==============================")

    return {
        "security_review_feedback": feedback,
        "security_review_status": status,
        "security_review_attempts": attempts,
        "current_stage": "security_review"
    }


def fix_code_after_security(state: SDLCState):

    print("===== ENTERED fix_code_after_security =====")

    prompt = f"""
You are a Senior Backend Developer.

Update the backend code according to the security review.

Requirements:

{state["requirements"]}

Design Document:

{state["design_docs"]}

Current Code:

{state["generated_code"]}

Security Review Feedback:

{state["security_review_feedback"]}

Return ONLY the updated backend code.

Do not explain anything.
"""

    print("Calling Security Fix LLM...")

    response = llm.invoke(prompt)

    print("Security fixes completed.")

    return {

        "generated_code": response.content,

        "current_stage": "security_fixed"

    }