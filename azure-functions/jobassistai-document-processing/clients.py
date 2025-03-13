# clients.py
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
from config import DI_ENDPOINT, DI_KEY, BLOB_CONNECTION, OPENAI_ENDPOINT, OPENAI_KEY, OPENAI_DEPLOYMENT, OPENAI_API_VERSION

# Clients
di_client = DocumentIntelligenceClient(
    endpoint=DI_ENDPOINT,
    credential=AzureKeyCredential(DI_KEY)
)
blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION)
openai_client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    api_key=OPENAI_KEY,
    api_version=OPENAI_API_VERSION
)