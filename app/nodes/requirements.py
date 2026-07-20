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
    print("Entered product_owner_review")
    """
    Reviews the generated user stories against
    the ORIGINAL user requirements.
    """

    attempts = state.get(
        "product_owner_attempts",
        0
    ) + 1

    # Stop infinite review loops
    if attempts >= 3:
        print("Maximum Product Owner attempts reached. Auto-approving.")
        return {
        "product_owner_review": "Auto-approved after maximum attempts.",
        "product_owner_status": "APPROVED",
        "product_owner_attempts": attempts,
        "current_stage": "product_owner_review"
    }
    prompt = f"""
You are a Product Owner.

Compare these requirements:

{state["requirements"]}

with these user stories:

{state["user_stories"]}

Only reject the user stories if a major feature requested by the user is completely missing.

Ignore:
- wording
- formatting
- writing style
- minor acceptance criteria

If the main functionality requested by the user exists, approve it.

Reply ONLY in one of these formats.

STATUS: APPROVED

FEEDBACK:
Approved.

OR

STATUS: FEEDBACK

FEEDBACK:
One or two sentences explaining the missing feature.
"""
    print("Calling Product Owner LLM")
    response = llm.invoke(prompt)

    print("Product Owner finished")
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

IMPORTANT NOTE: KEEP THE RESPONSE UNDER 300 WORDS.
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
    print(len(prompt))
    print(prompt[:500])
    response = llm.invoke(prompt)

    return {
        "user_stories": response.content,
        "current_stage": "user_stories_revised"
    }