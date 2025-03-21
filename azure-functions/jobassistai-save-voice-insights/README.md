# JobAssistAI Save Voice Insights Azure Function

## Overview

This Azure Function allows job coaches to store important insights they encounter during work through voice memo. These insights can be any random but useful information that might help future job coaches, especially when the original job coach is absent. In the UI, the job coach can upload a voice memo, which is saved in **Azure Blob storage**. This function is triggered as **blob trigger** when the audio file is uploaded. The audio file is then transcribed using **Azure AI Speech Services** and **Azure OpenAI's Whisper model**. The transcribed text is stored in a file and uploaded to blob storage for future references and the transcribed text is categorized as `category` and `details` using the Azure Function `jobassistai-http-trigger-openai` which returns category and details in JSON format. This is used as a payload to trigger the Azure Function `jobassistai-save-insights`, which generates a vector representation of the details using **Azure OpenAI's `text-embedding-ada-002` model** and stores the insights with id, category, details and details vector in **Azure Cosmos DB**.

## Features

- **Blob Triggered**: Invoked when audio file is uploaded to Azure Blob storage.
- **Azure OpenAI's Whisper model**: Transcribes the audio file to text.
- **Azure Blob Storage**: Stores audio files and transcribed text files
- **Azure Function (jobassistai-http-trigger-openai)**: Calls Azure Open AI to extract the main theme as `category` and provide a concise but complete summary as `details`, ensuring no critical information is lost from the transcribed text.
- **Azure Function (jobassistai-save-insights)**: Stores insights in Azure Cosmos DB for effecient retreival.
```python
insight = {
            "id": str(uuid.uuid4()),        # Unique ID for the insight
            "category": category,           # Category of the insight provided by Job Coach
            "details": details,             # Details of the insight provided by Job Coach
            "detailsVector": details_vector # Vector representation of the details
        }
```
- **Audio-based Input & Text Output**: Accepts audio in `WAV`, `MP3`, `OGG` and `FLAC` format and returns response message in text format.
- **Modular Design**: Organized into reusable modules for configuration, clients.

## Directory Structure
```
jobassistai-save-insights/
├── function_app.py              # Main entry point with the Azure Function
├── config.py                    # Environment variables and configuration
├── clients.py                   # Client initializations (OpenAI and Blob)
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation (this file)
└── host.json                    # Azure Functions configuration (auto-generated or customized)
└── transcribe_whisper.py        # Download/Upload to Blob and Transcribe functionalities
```

## Prerequisites

- **Azure Subscription**: Access to Azure AI services.
- **Azure OpenAI's Whisper model**: The model is deployed and accessible.
- **Azure Blob Storage**: The database must be configured to store audio files and transcribed text files.
- **Azure Functions (jobassistai-http-trigger-openai & jobassistai-save-insights)**: The functions are deployed and accessible. Ensure the endpoints are configured correctly in environment variables.
- **Python 3.12**: Compatible with Azure Functions Python runtime.
- **Azure Functions Core Tools**: For local testing and deployment.

## Usage

1. **Upload a voice memo**: Sends a blob trigger.
2. **Processing**:
   - The function transcribes audio file to text.
   - Uploads the transcribed text file to Blob storage.
   - Calls `jobassistai-http-trigger-openai` function to categorize the transcribed text as `category` and `detail`
   - Calls `jobassistai-save-insights` function to save the insight in Azure Cosmos DB.
3. **Output**: Generated response is returned to the caller in text format.

## Dependencies

See `requirements.txt`:
- `azure-functions>=1.18.0`
- `python-dotenv>=1.0.0`
- `azure-storage-blob>=12.19.0`
- `openai>=1.0.0`