import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

endpoint = "https://jobassistai-open-ai-service.openai.azure.com/"
model_name = "gpt-4o-mini"

client = ChatCompletionsClient(
    endpoint=endpoint,
    model_name=model_name,
    credential=DefaultAzureCredential(),
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