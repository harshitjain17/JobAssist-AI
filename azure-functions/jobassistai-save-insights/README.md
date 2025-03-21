# JobAssistAI Save Insights Azure Function

## Overview

This Azure Function allows job coaches to store important insights they encounter during work. These insights can be any random but useful information that might help future job coaches, especially when the original job coach is absent. When a user clicks **Save Insight** in the UI, this function is triggered. The function generates a vector representation of the details using **Azure OpenAI's `text-embedding-ada-002` model** for future AI-powered searches and stores the insights with id, category, details and details vector in **Azure Cosmos DB**.

## Features

- **HTTP Triggered**: Invoked via HTTP request.
- **Azure OpenAI (text-embedding-ada-002) Integration**: Creates a vector representation of the `details`.
- **Insight Document structure**: 

```python
insight = {
            "id": str(uuid.uuid4()),        # Unique ID for the insight
            "category": category,           # Category of the insight provided by Job Coach
            "details": details,             # Details of the insight provided by Job Coach
            "detailsVector": details_vector # Vector representation of the details
        }
```
- **Azure Cosmos DB**: Stores insights in Azure Cosmos DB for effecient retreival.
- **JSON-based Input & Text Output**: Accepts `category` and `details` in JSON format and returns response message in text format.
- **Modular Design**: Organized into reusable modules for configuration, clients.

## Directory Structure
```
jobassistai-save-insights/
├── function_app.py              # Main entry point with the Azure Function
├── config.py                    # Environment variables and configuration
├── clients.py                   # Client initializations (OpenAI and Cosmos)
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation (this file)
└── host.json                    # Azure Functions configuration (auto-generated or customized)
```

## Prerequisites

- **Azure Subscription**: Access to Azure AI services.
- **Azure OpenAI**: The `text-embedding-ada-002` model is deployed and accessible.
- **Azure Cosmos DB**: The database must be configured to store insights.
- **Python 3.12**: Compatible with Azure Functions Python runtime.
- **Azure Functions Core Tools**: For local testing and deployment.

## Usage

1. **HTTP Trigger**: Send a HTTP trigger with category and details as JSON payload.
2. **Processing**:
   - The function generates embeddings of details using `text-embedding-ada-002`.
   - Saves insights in Azure Cosmos DB.
3. **Output**: Generated response is returned to the caller in JSON format.

## Dependencies

See `requirements.txt`:
- `azure-functions>=1.18.0`
- `python-dotenv>=1.0.0`
- `azure.cosmos`
- `openai>=1.0.0`