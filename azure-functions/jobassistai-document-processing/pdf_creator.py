# pdf_creator.py
import io
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from clients import blob_service

def create_and_upload_pdf(html_content, report_type, client_name, note_id):
    """Create a PDF from HTML content and upload it to Blob Storage."""
    processed_container = blob_service.get_container_client("case-notes")
    styles = getSampleStyleSheet()
    header_style = styles["Heading1"]
    header_style.fontSize = 16
    header_style.textColor = colors.darkblue
    field_style = styles["BodyText"]
    field_style.fontSize = 12
    field_style.leading = 16  # Line spacing

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