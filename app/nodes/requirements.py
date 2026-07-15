from app.llm import llm
from app.state import SDLCState


def generate_user_stories(state: SDLCState):
    """
    Converts the user's software requirements
    into Agile user stories.
    """

    prompt = f"""
You are an experienced Business Analyst working on a software project.

Convert the following software requirements into clear Agile user stories.

SOFTWARE REQUIREMENTS:
{state["requirements"]}

For every user story, use this format:

USER STORY <number>

Title:
A short title

Story:
As a <type of user>,
I want <some feature>,
so that <some benefit>.

Acceptance Criteria:
- Criterion 1
- Criterion 2
- Criterion 3

IMPORTANT RULES:

1. Cover every important requirement given by the user.
2. Do not ignore any requested feature.
3. Do not invent unnecessary features.
4. Make the acceptance criteria clear and testable.
5. Generate enough user stories to fully represent the requirements.

Return only the complete user stories.
"""

    response = llm.invoke(prompt)

    return {
        "user_stories": response.content,
        "current_stage": "user_stories_generated"
    }


# =========================================================
# NODE 2: PRODUCT OWNER REVIEW
# =========================================================

def product_owner_review(state: SDLCState):
    """
    Reviews the generated user stories against
    the ORIGINAL user requirements.
    """

    attempts = state.get(
        "product_owner_attempts",
        0
    ) + 1

    prompt = f"""
You are a strict and experienced Product Owner.

Your job is to review the generated Agile user stories
and determine whether they completely satisfy the
ORIGINAL SOFTWARE REQUIREMENTS.

ORIGINAL SOFTWARE REQUIREMENTS:
{state["requirements"]}

GENERATED USER STORIES:
{state["user_stories"]}

Review the stories carefully.

Check whether:

1. Every requirement is represented by at least one user story.
2. No important feature from the original requirements is missing.
3. Every user story is clear and understandable.
4. The acceptance criteria are sufficient and testable.
5. The stories correctly represent the user's requested system.
6. The stories do not contradict the original requirements.

If the user stories fully satisfy the requirements,
return exactly:

STATUS: APPROVED

FEEDBACK:
The user stories sufficiently cover the original requirements.

If something is missing or insufficient,
return exactly:

STATUS: FEEDBACK

FEEDBACK:
Clearly explain:
- What requirement is missing
- Which user story is insufficient
- What must be added or changed

Do not approve incomplete user stories.
"""

    response = llm.invoke(prompt)

    review = response.content

    # Determine the routing status
    if "STATUS: APPROVED" in review.upper():
        status = "APPROVED"
    else:
        status = "FEEDBACK"

    return {
        "product_owner_review": review,
        "product_owner_status": status,
        "product_owner_attempts": attempts,
        "current_stage": "product_owner_review"
    }


# =========================================================
# NODE 3: REVISE USER STORIES
# =========================================================

def revise_user_stories(state: SDLCState):
    """
    Revises the user stories according to the
    Product Owner's feedback.
    """

    prompt = f"""
You are an experienced Business Analyst.

The Product Owner has reviewed your user stories
and found problems with them.

Your task is to revise the user stories so that
they fully satisfy both:

1. The original software requirements
2. The Product Owner's feedback

ORIGINAL SOFTWARE REQUIREMENTS:
{state["requirements"]}

CURRENT USER STORIES:
{state["user_stories"]}

PRODUCT OWNER REVIEW:
{state["product_owner_review"]}

IMPORTANT RULES:

1. Fix every issue identified by the Product Owner.
2. Add missing user stories if necessary.
3. Improve existing stories if necessary.
4. Keep all existing stories that are already correct.
5. Return the COMPLETE revised set of user stories,
not only the changed stories.
6. Make sure every original requirement is covered.

Use this format:

USER STORY <number>

Title:
A short title

Story:
As a <type of user>,
I want <feature>,
so that <benefit>.

Acceptance Criteria:
- Criterion 1
- Criterion 2
- Criterion 3

Return only the complete revised user stories.
"""

    response = llm.invoke(prompt)

    return {
        "user_stories": response.content,
        "current_stage": "user_stories_revised"
    }