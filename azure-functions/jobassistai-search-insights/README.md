# JobAssistAI Search Insights Azure Function

## Overview

This Azure Function enables job coaches to search insights stored in **Azure Cosmos DB** using **natural language queries**. It integrates **Azure OpenAI (text-embedding-ada-002)** to generate embeddings for the query and uses **Azure AI Search** to retrieve relevant insights. Instead of returning full database entries, this function calls an existing Azure Funtion **jobassistai-http-trigger-openai** to extract and summarize the most relevant information.

## Features

- **HTTP Triggered**: Invoked via HTTP request.
- **Azure OpenAI (text-embedding-ada-002) Integration**: Converts natural language queries into embeddings.
- **Azure AI Search Integration**: Retrieves relevant information stored in Azure Cosmos DB.
- **Azure Function (jobassistai-http-trigger-openai)**: Calls Azure Open AI to extract and refine the response.
- **JSON-based Input & Output**: Accepts search query in JSON format and returns relevant insights in JSON format.
- **Modular Design**: Organized into reusable modules for configuration, clients.

## Directory Structure
```
jobassistai-search-insights/
├── function_app.py              # Main entry point with the Azure Function
├── config.py                    # Environment variables and configuration
├── clients.py                   # Client initializations (SpeechSDK)
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation (this file)
└── host.json                    # Azure Functions configuration (auto-generated or customized)
```

## Prerequisites

- **Azure Subscription**: Access to Azure AI services.
- **Azure OpenAI**: The `text-embedding-ada-002` model is deployed and accessible.
- **Azure AI Search**: The index is created and configured with data from Cosmos DB.
- **Azure Function `jobassistai-http-trigger-openai`**: The function is deployed and accessible. Ensure the endpoint is configured correctly in environment variables.
- **Python 3.12**: Compatible with Azure Functions Python runtime.
- **Azure Functions Core Tools**: For local testing and deployment.

## Usage

1. **HTTP Trigger**: Send a HTTP trigger with search query as JSON payload.
2. **Processing**:
   - The function generates embeddings using `text-embedding-ada-002`.
   - Calls Azure AI Search to fetch relevant results from Azure Cosmos DB.
   - The function calls `jobassistai-http-trigger-openai` function to summarize and extract only the most relevant details.
3. **Output**: Generated response is returned to the caller in JSON format.

## Dependencies

See `requirements.txt`:
- `azure-functions>=1.18.0`
- `python-dotenv>=1.0.0`
- `azure.cosmos`
- `openai>=1.0.0`