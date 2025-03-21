# JobAssistAI Azure Open AI Function

## Overview

This Azure Function integrates with **Azure OpenAI** to generate responses based on a predefined **system prompt** and a **user prompt**. It supports two main HTTP-triggered endpoints for different use cases:

1. **Basic OpenAI Integration**: Standard function to process user prompts with a system prompt.
2. **OpenAI with Azure Search Integration**: Extended function that queries Azure Search data sources and provides citations in the response.

## Features

- **HTTP Triggered**: Invoked via HTTP request.
- **Dynamic Prompting**: Retrieves system prompt based on the system role from `system_prompt_mapping.json`.
- **Azure OpenAI Integration**: Calls Azure OpenAI API to generate structured responses.
- **Azure Search Integration**: The second endpoint integrates with Azure Search to include citations in the response.
- **JSON-based Input & Output**: Accepts input in JSON format and returns structured AI-generated responses.
- **Modular Design**: Organized into reusable modules for configuration, clients, and system prompt mapping.

## Directory Structure
```
jobassistai-http-trigger-openai/
├── function_app.py              # Main entry point with the Azure Function
├── config.py                    # Environment variables and configuration
├── clients.py                   # Client initializations (OpenAI)
├── system_prompt_mapping.json   # Mappings of system role to system prompt
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation (this file)
└── host.json                    # Azure Functions configuration (auto-generated or customized)
```

## Prerequisites

- **Azure Subscription**: Access to Azure OpenAI services.
- **Python 3.12**: Compatible with Azure Functions Python runtime.
- **Azure Functions Core Tools**: For local testing and deployment.

## Usage

1. HTTP Trigger: Send an HTTP request with a `system_role` and `user_prompt` (and optional data_sources for the second endpoint).
2. **Processing**:
   - The function extracts `system_role` and `user_prompt` from the request.
   - The system prompt is retrieved from `system_prompt_mapping.json` based on the `system_role`.
   - The Azure OpenAI API is called to generate a structured response.
   - If the second endpoint is used, additional data sources (like Azure Search) are queried, and citations are included in the response.
3. **Output**: The generated response, along with citations if applicable, is returned in JSON format.

## Dependencies

See `requirements.txt`:
- `azure-functions>=1.18.0`
- `openai>=1.0.0`
- `python-dotenv>=1.0.0`