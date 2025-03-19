import os
import sys
import tempfile
import time
from dotenv import load_dotenv
import openai
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Load environment variables
load_dotenv()

def download_blob_to_temp(blob_name):
    """Download a blob to a temporary file and return the file path."""
    conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME")
    
    if not conn_str or not container_name:
        raise ValueError("Azure Storage connection string and container name must be set in .env file")
    
    # Create a blob service client
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_client = blob_service_client.get_container_client(container_name)

    # blob_list = container_client.list_blobs()
    # for blob in blob_list:
    #     print(blob.name)
    # quit()

    blob_client = container_client.get_blob_client(blob_name)
    
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
    api_key = os.environ.get("OPENAI_SERVICE_KEY")
    api_endpoint = os.environ.get("OPENAI_SERVICE_URI")
    api_version = os.environ.get("OPENAI_SERVICE_VERSION")
    
    if not api_key or not api_endpoint:
        raise ValueError("Azure OpenAI API key and endpoint must be set in .env file")
    
    # Configure OpenAI client
    client = openai.AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        base_url=api_endpoint
    )
    
    print("Starting transcription with Whisper model...")
    
    try:
        # Check file size - Azure OpenAI has a 25MB limit
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > 25:
            raise ValueError(f"File is {file_size_mb:.2f}MB, exceeding the 25MB limit for Whisper API")
        
        # Open the audio file
        with open(file_path, "rb") as audio_file:
            # Call the Azure OpenAI audio transcription API (using Whisper model)
            response = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper",
                response_format="text"
            )
            
        return response
        
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        raise

def upload_blob_from_file(file_path, blob_path):
    """Upload a file to Azure Blob Storage"""
    
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
    
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    print(f"File uploaded to Azure Blob Storage: {blob_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python transcribe_whisper.py <blob_name>")
        sys.exit(1)
        
    blob_name = sys.argv[1]
    
    try:
        # Download the blob to a temporary file
        temp_file_path = download_blob_to_temp(blob_name)
        
        # Start timer for performance comparison
        start_time = time.time()
        
        # Transcribe the audio file with Whisper
        transcript = transcribe_with_whisper(temp_file_path)
        
        # Calculate transcription time
        transcription_time = time.time() - start_time
        
        # Output the transcript
        print("\nTranscription Result (Azure OpenAI Whisper):\n" + "-" * 40)
        print(transcript)
        print(f"\nTranscription completed in {transcription_time:.2f} seconds")
        
        # Save transcript to file
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(blob_name)[1])
        temp_file_path = temp_file.name
        temp_file.close()
    
        with open(temp_file_path, "w") as file:
            file.write(transcript)
        print(f"\nTranscript saved to {temp_file_path}")
        upload_blob_from_file(temp_file_path, f"{blob_name}.txt")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up temporary file
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    main()
