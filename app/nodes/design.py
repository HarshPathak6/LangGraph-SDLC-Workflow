from app.llm import llm
from app.state import SDLCState


def create_design_docs(state: SDLCState):
    print("Entered create_design_docs")

    """
    Creates technical design documentation
    from approved user stories.
    """

    prompt = f"""
You are a Software Architect.

Create a practical technical design for this software project.

REQUIREMENTS:
{state["requirements"]}

APPROVED USER STORIES:
{state["user_stories"]}

Include these sections:

1. Project Overview
2. Architecture
3. Main Components
4. Technology Stack
5. Database Entities
6. Important API Endpoints
7. Authentication and Authorization
8. Basic Data Flow
9. Security Considerations

IMPORTANT: KEEP THE RESPONSE CONCISE AND UNDER 400 WORDS.
RULES:
- Keep the design concise but technically useful.
- Prefer a modular monolith for a normal-sized project.
- Do not add unnecessary microservices or enterprise infrastructure.
- Do not include deployment details yet.
- Do not repeat all the user stories.
- Keep each section focused.
"""
    print("Calling Design LLM...")
    response = llm.invoke(prompt)
    print("Design LLM returned")

    return {
        "design_docs": response.content,
        "current_stage": "design_docs_created"
    }


def review_design(state: SDLCState):

    current_attempts = state.get("design_review_attempts", 0)

    prompt = f"""
    You are a Senior Software Architect reviewing a technical design document.

    ORIGINAL REQUIREMENTS:
    {state["requirements"]}

    APPROVED USER STORIES:
    {state["user_stories"]}

    DESIGN DOCUMENT:
    {state["design_docs"]}

    Review whether the design is sufficient to implement the approved
    requirements and user stories.

    Check:
    1. Architecture
    2. Main components
    3. Database design
    4. API design
    5. Authentication and authorization
    6. Security
    7. Practical implementation

    Do not reject for minor formatting issues.

    Return EXACTLY:

    STATUS: APPROVED
    FEEDBACK: Brief reason

    OR:

    STATUS: NEEDS_REVISION
    FEEDBACK: Briefly explain the important changes required.
    """

    response = llm.invoke(prompt)

    if "NEEDS_REVISION" in response.content.upper():
        status = "NEEDS_REVISION"
    else:
        status = "APPROVED"

    return {
        "design_review_status": status,
        "design_review_feedback": response.content,
        "design_review_attempts": current_attempts + 1,
        "current_stage": "design_reviewed"
    }


def revise_design_docs(state: SDLCState):

    prompt = f"""
    You are a Senior Software Architect.

    Revise the current technical design document according to the
    Design Review feedback.

    ORIGINAL REQUIREMENTS:
    {state["requirements"]}

    APPROVED USER STORIES:
    {state["user_stories"]}

    CURRENT DESIGN DOCUMENT:
    {state["design_docs"]}

    DESIGN REVIEW FEEDBACK:
    {state["design_review_feedback"]}

    INSTRUCTIONS:
    - Fix the important issues identified by the reviewer.
    - Preserve correct parts of the existing design.
    - Do not add unnecessary complexity.
    - Keep the design practical.
    - Return the complete revised design document.
    """

    response = llm.invoke(prompt)

    return {
        "design_docs": response.content,
        "current_stage": "design_docs_revised"
    }