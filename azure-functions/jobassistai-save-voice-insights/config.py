import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_NAME")

# Azure Whisper API
API_KEY = os.environ.get("OPENAI_SERVICE_KEY")
API_ENDPOINT = os.environ.get("OPENAI_SERVICE_URI")
API_VERSION = os.environ.get("OPENAI_SERVICE_VERSION")

# Azure OpenAI Function App
SYSTEM_ROLE_CREATE_INSIGHT = os.environ["SYSTEM_ROLE_CREATE_INSIGHT"]
FUNCTION_HTTP_OPENAI_URL = os.environ["FUNCTION_HTTP_OPENAI_URL"]

# Save Insights Function App
FUNCTION_SAVE_INSIGHTS_URL = os.getenv("FUNCTION_SAVE_INSIGHTS_URL")