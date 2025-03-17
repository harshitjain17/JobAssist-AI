from azure.cosmos import CosmosClient
from config import COSMOS_DB_ENDPOINT, COSMOS_DB_KEY, DATABASE_NAME, CONTAINER_NAME

# Connect to Cosmos DB
cosmos_client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
cosmos_database = cosmos_client.get_database_client(DATABASE_NAME)
knowledge_retention_container = cosmos_database.get_container_client(CONTAINER_NAME)