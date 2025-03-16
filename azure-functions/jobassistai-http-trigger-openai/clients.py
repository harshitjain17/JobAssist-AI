from config import OPENAI_ENDPOINT, OPENAI_KEY, OPENAI_API_VERSION
from openai import AzureOpenAI

# Clients
openai_client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    api_key=OPENAI_KEY,
    api_version=OPENAI_API_VERSION
)