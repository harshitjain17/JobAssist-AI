import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

endpoint = os.getenv("OPENAI_SERVICE_URI")
model_name = os.getenv("CHAT_MODEL")
deployment = os.getenv("CHAT_MODEL")

subscription_key = os.getenv("OPENAI_SERVICE_KEY")
api_version = os.getenv("OPENAI_SERVICE_VERSION")

search_endpoint = os.getenv("AISEARCH_CONNECTION_URI")
search_key = os.getenv("AISEARCH_CONNECTION_KEY")
index_name = os.getenv("AISEARCH_INDEX_NAME")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

data_sources = {
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

system_prompt = """
You are an AI assistant for job placement specialists.
You are trained on the same material as the specialists so you understand their roles & responsibilities as well as the mission & values of their organization.
Your assistance is invaluable to helping the specialists operate efficiently to improve the lives of their consumers.
You may receive general or specific questions and you should helpfully respond accordingly, always using the reference material as your primary source and providing citations as needed.
You may also receive structured detail regarding the context in which the question is being asked such as an event that has taken place or detail regarding a consumer.
If you receive only the structured detail, respond with the next best action that should be taken based on this detail.
If the detail is accompanied by an inquiry, incorporate the detail as context to provide a more targeted response.
"""

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What are the key responsibilities of a job placement specialist?",
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment,
    extra_body=data_sources
)

print(response.choices[0].message.content)

os.makedirs(".out", exist_ok=True)
with open(".out/response__chat_with_resources.json", "w") as f:
    f.write(response.model_dump_json(indent=2))