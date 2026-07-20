from mem0 import MemoryClient
from app.config import settings

client = MemoryClient(api_key=settings.MEM0_API_KEY)


def save_memory(user_id, text):
    print("Saving memory...")

    result = client.add(
        messages=[
            {
                "role": "user",
                "content": text
            }
        ],
        user_id=str(user_id)
    )

    print(result)
    return result


def get_memory(user_id):
    print("Searching memories...")

    result = client.search(
        query="project requirements",
        filters={
            "user_id": str(user_id)
        }
    )

    print(result)
    return result