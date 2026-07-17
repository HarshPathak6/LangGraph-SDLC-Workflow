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

