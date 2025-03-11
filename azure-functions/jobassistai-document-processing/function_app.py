# Description: Azure Function to process case notes and generate reports.

import azure.functions as func
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
import os
import re
import logging
from dotenv import load_dotenv
load_dotenv()

app = func.FunctionApp()

# Environment variables (set in Function App settings)
DI_ENDPOINT = os.environ["AZURE_DI_ENDPOINT"]
DI_KEY = os.environ["AZURE_DI_KEY"]
BLOB_CONNECTION = os.environ["BLOB_CONNECTION_STRING"]
# COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
# COSMOS_KEY = os.environ["COSMOS_KEY"]

# Clients
di_client = DocumentIntelligenceClient(DI_ENDPOINT, AzureKeyCredential(DI_KEY))
blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION)
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
    
    # Extract entities intelligently
    entities = {
        "raw_text": "",  # Full extracted text
        "names": [],     # Potential employee names
        "dates": [],     # Detected dates
        "progress": []   # General text chunks as progress notes
    }

    # Aggregate all text from paragraphs
    if result.paragraphs:
        entities["raw_text"] = "\n".join([p.content for p in result.paragraphs])

    # Extract entities from DI output
    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            key = kvp.key.content if kvp.key else "Unknown"
            value = kvp.value.content if kvp.value else "Unknown"
            # Heuristic: Look for common entity types
            if "name" in key.lower() or "employee" in key.lower():
                entities["names"].append(value)
            elif "date" in key.lower():
                entities["dates"].append(value)
            elif "progress" in key.lower() or "notes" in key.lower():
                entities["progress"].append(value)

    # Fallback: Extract from raw text if no key-value pairs
    if not entities["names"] or not entities["dates"]:
        text = entities["raw_text"]
        # Simple regex for dates (e.g., MM/DD/YY or MM-DD-YYYY)
        dates = re.findall(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text)
        entities["dates"].extend(dates)
        # Names: Look for capitalized words (crude heuristic)
        names = re.findall(r"\b[A-Z][a-z]+\b(?:\s[A-Z][a-z]+\b)?", text)
        entities["names"].extend([n for n in names if n not in entities["dates"]])
        # Progress: Use remaining text chunks
        if not entities["progress"]:
            entities["progress"].append(text.strip())

    # Log extracted entities for now
    logging.info(f"Extracted entities for {note_id}: {entities}")



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