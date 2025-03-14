# function_app.py
# Description: Azure Function to process case notes and generate PDF reports.

import azure.functions as func
import logging
from clients import di_client
from azure.ai.documentintelligence.models import AnalyzeResult
from report_generator import generate_report
from pdf_creator import create_and_upload_pdf

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", source="EventGrid", path="case-notes/arriving-files/{name}", connection="jobassistaistorage_STORAGE")
def main(myblob: func.InputStream):
    """Process a blob trigger to generate and upload PDF reports."""
    logging.info(f"Blob trigger fired for: {myblob.name}")

    # Extract note_id from blob path
    try:
        note_id = myblob.name.split("/")[-1].split(".")[0]
    except IndexError:
        logging.error("Invalid blob path format")
        raise ValueError("Blob path must follow 'case-notes/arriving-files/{name}'")

    # Read blob content as raw bytes
    try:
        blob_content = myblob.read()
    except Exception as e:
        logging.error(f"Failed to read blob: {str(e)}")
        raise

    # Extract text with Document Intelligence
    try:
        poller = di_client.begin_analyze_document("prebuilt-read", blob_content)
        result: AnalyzeResult = poller.result()
        raw_text = "\n".join([p.content for p in result.paragraphs]) if result.paragraphs else ""
        if not raw_text:
            logging.warning(f"No text extracted from {note_id}")
            raise ValueError("No text found in document")
        logging.info(f"Extracted raw text from {note_id}: \n{raw_text}")
    except Exception as e:
        logging.error(f"Document Intelligence failed: {str(e)}")
        raise

    # Generate reports
    reports = {
        "government": generate_report(raw_text, "government"),
        "employer": generate_report(raw_text, "employer")
    }

    # Extract client_name from government report
    client_name = "unknown_client"
    try:
        for line in reports["government"].split("<br>"):
            if "<b>Client Name:</b>" in line:
                client_name = line.split("<b>Client Name:</b>")[1].strip().replace(" ", "_").lower()
                break
    except Exception as e:
        logging.warning(f"Could not extract client_name: {str(e)}")

    # Create and upload PDFs
    for report_type, html_content in reports.items():
        create_and_upload_pdf(html_content, report_type, client_name, note_id)

    logging.info(f"Successfully processed {note_id}")