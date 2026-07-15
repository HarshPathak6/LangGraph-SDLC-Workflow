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
    create_design_docs
)


# =========================================================
# ROUTING FUNCTION
# =========================================================

def route_product_owner_review(state: SDLCState):
    """
    Decides where the graph goes after
    the Product Owner reviews the stories.
    """

    if state["product_owner_status"] == "APPROVED":
        return "create_design_docs"

    return "revise_user_stories"


# =========================================================
# BUILD GRAPH
# =========================================================

def build_graph(checkpointer):

    builder = StateGraph(SDLCState)


    # -----------------------------------------------------
    # ADD NODES
    # -----------------------------------------------------

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

    builder.add_node(
        "create_design_docs",
        create_design_docs
    )


    # -----------------------------------------------------
    # NORMAL EDGES
    # -----------------------------------------------------

    # START
    #   ↓
    # Generate User Stories

    builder.add_edge(
        START,
        "generate_user_stories"
    )


    # Generate User Stories
    #   ↓
    # Product Owner Review

    builder.add_edge(
        "generate_user_stories",
        "product_owner_review"
    )


    # Revised User Stories
    #   ↓
    # Product Owner reviews them again

    builder.add_edge(
        "revise_user_stories",
        "product_owner_review"
    )


    # Create Design Docs
    #   ↓
    # END for now

    builder.add_edge(
        "create_design_docs",
        END
    )


    # -----------------------------------------------------
    # CONDITIONAL EDGE
    # -----------------------------------------------------

    builder.add_conditional_edges(
        "product_owner_review",
        route_product_owner_review,
        {
            "create_design_docs": "create_design_docs",
            "revise_user_stories": "revise_user_stories"
        }
    )


    # -----------------------------------------------------
    # COMPILE WITH NEON CHECKPOINTER
    # -----------------------------------------------------

    return builder.compile(
        checkpointer=checkpointer
    )

