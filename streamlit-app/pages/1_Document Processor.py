import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
import time
from io import BytesIO
from PyPDF2 import PdfReader

# Load environment variables from .env
load_dotenv()

# Fetch BLOB_CONNECTION_STRING from .env
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
if not BLOB_CONNECTION_STRING:
    st.error("BLOB_CONNECTION_STRING not found in .env file. Please configure it.")
    st.stop()

# Initialize Blob Service Client
blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)

# Custom CSS for responsiveness and styling
st.markdown("""
    <style>
    .main { padding: 10px; }
    .stButton>button { width: 100%; background-color: #0078d4; color: white; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #005a9e; }
    .stSpinner { text-align: center; }
    .report-expander { margin-bottom: 10px; }
    .preview-box { max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; }
    @media (max-width: 600px) {
        .stButton>button { font-size: 14px; }
        .report-expander { font-size: 14px; }
    }
    </style>
""", unsafe_allow_html=True)

# Page setup
st.title("JobAssist Document Processor")
st.subheader("Streamline Your Job Coach Reports")
st.write("Upload handwritten notes to generate professional PDF reports for government agencies and employers.")

# File uploader
uploaded_file = st.file_uploader("Choose a note file", type=["txt", "docx", "pdf", "png", "jpg"], key="file_uploader")

if uploaded_file:
    # Display file details
    st.write("**Uploaded File Details**")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Name: {uploaded_file.name}")
    with col2:
        st.write(f"Size: {uploaded_file.size / 1024:.2f} KB")

    # Upload and generate reports button
    if st.button("Upload & Generate Reports"):
        with st.spinner("Processing your note... Please wait"):
            # Upload to Blob Storage
            note_id = f"note_{int(time.time())}"
            container_client = blob_service.get_container_client("case-notes")
            blob_path = f"arriving-files/{note_id}_{uploaded_file.name}"
            try:
                blob_client = container_client.upload_blob(blob_path, uploaded_file.read(), overwrite=True)
                st.success(f"File uploaded to {blob_path}")
            except Exception as e:
                st.error(f"Upload failed: {str(e)}")
                st.stop()

            # Poll for processed reports
            max_attempts = 30  # Increased to 60 seconds total
            processed_prefix = "processed/"  # Broad search initially
            client_name = uploaded_file.name.split('.')[0].replace(' ', '_').lower()  # Fallback client_name
            for attempt in range(max_attempts):
                blobs = list(container_client.list_blobs(name_starts_with=processed_prefix))
                st.write(f"Attempt {attempt + 1}: Found {len(blobs)} blobs")  # Debugging
                
                # Look for government and employer reports with note_id or dynamic client_name
                gov_blob = next((b for b in blobs if "government_report.pdf" in b.name and note_id in b.name), None)
                emp_blob = next((b for b in blobs if "employer_report.pdf" in b.name and note_id in b.name), None)
                
                # If not found with note_id, try with client_name from file or content
                if not (gov_blob and emp_blob):
                    gov_blob = next((b for b in blobs if "government_report.pdf" in b.name), None)
                    emp_blob = next((b for b in blobs if "employer_report.pdf" in b.name), None)
                    if gov_blob:
                        client_name = gov_blob.name.split("processed/")[1].split("_government")[0]

                if gov_blob and emp_blob:
                    # Download PDFs
                    gov_pdf = container_client.download_blob(gov_blob.name).readall()
                    emp_pdf = container_client.download_blob(emp_blob.name).readall()
                    
                    st.success("Reports generated successfully!")
                    
                    # Government Report
                    with st.expander("Government Report", expanded=True):
                        st.write("**Job Support Compliance Report**")
                        col_preview, col_download = st.columns([2, 1])
                        with col_preview:
                            st.write("Preview:")
                            pdf_reader = PdfReader(BytesIO(gov_pdf))
                            preview_text = "\n".join([pdf_reader.pages[i].extract_text() for i in range(min(1, len(pdf_reader.pages)))])
                            st.markdown(f'<div class="preview-box">{preview_text}</div>', unsafe_allow_html=True)
                        with col_download:
                            st.download_button(
                                label="Download",
                                data=gov_pdf,
                                file_name="government_report.pdf",
                                mime="application/pdf"
                            )
                    
                    # Employer Report
                    with st.expander("Employer Report", expanded=True):
                        st.write("**Employee Progress Report**")
                        col_preview, col_download = st.columns([2, 1])
                        with col_preview:
                            st.write("Preview:")
                            pdf_reader = PdfReader(BytesIO(emp_pdf))
                            preview_text = "\n".join([pdf_reader.pages[i].extract_text() for i in range(min(1, len(pdf_reader.pages)))])
                            st.markdown(f'<div class="preview-box">{preview_text}</div>', unsafe_allow_html=True)
                        with col_download:
                            st.download_button(
                                label="Download",
                                data=emp_pdf,
                                file_name="employer_report.pdf",
                                mime="application/pdf"
                            )
                    break
                time.sleep(2)
            else:
                st.error("Processing timed out. Check Azure Function logs or try again.")
                st.write("Available blobs in 'processed/':")
                for blob in blobs:
                    st.write(f"- {blob.name}")

# Refresh button to check existing reports
if st.button("Refresh Processed Reports"):
    container_client = blob_service.get_container_client("case-notes")
    blobs = list(container_client.list_blobs(name_starts_with="processed/"))
    if blobs:
        st.write("**Available Reports**")
        for blob in blobs:
            st.write(f"- {blob.name}")
    else:
        st.info("No processed reports found.")

# Footer
st.markdown("---")
st.write("Powered by Azure Document Intelligence, OpenAI, and ReportLab | JobAssistAI © 2025")
st.write("Powered by Azure Document Intelligence, OpenAI, and ReportLab | JobAssistAI © 2025")