# Description: Azure Function to process case notes and generate reports.

import azure.functions as func
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
from azure.cosmos import CosmosClient
import os
import re
import logging
import json
from dotenv import load_dotenv
load_dotenv()

app = func.FunctionApp()

# Environment variables (set in Function App settings)
DI_ENDPOINT = os.environ["AZURE_DI_ENDPOINT"]
DI_KEY = os.environ["AZURE_DI_KEY"]
BLOB_CONNECTION = os.environ["BLOB_CONNECTION_STRING"]
OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
OPENAI_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]
# COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
# COSMOS_KEY = os.environ["COSMOS_KEY"]

# Clients
di_client = DocumentIntelligenceClient(
    endpoint=DI_ENDPOINT,
    credential=AzureKeyCredential(DI_KEY)
)
blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION)
openai_client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    api_key=OPENAI_KEY,
    api_version=OPENAI_API_VERSION
)

# cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
# db = cosmos_client.get_database_client("JobAssistDB")
# container = db.get_container_client("Reports")

# def generate_report(entities, template_name):
#     try:
#         template_blob = blob_service.get_blob_client(container="templates", blob=template_name)
#         template = template_blob.download_blob().readall().decode("utf-8")
#         return template.format(**entities)
#     except Exception as e:
#         logging.error(f"Error generating report from {template_name}: {str(e)}")
#         return f"Error: Could not generate {template_name.split('_')[0]} report."

@app.blob_trigger(arg_name="myblob", path="case-notes/arriving-files/{name}", connection="jobassistaistorage_STORAGE") 
def main(myblob: func.InputStream):
    logging.info(f"Blob trigger fired for: {myblob.name}")
    
    # Extract note_id from blob path (e.g., "case-notes/arriving-files/note123.txt" -> "note123")
    try:
        note_id = myblob.name.split("/")[-1].split(".")[0]
    except IndexError:
        logging.error("Invalid blob path format")
        raise ValueError("Blob path must follow 'case-notes/arriving-files/{name}'")

    # Read blob content as raw bytes (supports TXT, DOCX, PDF, PNG, etc.)
    try:
        blob_content = myblob.read()  # Raw bytes, no decoding
    except Exception as e:
        logging.error(f"Failed to read blob: {str(e)}")
        raise

    # Extract text with Document Intelligence using prebuilt-read
    try:
        poller = di_client.begin_analyze_document("prebuilt-read", blob_content)
        result: AnalyzeResult = poller.result()
        raw_text = "\n".join([p.content for p in result.paragraphs]) if result.paragraphs else ""
        if not raw_text:
            logging.warning(f"No text extracted from {note_id}")
            raise ValueError("No text found in document")
        logging.info(f"Extracted raw text from {note_id}: {raw_text[:100]}...")
    except Exception as e:
        logging.error(f"Document Intelligence (prebuilt-read) failed: {str(e)}")
        raise
    
    # Define OpenAI prompt for intelligent entity extraction in JSON mode
    prompt = f"""
    You are an AI assistant processing job coach notes for disabled clients in a supported employment program. 
    These notes detail a shift's who, what, where, when, and why for stakeholder reports (e.g., government, employers). 
    Extract relevant entities dynamically (names, activities, locations, dates, purposes, etc.) from the text below. 
    Return a concise, objective JSON object, using lists for multiple values and 'Unknown' for unclear details. 
    Include 'json' for JSON mode.
    Text:
    {raw_text}
    """

    # Call OpenAI with JSON mode
    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_DEPLOYMENT,
            response_format={"type": "json_object"},  # Enable JSON mode
            messages=[
                {"role": "system", "content": "You are a precise entity extraction tool designed to output JSON for supported employment case notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,    # Low temperature for structured output
            max_tokens=10000    # Increased to handle complex notes
        )
        entities_json = response.choices[0].message.content.strip()
        entities = json.loads(entities_json)
        logging.info(f"Extracted entities for {note_id}: {json.dumps(entities, indent=2)}")
    except Exception as e:
        logging.error(f"OpenAI processing failed: {str(e)}")
        entities = {"error": "Failed to process with OpenAI", "raw_text": raw_text}
        logging.info(f"Fallback entities for {note_id}: {json.dumps(entities, indent=2)}")


    # # Generate and save reports
    # reports = {
    #     "government": generate_report(entities, "government_template.txt"),
    #     "employer": generate_report(entities, "employer_template.txt"),
    #     "team": generate_report(entities, "team_template.txt")
    # }
    # report_urls = {}
    # report_container = blob_service.get_container_client(f"{coach_id}/reports")
    # for stakeholder, report in reports.items():
    #     try:
    #         blob_client = report_container.upload_blob(f"{note_id}_{stakeholder}.txt", report, overwrite=True)
    #         report_urls[stakeholder] = blob_client.url
    #     except Exception as e:
    #         logging.error(f"Failed to upload {stakeholder} report: {str(e)}")
    #         raise

    # # Save metadata to Cosmos DB
    # metadata = {
    #     "id": note_id,
    #     "coach_id": coach_id,
    #     "entities": entities,
    #     "report_urls": report_urls,
    #     "timestamp": int(os.time())
    # }
    # try:
    #     container.upsert_item(metadata)
    #     logging.info(f"Successfully processed {note_id}")
    # except Exception as e:
    #     logging.error(f"Cosmos DB save failed: {str(e)}")
    #     raise