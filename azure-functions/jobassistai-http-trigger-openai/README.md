# JobAssistAI Azure Open AI Function

## Overview

This Azure Function integrates with **Azure OpenAI** to generate responses based on a predefined **system prompt** and a **user prompt**. It is designed to be reusable for various OpenAI-powered requests and is currently used for task breakdown in JobAssistAI application.

## Features

- **HTTP Triggered**: Invoked via HTTP request.
- **Dynamic Prompting**: Uses `system_prompt_mapping.json` to retrieve the appropriate system prompt based on the provided system role.
- **Azure OpenAI Integration**: Calls Azure OpenAI API to generate structured responses.
- **JSON-based Input & Output**: Accepts input in JSON format and returns structured AI-generated responses.
- **Modular Design**: Organized into reusable modules for configuration, clients and system prompt mapping.
- **Reusability**: Enable reusability by adding a new system role in `system_prompt_mapping.json` and sending HTTP requests with this system role and user prompt.

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

1. **HTTP Trigger**: Send a HTTP trigger with system role and user prompt.
2. **Processing**:
   - The function extracts system role and user prompt from the request.
   - References `system_prompt_mapping.json` to retrieve the appropriate system prompt based on the provided system role.
   - Calls Azure OpenAI to generate a structured response based on the combined system and user prompts.
3. **Output**: Generated response is returned to the caller in JSON format.

## Dependencies

See `requirements.txt`:
- `azure-functions>=1.18.0`
- `openai>=1.0.0`
- `python-dotenv>=1.0.0`