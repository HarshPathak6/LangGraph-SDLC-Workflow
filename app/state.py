from typing import TypedDict


class SDLCState(TypedDict, total=False):

    # Project identity
    project_id: str

    # Initial input
    requirements: str

    # General tracking
    current_stage: str

    # Requirements phase
    user_stories: str

    # Product Owner Review 
    product_owner_review: str
    product_owner_status: str

    # Product Owner Review Loop tracking
    product_owner_attempts: int

    # Design phase
    design_docs: str

    # Design Review
    design_review_status: str
    design_review_feedback: str
    design_review_attempts: int

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

    