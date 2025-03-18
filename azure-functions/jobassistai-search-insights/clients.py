from azure.cosmos import CosmosClient
from openai import AzureOpenAI
from config import COSMOS_DB_ENDPOINT, COSMOS_DB_KEY, DATABASE_NAME, CONTAINER_NAME, OPENAI_ENDPOINT, OPENAI_KEY, OPENAI_API_VERSION, AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, KNOWLEDGE_RETENTION_INDEX_NAME

# Connect to Cosmos DB
cosmos_client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
cosmos_database = cosmos_client.get_database_client(DATABASE_NAME)
knowledge_retention_container = cosmos_database.get_container_client(CONTAINER_NAME)

# Clients
openai_client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    api_key=OPENAI_KEY,
    api_version=OPENAI_API_VERSION
)

# Azure AI Search vector query
AZURE_SEARCH_URL = f"https://{AZURE_SEARCH_ENDPOINT}.search.windows.net/indexes/{KNOWLEDGE_RETENTION_INDEX_NAME}/docs/search?api-version=2023-07-01-preview"

azure_search_headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_KEY
}