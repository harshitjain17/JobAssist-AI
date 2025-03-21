
import os
from pathlib import Path
from opentelemetry import trace
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from config import ASSET_PATH, get_logger

from azure.ai.inference import ChatCompletionsClient

project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)
connections = project.connections.list(
    connection_type=ConnectionType.AZURE_OPEN_AI,
)

print("ConnectionType.AZURE_AI_SERVICES")
for connection in project.connections.list(connection_type=ConnectionType.AZURE_AI_SERVICES):
    print(f"\t{connection}")

print("ConnectionType.AZURE_OPEN_AI")
for connection in project.connections.list(connection_type=ConnectionType.AZURE_OPEN_AI):
    print(f"\t{connection}")

