from langchain_openai import ChatOpenAI
from app.config import settings

llm = ChatOpenAI(
    model=settings.OPENROUTER_MODEL,
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.2
)

# from langchain_google_genai import ChatGoogleGenerativeAI
# from app.config import settings

# print("Gemini model from settings:", settings.GEMINI_MODEL)
# llm = ChatGoogleGenerativeAI(
#     model=settings.GEMINI_MODEL,
#     google_api_key=settings.GEMINI_API_KEY,
#     temperature=0.2,
# )

# from click import prompt
# from langchain_groq import ChatGroq
# from app.config import settings

# llm = ChatGroq(
#     model=settings.GROQ_MODEL,
#     api_key=settings.GROQ_API_KEY,
#     temperature=0.2
# )

# def invoke_llm(prompt: str) -> dict:
#     """
#     Invokes the LLM with the given prompt and returns the response.
#     """
#     response = llm.invoke(prompt)
#     return response.content