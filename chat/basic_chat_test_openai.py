import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

endpoint = os.getenv("OPENAI_SERVICE_URI")
model_name = os.getenv("CHAT_MODEL")
deployment = os.getenv("CHAT_MODEL")

subscription_key = os.getenv("OPENAI_SERVICE_KEY")
api_version = os.getenv("OPENAI_SERVICE_VERSION")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?",
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

print(response.choices[0].message.content)