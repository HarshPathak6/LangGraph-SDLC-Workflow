# from langgraph.graph import StateGraph, START, END

# from app.state import SDLCState
# from app.llm import llm

# def call_llm(prompt: str) -> str:
#     response = llm.invoke(prompt)
#     return response.content

# =========================================================
# REQUIREMENTS PHASE
# =========================================================

from langgraph.graph import StateGraph, START, END

from app.state import SDLCState

from app.nodes.requirements import (
    generate_user_stories,
    product_owner_review,
    revise_user_stories
)

from app.nodes.design import (
    create_design_docs,
    review_design,
    revise_design_docs
)

from app.nodes.development import generate_code

# =========================================================
# ROUTING FUNCTION
# =========================================================

def route_product_owner_review(state: SDLCState):

    if state["product_owner_status"] == "APPROVED":
        return "approved"

    return "needs_revision"

def route_design_review(state: SDLCState):

    if state.get("design_review_status") == "APPROVED":
        return "approved"

    return "needs_revision"

# =========================================================
# BUILD GRAPH
# =========================================================

def build_graph(checkpointer):

    builder = StateGraph(SDLCState)


# ==========================================================
    # REQUIREMENTS PHASE
    # ==========================================================

    builder.add_node(
        "generate_user_stories",
        generate_user_stories
    )

    builder.add_node(
        "product_owner_review",
        product_owner_review
    )

    builder.add_node(
        "revise_user_stories",
        revise_user_stories
    )

    # ==========================================================
    # DESIGN PHASE
    # ==========================================================

    builder.add_node(
        "create_design_docs",
        create_design_docs
    )

    builder.add_node(
        "design_review",
        review_design
    )

    builder.add_node(
        "revise_design_docs",
        revise_design_docs
    )

    # ==========================================================
    # DEVELOPMENT PHASE
    # ==========================================================

    builder.add_node(
        "generate_code",
        generate_code
    )

    # ==========================================================
    # START
    # ==========================================================

    builder.add_edge(
        START,
        "generate_user_stories"
    )

    # ==========================================================
    # REQUIREMENTS LOOP
    # ==========================================================

    builder.add_edge(
        "generate_user_stories",
        "product_owner_review"
    )

    builder.add_conditional_edges(
        "product_owner_review",
        route_product_owner_review,
        {
            "approved": "create_design_docs",
            "needs_revision": "revise_user_stories"
        }
    )

    builder.add_edge(
        "revise_user_stories",
        "product_owner_review"
    )

    # ==========================================================
    # DESIGN LOOP
    # ==========================================================

    builder.add_edge(
        "create_design_docs",
        "design_review"
    )

    builder.add_conditional_edges(
        "design_review",
        route_design_review,
        {
            "approved": "generate_code",
            "needs_revision": "revise_design_docs"
        }
    )

    builder.add_edge(
        "revise_design_docs",
        "design_review"
    )

    # ==========================================================
    # DEVELOPMENT
    # ==========================================================

    builder.add_edge(
        "generate_code",
        END
    )

    return builder.compile(
        checkpointer=checkpointer
    )

