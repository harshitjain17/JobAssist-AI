# Description: Azure Function to process case notes and generate PDF reports.

import azure.functions as func
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
import os
import logging
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io

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

@app.blob_trigger(arg_name="myblob", path="case-notes/arriving-files/{name}", connection="jobassistaistorage_STORAGE")
def main(myblob: func.InputStream):
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

    # Prompts for OpenAI to generate HTML reports
    government_prompt = f"""
    From the text below, generate an HTML report using this template. Fill fields based on relevance, using 'Unknown' for missing details. Only include text in 'Compliance Notes' if it specifically relates to compliance or regulatory observations; otherwise, leave it 'Unknown'. Use <b> tags for field names and <br> for line breaks. Do not wrap the output in code blocks (e.g., ```html).
    Template:
    <b>Job Support Compliance Report (to Government Agencies)</b><br>
    <b>Date:</b> <br>
    <b>Client Name:</b> <br>
    <b>Supervisor/Coach Name:</b> <br>
    <b>Disability:</b> <br>
    <b>Location:</b> <br>
    <b>Purpose:</b> <br>
    <b>Activity:</b> <br>
    <b>Support Provided:</b> <br>
    <b>Challenges Faced:</b> <br>
    <b>Follow-Up Actions Required:</b> <br>
    <b>Next Scheduled Check-In:</b> <br>
    <b>Compliance Notes:</b> <br>
    <b>State-Specific Regulations Applied:</b> <br>

    Text: 
    {raw_text}
    """

    employer_prompt = f"""
    From the text below, generate an HTML report using this template. Fill fields based on relevance, using 'Unknown' for missing details. Only include text in 'Additional Notes' if it provides relevant extra context beyond other fields; otherwise, leave it 'Unknown'. Use <b> tags for field names and <br> for line breaks. Do not wrap the output in code blocks (e.g., ```html).
    Template:
    <b>Employee Progress Report (to Employer)</b><br>
    <b>Date:</b> <br>
    <b>Employee Name:</b> <br>
    <b>Supervisor/Coach Name:</b> <br>
    <b>Disability:</b> <br>
    <b>Activity Performed:</b> <br>
    <b>Performance Summary:</b> <br>
    <b>Job Readiness Skills Observed:</b> <br>
    <b>Areas for Improvement:</b> <br>
    <b>Employee Satisfaction Feedback:</b> <br>
    <b>Additional Notes:</b> <br>

    Text: 
    {raw_text}
    """

    # Generate reports one by one
    reports = {}
    for report_type, prompt in [("government", government_prompt), ("employer", employer_prompt)]:
        try:
            response = openai_client.chat.completions.create(
                model=OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are a precise report generator outputting HTML for job coach notes for a supported employment program."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            reports[report_type] = response.choices[0].message.content.strip()
            logging.info(f"Generated {report_type} report for {note_id}")
        except Exception as e:
            logging.error(f"OpenAI failed for {report_type} report: {str(e)}")
            reports[report_type] = "<b>Error</b><br>Failed to generate {report_type} report."

    # Extract client_name from government report
    client_name = "unknown_client"
    try:
        for line in reports["government"].split("<br>"):
            if "<b>Client Name:</b>" in line:
                client_name = line.split("<b>Client Name:</b>")[1].strip().replace(" ", "_").lower()
                break
    except Exception as e:
        logging.warning(f"Could not extract client_name: {str(e)}")

    # Convert HTML to PDF using reportlab and upload to Blob Storage
    processed_container = blob_service.get_container_client("case-notes")
    styles = getSampleStyleSheet()
    header_style = styles["Heading1"]
    header_style.fontSize = 16
    header_style.textColor = colors.darkblue
    field_style = styles["BodyText"]
    field_style.fontSize = 12
    field_style.leading = 16  # Line spacing

    for report_type, html_content in reports.items():
        try:
            # Create PDF in memory
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=letter,
                title=f"{report_type.capitalize()} Report - {client_name}"
            )
            story = []
            lines = [line.strip() for line in html_content.split("<br>") if line.strip()]
            
            # First line is the header
            header = lines[0].replace("<b>", "").replace("</b>", "")
            story.append(Paragraph(header, header_style))
            story.append(Spacer(1, 12))  # Space after header
            
            # Remaining lines are fields
            for line in lines[1:]:
                if "<b>" in line:
                    field_name = line.split("<b>")[1].split("</b>")[0]
                    field_value = line.split("</b>")[1].strip()
                    story.append(Paragraph(f"<b>{field_name}</b> {field_value}", field_style))
                else:
                    story.append(Paragraph(line, field_style))
                story.append(Spacer(1, 6))  # Space between fields
            
            doc.build(story)
            
            # Get PDF bytes
            pdf_content = pdf_buffer.getvalue()
            pdf_buffer.close()
            
            # Upload to Blob Storage
            blob_path = f"processed/{client_name}_{report_type}_report.pdf"
            blob_client = processed_container.upload_blob(blob_path, pdf_content, overwrite=True)
            logging.info(f"Uploaded {report_type} report to {blob_path}: {blob_client.url}")
        except Exception as e:
            logging.error(f"Failed to generate/upload {report_type} PDF: {str(e)}")
            raise

    logging.info(f"Successfully processed {note_id}")