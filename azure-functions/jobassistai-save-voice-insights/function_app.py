import azure.functions as func
import logging
import os
import requests
import json
from transcribe_whisper import download_blob_to_temp, transcribe_with_whisper, upload_blob_from_file
from config import SYSTEM_ROLE_CREATE_INSIGHT, FUNCTION_HTTP_OPENAI_URL, FUNCTION_SAVE_INSIGHTS_URL, AZURE_STORAGE_CONTAINER_NAME

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="voice-insights/audio-files/{name}", connection="jobassistaistorage_STORAGE") 
def save_voice_insights(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    try:
        logging.info("Saving voice insights...")

        blob_name = myblob.name.replace(f"{AZURE_STORAGE_CONTAINER_NAME}/", "")

        # Download the blob to a temporary file
        temp_file_path = download_blob_to_temp(blob_name)

        # Verify file exists
        if not os.path.exists(temp_file_path):
            raise FileNotFoundError(f"Temporary file {temp_file_path} not found after download")

        # Transcribe the audio file with Whisper
        transcript = transcribe_with_whisper(temp_file_path)

        if transcript:
            
            # Upload the transcript to Azure Blob Storage
            upload_blob_from_file(transcript, blob_name)

            # Convert transcipt to insight(category, details) using Azure OpenAI
            user_prompt = f"Transcript: {transcript}"

            # Prepare the payload and send to OpenAI Azure Function
            payload = {"system_role" : SYSTEM_ROLE_CREATE_INSIGHT, "user_prompt" : user_prompt}
            response = requests.post(FUNCTION_HTTP_OPENAI_URL, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                raw_message = response_data.get("message", {})
                cleaned_response = raw_message.replace("```json", "").replace("```", "").strip()
                response_message = json.loads(cleaned_response)

                # Extract category and details from response_message
                category = response_message.get("category", "")
                details = response_message.get("details", "")
                logging.info(f"Insight received from OpenAI: category: {category}, details: {details}")

                if category and details:
                    try:
                        # Prepare JSON payload
                        cosmos_payload = {
                            "category": category,
                            "details": details
                        }
                        response = requests.post(FUNCTION_SAVE_INSIGHTS_URL, json=cosmos_payload)
                        if response.status_code == 200:
                            logging.info("Voice Insight successfully added to Cosmos DB.")
                        else:
                            logging.error(f"Save Voice Insight - Save insight error: {str(response.text)}")
                    except Exception as e:
                        logging.error(f"Save Voice Insight - Error: {str(e)}")
                else:
                    logging.error("Save Voice Insight - Empty category or detail")
            else:
                logging.error(f"Save Voice Insight - OpenAI Azure Error: {str(response.text)}")
        else:
            logging.error("Error while transcribing voice insights")

    except Exception as e:
        logging.error(f"Error while saving voice insights: {str(e)}")

    finally:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)