import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Azure AI Search details
AZURE_SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
AZURE_SEARCH_KEY = os.environ["AZURE_SEARCH_KEY"]
KNOWLEDGE_RETENTION_INDEX_NAME = os.environ["KNOWLEDGE_RETENTION_INDEX_NAME"]
SEARCH_URL = f"https://{AZURE_SEARCH_ENDPOINT}.search.windows.net/indexes/{KNOWLEDGE_RETENTION_INDEX_NAME}?api-version=2023-07-01-preview"

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_KEY
}

# Define the index schema
index_payload = {
    "name": KNOWLEDGE_RETENTION_INDEX_NAME,
    "fields": [
        { "name": "id", "type": "Edm.String", "key": True, "searchable": False },
        { "name": "category", "type": "Edm.String", "searchable": True },
        { "name": "details", "type": "Edm.String", "searchable": True },
        {
            "name": "detailsVector",
            "type": "Collection(Edm.Single)",
            "searchable": True,
            "dimensions": 1536,  # Example dimension for OpenAI embeddings
            "vectorSearchProfile": "default"
        }
    ],
    "vectorSearch": {
        "profiles": [
            {
                "name": "default",
                "algorithm": "hnsw",  # Vector search algorithm
                "hnswParameters": { "m": 4, "efConstruction": 400, "efSearch": 500 }
            }
        ]
    }
}

# Make the request to create the index
response = requests.put(SEARCH_URL, headers=headers, json=index_payload)

# Print response
print(response.status_code, response.text)