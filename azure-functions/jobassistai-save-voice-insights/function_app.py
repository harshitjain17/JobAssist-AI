import azure.functions as func
import logging
import os
import requests
from transcribe_whisper import download_blob_to_temp, transcribe_with_whisper, upload_blob_from_file
from config import SYSTEM_ROLE_CREATE_INSIGHT, FUNCTION_HTTP_OPENAI_URL, FUNCTION_SAVE_INSIGHTS_URL

app = func.FunctionApp()

@app.blob_trigger(arg_name="save_voice_insights", path="path-of-blob",
                               connection="jobassistaistorage_STORAGE") 
def save_voice_insights(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    try:
        logging.info("Saving voice insights...")

        # Download the blob to a temporary file
        temp_file_path = download_blob_to_temp(myblob.name)

        # Transcribe the audio file with Whisper
        transcript = transcribe_with_whisper(temp_file_path)
        
        if transcript:
            # Upload the transcript to Azure Blob Storage
            upload_blob_from_file(transcript, f"{myblob.name}.txt")

            # Convert transcipt to insight(category, details) using Azure OpenAI
            user_prompt = f"Transcript: {transcript}"

            # Prepare the payload and send to OpenAI Azure Function
            payload = {"system_role" : SYSTEM_ROLE_CREATE_INSIGHT, "user_prompt" : user_prompt}
            response = requests.post(FUNCTION_HTTP_OPENAI_URL, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                response_message = response_data.get("message", {})

                # Extract category and details from response_message
                category = response_message.get("category", "")
                details = response_message.get("details", "")
                logging.info(f"Insight received from OpenAI: category: {category}, details: {details}")

                if category and details:
                    # Save the insight to Cosmos DB
                    try:
                        response = requests.post(FUNCTION_SAVE_INSIGHTS_URL, json=payload)
                        if response.status_code == 200:
                            return func.HttpResponse("Voice Insight successfully added to Cosmos DB.", status_code=200)
                        else:
                            return func.HttpResponse(f"Save Voice Insight - Save insight azure function error: {str(response.text)}", status_code=500)
                    except Exception as e:
                        return func.HttpResponse(f"Save Voice Insight - Save insight azure function error: {str(e)}", status_code=500)
                else:
                    return func.HttpResponse("Save Voice Insight - empty category or detail", status_code=400)
            else:
                return func.HttpResponse(f"Save Voice Insight - Create Insight Azure OpenAI Error: {str(e)}", status_code=500)
        else:
            return func.HttpResponse("Error while transcribing voice insights", status_code=400)

    except Exception as e:
        return func.HttpResponse("Error while saving voice insights", status_code=400)
    finally:
        # Clean up temporary file
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
