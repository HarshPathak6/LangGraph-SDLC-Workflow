from app.state import SDLCState
from app.llm import llm



def write_test_cases(state: SDLCState):

    print("===== ENTERED write_test_cases =====")

    prompt = f"""
You are a software tester.

Write an API test case for this code.

Return only the test case.

Code:

{state["generated_code"]}
"""

    print("Calling Test Case Generator...")

    response = llm.invoke(prompt)

    print("Test cases generated")

    return {
        "test_cases": response.content,
        "current_stage": "test_cases_generated"
    }



def test_case_review(state: SDLCState):

    print("===== ENTERED test_case_review =====")

    print("Test case length:", len(state.get("test_cases", "")))

    prompt = f"""
You are a senior QA engineer.

Review this software test case.

If it is good enough, reply exactly:

STATUS: APPROVED

Otherwise reply exactly:

STATUS: FEEDBACK

FEEDBACK:
<short feedback>

Test Cases:

{state["test_cases"]}
"""

    print("Calling Test Case Review LLM...")

    attempts = state.get("test_case_review_attempts", 0) + 1

    response = llm.invoke(prompt)

    print("\n========= RAW LLM RESPONSE =========")
    print(response.content)
    print("===================================\n")

    review = response.content

    if "STATUS: APPROVED" in review.upper():
        status = "APPROVED"
        feedback = ""

    else:
        status = "FEEDBACK"

        if "FEEDBACK:" in review.upper():
            feedback = review.split("FEEDBACK:",1)[1].strip()
        else:
            feedback = review

    print("============================")
    print("Review Attempt:", attempts)
    print("Status:", status)
    print("============================")

    if attempts >= 3:
        print("Maximum review attempts reached. Auto-approving.")

        return {
            "test_case_review": "Auto-approved after maximum attempts.",
            "test_case_review_status": "APPROVED",
            "test_case_review_feedback": "",
            "test_case_review_attempts": attempts,
            "current_stage": "test_case_review"
        }

    return {
        "test_case_review": feedback,
        "test_case_review_status": status,
        "test_case_review_feedback": feedback,
        "test_case_review_attempts": attempts,
        "current_stage": "test_case_review"
    }


def fix_test_cases(state: SDLCState):

    print("===== ENTERED fix_test_cases =====")

    prompt = f"""
Improve this software test case.

Code:

{state["generated_code"]}

Reviewer Feedback:

{state["test_case_review_feedback"]}

Current Test Cases:

{state["test_cases"]}

Return only the improved test case.
"""

    print("Calling Fix Test Case LLM...")

    response = llm.invoke(prompt)

    print("Test case fixed")

    return {
        "test_cases": response.content,
        "current_stage": "test_cases_fixed"
    }


def qa_testing(state: SDLCState):

    print("===== ENTERED qa_testing =====")

    print("Generated code length:",
        len(state.get("generated_code", "")))

    prompt = f"""
You are a QA engineer.

Review this code together with its test case.

If everything looks correct reply exactly:

STATUS: APPROVED

Otherwise reply exactly:

STATUS: FEEDBACK

FEEDBACK:
<short feedback>

Code:

{state["generated_code"]}

Test Cases:

{state["test_cases"]}
"""

    print("Calling QA LLM...")

    attempts = state.get("qa_attempts", 0) + 1

    response = llm.invoke(prompt)

    print("\n========= RAW QA RESPONSE =========")
    print(response.content)
    print("==================================\n")

    review = response.content

    if "STATUS: APPROVED" in review.upper():
        status = "APPROVED"
        feedback = ""

    else:
        status = "FEEDBACK"

        if "FEEDBACK:" in review.upper():
            feedback = review.split("FEEDBACK:",1)[1].strip()
        else:
            feedback = review

    print("========================")
    print("QA Attempt:", attempts)
    print("Status:", status)
    print("========================")

    if attempts >= 3:

        print("Maximum QA attempts reached. Auto-approving.")

        return {
            "qa_result":"Auto-approved after maximum attempts.",
            "qa_status":"APPROVED",
            "qa_feedback":"",
            "qa_attempts":attempts,
            "current_stage":"qa_testing"
        }

    return {

        "qa_result":feedback,
        "qa_status":status,
        "qa_feedback":feedback,
        "qa_attempts":attempts,
        "current_stage":"qa_testing"
    }


def fix_code_after_qa(state: SDLCState):

    print("===== ENTERED fix_code_after_qa =====")

    prompt = f"""
Improve this code using the QA feedback.

Return only the updated code.

QA Feedback:

{state["qa_feedback"]}

Current Code:

{state["generated_code"]}
"""

    print("Calling QA Fix LLM...")

    response = llm.invoke(prompt)

    print("QA fixes completed")

    return {

        "generated_code":response.content,

        "current_stage":"qa_code_fixed"
    }