# Audio Transcription with Azure AI Speech Services

This project demonstrates how to transcribe audio files stored in Azure Blob Storage using Azure AI Speech Services and Azure OpenAI's Whisper model.

## Prerequisites

1. Azure Subscription
3. Azure OpenAI resource with access to the Whisper model
4. Azure Storage Account with a container containing audio files
5. Python 3.7 or later

## Setup

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Fill in your Azure credentials in the `.env` file:
```
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string_here
AZURE_STORAGE_CONTAINER_NAME=your_container_name_here
AZURE_OPENAI_API_KEY=your_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-09-01-preview
```

## Usage

### Using Azure OpenAI's Whisper Model

Transcribe an audio file using the Whisper model:

```bash
python transcribe_whisper.py voice_memos/audio_file_name.wav
```

The transcript will be displayed in the console and saved as `audio_file_name_whisper_transcript.txt`.

## Comparing the Two Methods

- **Azure OpenAI Whisper**: Often provides higher accuracy for challenging audio and different accents, but has a 25MB file size limit.

## Supported Audio Formats

Both services support the following audio formats:
- WAV
- MP3
- OGG
- FLAC

## Notes

- For large audio files, the transcription may take some time
- The audio quality affects transcription accuracy
- Consider implementing batch processing for multiple files
- Azure OpenAI's Whisper has a 25MB file size limit
