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
    revise_user_stories,
)

from app.nodes.design import (
    create_design_docs,
    review_design,
    revise_design_docs
)

from app.nodes.development import (
    generate_code,
    code_review,
    fix_code_after_review,
    security_review,
    fix_code_after_security
)

from app.nodes.testing import (
    write_test_cases,
    test_case_review,
    fix_test_cases,
    qa_testing,
    fix_code_after_qa
)
# =========================================================
# ROUTING FUNCTION
# =========================================================

def route_product_owner_review(state: SDLCState):
    print("=" * 40)
    print("PRODUCT OWNER STATUS:", state.get("product_owner_status"))
    print("=" * 40)

    if state["product_owner_status"] == "APPROVED":
        print("Routing -> create_design_docs")
        return "approved"
    
    print("Routing -> revise_user_stories")
    return "needs_revision"

def route_design_review(state: SDLCState):

    print("Design Review Status:", state.get("design_review_status"))

    if state.get("design_review_status") == "APPROVED":
        print("Routing to generate_code")
        return "approved"

    print("Routing to revise_design_docs")
    return "needs_revision"


def route_code_review(state: SDLCState):

    status = state.get("code_review_status", "")
    
    print("=" * 30)
    print("CODE REVIEW STATUS:", status)
    print("=" * 30)

    if status == "APPROVED":
        return "approved"

    return "needs_revision"


def route_security_review(state: SDLCState):

    status = state.get("security_review_status", "")

    print("=" * 30)
    print("SECURITY REVIEW STATUS:", status)
    print("=" * 30)

    if status == "APPROVED":
        return "approved"

    return "needs_revision"

def route_test_case_review(state: SDLCState):

    status = state.get("test_case_review_status", "")

    print("=" * 30)
    print("TEST CASE REVIEW STATUS:", status)
    print("=" * 30)

    if status == "APPROVED":
        return "approved"

    return "needs_revision"

def route_qa_review(state: SDLCState):

    status = state.get("qa_status","")

    print("="*30)
    print("QA STATUS:",status)
    print("="*30)

    if status=="APPROVED":
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

    builder.add_node(

    "code_review",

    code_review

)

    builder.add_node(

    "fix_code_after_review",

    fix_code_after_review

)
    
    builder.add_node(
    "security_review",
    security_review
)

    builder.add_node(
    "fix_code_after_security",
    fix_code_after_security
)
    
#--------------------------------------
# TESTING PHASE
#--------------------------------------

    builder.add_node(
    "write_test_cases",
    write_test_cases
)

    builder.add_node(
    "test_case_review",
    test_case_review
)

    builder.add_node(
    "fix_test_cases",
    fix_test_cases
)

    builder.add_node(
    "qa_testing",
    qa_testing
)

    builder.add_node(
    "fix_code_after_qa",
    fix_code_after_qa
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

    "code_review"

)

    builder.add_conditional_edges(

    "code_review",

    route_code_review,

    {

        "approved":"security_review",

        "needs_revision":"fix_code_after_review"

    }

)

    builder.add_edge(

    "fix_code_after_review",

    "code_review"

)
    

    builder.add_conditional_edges(
    "security_review",
    route_security_review,
    {
        "approved": "write_test_cases",
        "needs_revision": "fix_code_after_security"
    }
)
    
    builder.add_conditional_edges(
    "test_case_review",
    route_test_case_review,
    {
        "approved": "qa_testing",
        "needs_revision": "fix_test_cases"
    }
)
    
    builder.add_conditional_edges(

    "qa_testing",

    route_qa_review,

    {

        "approved":END,

        "needs_revision":"fix_code_after_qa"

    }

)

    builder.add_edge(
    "fix_code_after_security",
    "security_review"
)

    builder.add_edge(
    "write_test_cases",
    "test_case_review"
)
    
    builder.add_edge(
    "fix_test_cases",
    "test_case_review"
)
    
    builder.add_edge(

    "fix_code_after_qa",

    "qa_testing"

)
    
    return builder.compile(
        checkpointer=checkpointer
    )

