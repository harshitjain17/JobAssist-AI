# JobAssistAI Azure SpeechSDK Text to Speech Function

## Overview

This Azure Function integrates with **Azure SpeechSDK** to generate audio responses to the text input. It is designed to be reusable for various Azure Text-to-Speech requests and is currently used to generate audio for detailed instructions of task breakdown in JobAssistAI application.

## Features

- **HTTP Triggered**: Invoked via HTTP request.
- **Azure SpeechSDK Integration**: Calls Azure SpeechSDK to generate audio responses in MP3 format.
- **JSON-based Input & MP3 audio Output**: Accepts input in JSON format and returns MP3 audio.
- **Modular Design**: Organized into reusable modules for configuration and clients.
- **Reusability**: Azure Function to process HTTP requests with dynamic text input, enabling reusable and flexible integrations.

## Directory Structure
```
jobassistai-http-trigger-tts/
├── function_app.py              # Main entry point with the Azure Function
├── config.py                    # Environment variables and configuration
├── clients.py                   # Client initializations (SpeechSDK)
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation (this file)
└── host.json                    # Azure Functions configuration (auto-generated or customized)
```

## Prerequisites

- **Azure Subscription**: Access to Azure SpeechSDK services.
- **Python 3.12**: Compatible with Azure Functions Python runtime.
- **Azure Functions Core Tools**: For local testing and deployment.

## Usage

1. **HTTP Trigger**: Send a HTTP trigger with text as JSON payload.
2. **Processing**:
   - The function extracts text from the request.
   - Calls Azure SpeechSDK to generate audio response based on the input text.
3. **Output**: Generated response is returned to the caller in MP3 format.

## Dependencies

See `requirements.txt`:
- `azure-functions>=1.18.0`
- `azure-cognitiveservices-speech`
- `python-dotenv>=1.0.0`