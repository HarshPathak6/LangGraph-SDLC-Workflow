from app.llm import llm
from app.state import SDLCState


def create_design_docs(state: SDLCState):
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

RULES:
- Keep the design concise but technically useful.
- Prefer a modular monolith for a normal-sized project.
- Do not add unnecessary microservices or enterprise infrastructure.
- Do not include deployment details yet.
- Do not repeat all the user stories.
- Keep each section focused.
"""

    response = llm.invoke(prompt)

    return {
        "design_docs": response.content,
        "current_stage": "design_docs_created"
    }