import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

endpoint = os.getenv("OPENAI_SERVICE_URI")
model_name = os.getenv("CHAT_MODEL")

subscription_key = os.getenv("OPENAI_SERVICE_KEY")
api_version = os.getenv("OPENAI_SERVICE_VERSION")

search_endpoint = os.getenv("AISEARCH_CONNECTION_URI")
search_key = os.getenv("AISEARCH_CONNECTION_KEY")
index_name = os.getenv("AISEARCH_INDEX_NAME")

DEFAULT_SYSTEM_PROMPT = """
You are an AI assistant for job placement specialists.
You are trained on the same material as the specialists so you understand their roles & responsibilities as well as the mission & values of their organization.
Your assistance is invaluable to helping the specialists operate efficiently to improve the lives of their consumers.
You may receive general or specific questions and you should helpfully respond accordingly, always using the reference material as your primary source and providing citations as needed.
You may also receive structured detail regarding the context in which the question is being asked such as an event that has taken place or detail regarding a consumer.
If you receive only the structured detail, respond with the next best action that should be taken based on this detail.
If the detail is accompanied by an inquiry, incorporate the detail as context to provide a more targeted response.
"""

DEFAULT_DATA_SOURCES = {
    "data_sources": [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": search_endpoint,
                "index_name": index_name,
                "authentication": {
                    "type": "api_key",
                    "key": search_key
                }
            }
        }
    ]
}

def create_chat_completion(
        user_content=None,
        user_context=None,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        data_sources=DEFAULT_DATA_SOURCES,
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=model_name
    ):
    
    user_prompt = ""
    if user_context:
        user_prompt = f"{json.dumps(user_context)}\n"
    if user_content:
        user_prompt += user_content
    
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        model=model,
    )
    return response

if __name__ == "__main__":
    # Example usage
    system_prompt = """
    You are an AI assistant for job placement specialists.
    You are trained on the same material as the specialists so you understand their roles & responsibilities as well as the mission & values of their organization.
    Your assistance is invaluable to helping the specialists operate efficiently to improve the lives of their consumers.
    You may receive general or specific questions and you should helpfully respond accordingly, always using the reference material as your primary source and providing citations as needed.
    You may also receive structured detail regarding the context in which the question is being asked such as an event that has taken place or detail regarding a consumer.
    If you receive only the structured detail, respond with the next best action that should be taken based on this detail.
    If the detail is accompanied by an inquiry, incorporate the detail as context to provide a more targeted response.
    """

    user_content = "What are the key responsibilities of a job placement specialist?"
    user_context = {
        "user": { "name": "Roger Jacobs" },
        "consumer": {
            "name": "Violet Adams",
            "phone_mobile": "4045552119",
            "email": "violet88404@gmail.com"
        },
        "contacts": {
            "counselor": { "name": "John Evans", "email": "john.evans@pscservices.com"},
            "emergency": { "name": "Harold Adams", "relationship": "father", "phone": "4045559216"}
        },
        "recent_notes": [
            { "date": "2025-03-01", "content": "First check-in with Violet after qualification, she is very hopeful & engaged." },
            { "date": "2025-03-04", "content": "Violet's dad called to reschedule this afternoon's appointment due to a fever." },
        ],
        "context": {
            "domain": "appointment",
            "event": "status_change",            
            "detail": "no-show",
            "timestamp": datetime.now().isoformat()
        },
    }

    # response = create_chat_completion(system_prompt=system_prompt, user_content=user_content)
    response = create_chat_completion(system_prompt=system_prompt, user_context=user_context)
    print(response.choices[0].message.content)