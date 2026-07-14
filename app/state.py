from typing import TypedDict


class SDLCState(TypedDict, total=False):

    # Project identity
    project_id: str

    # Initial input
    requirements: str

    # Requirements phase
    user_stories: str
    product_owner_review: str
    product_owner_status: str

    # Design phase
    design_docs: str
    design_review: str
    design_status: str

    # Development phase
    generated_code: str
    code_review: str
    code_status: str

    # Security phase
    security_review: str
    security_status: str

    # Testing phase
    test_cases: str
    test_case_review: str
    test_case_status: str

    # QA phase
    qa_result: str
    qa_status: str

    # Deployment
    deployment_result: str

    # General tracking
    current_stage: str