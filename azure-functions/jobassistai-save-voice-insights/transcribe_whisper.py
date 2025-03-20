import os
import sys
import tempfile
import time
from dotenv import load_dotenv
import openai
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from config import AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_CONTAINER_NAME, API_KEY, API_ENDPOINT, API_VERSION
from clients import api_client, blob_service_client, container_client

# Load environment variables
load_dotenv()

def download_blob_to_temp(blob_name):
    """Download a blob to a temporary file and return the file path."""

    if not AZURE_STORAGE_CONNECTION_STRING or not AZURE_STORAGE_CONTAINER_NAME:
        raise ValueError("Azure Storage connection string and container name must be set in .env file")

    # Create a blob service client
    blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=blob_name)
    
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(blob_name)[1])
    temp_file_path = temp_file.name
    temp_file.close()
    
    print(f"Downloading {blob_name} to {temp_file_path}...")
    
    # Download the blob to the temporary file
    with open(temp_file_path, "wb") as file:
        file.write(blob_client.download_blob().readall())
    
    return temp_file_path

def transcribe_with_whisper(file_path):
    """Transcribe an audio file using Azure OpenAI's Whisper model."""
    
    if not API_KEY or not API_ENDPOINT:
        raise ValueError("Azure OpenAI API key and endpoint must be set in .env file")
    
    print("Starting transcription with Whisper model...")
    
    try:
        # Check file size - Azure OpenAI has a 25MB limit
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > 25:
            raise ValueError(f"File is {file_size_mb:.2f}MB, exceeding the 25MB limit for Whisper API")
        
        # Open the audio file
        with open(file_path, "rb") as audio_file:
            # Call the Azure OpenAI audio transcription API (using Whisper model)
            response = api_client.audio.transcriptions.create(
                file=audio_file,
                model="whisper",
                response_format="text"
            )
            
        return response
        
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        raise

def upload_blob_from_file(transcript, blob_name):
    # Save transcript to file
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(blob_name)[1])
    temp_file_path = temp_file.name
    temp_file.close()

    with open(temp_file_path, "w") as file:
        file.write(transcript)
    print(f"\nTranscript saved to {temp_file_path}")
    
    # Clean up the blob_name by removing '.mp3' if present and set the path to 'transcriptions/'
    base_name = blob_name.replace(".mp3", "")
    base_name = blob_name.replace("audio-files/", "")
    blob_path = f"transcriptions/{base_name}.txt"

    # Upload to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=blob_path)
    
    with open(temp_file_path, "rb") as data:
        blob_client.upload_blob(data)

    print(f"File uploaded to Azure Blob Storage: {blob_path}")