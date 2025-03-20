import openai
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from config import AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_CONTAINER_NAME, API_KEY, API_ENDPOINT, API_VERSION

# Create a blob service client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)

# Configure OpenAI client
api_client = openai.AzureOpenAI(
    api_key=API_KEY,
    api_version=API_VERSION,
    base_url=API_ENDPOINT
)