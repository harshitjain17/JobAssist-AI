import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

endpoint = os.getenv("OPENAI_SERVICE_URI")
model_name = os.getenv("CHAT_MODEL")

subscription_key = os.getenv("OPENAI_SERVICE_KEY")
api_version = os.getenv("OPENAI_SERVICE_VERSION")

client = ChatCompletionsClient(
    endpoint=endpoint,
    model_name=model_name,
    credential=AzureKeyCredential(subscription_key),
)

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="I am going to Paris, what should I see?"),
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=model_name
)

print(response.choices[0].message.content)