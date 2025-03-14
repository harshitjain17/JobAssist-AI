import streamlit as st
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import time
from io import BytesIO

# Load environment variables from .env
load_dotenv()

# Fetch BLOB_CONNECTION_STRING from .env
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
if not BLOB_CONNECTION_STRING:
    st.error("BLOB_CONNECTION_STRING not found in .env file. Please configure it.")
    st.stop()

# Initialize Blob Service Client
blob_service = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)

# Custom CSS for professional and responsive design
st.markdown("""
    <style>
    /* Container for centered content */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    /* Button styling */
    .stButton>button {
        width: 200px;
        background-color: #28a745;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #218838;
    }
    /* File uploader and text */
    .stFileUploader, .stText {
        font-family: 'Arial', sans-serif;
        color: #333333;
    }
    /* Expander styling */
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    /* Spinner alignment */
    .stSpinner {
        text-align: center;
        color: #666666;
    }
    /* Responsive adjustments */
    @media (max-width: 600px) {
        .main-container {
            padding: 10px;
        }
        .stButton>button {
            width: 150px;
            font-size: 14px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'reports_generated' not in st.session_state:
    st.session_state.reports_generated = False
if 'gov_pdf' not in st.session_state:
    st.session_state.gov_pdf = None
if 'emp_pdf' not in st.session_state:
    st.session_state.emp_pdf = None

# Page setup with container
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("JobAssist Document Processor")
st.subheader("Streamline Job Coach Reporting")
st.write("Upload a handwritten note to generate professional PDF reports for government agencies and employers.")

# File uploader
uploaded_file = st.file_uploader("Select a Note File", type=["txt", "docx", "pdf", "png", "jpg"], key="file_uploader")
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file

# Use session state file if available
current_file = st.session_state.uploaded_file

if current_file:
    # File details
    st.write("**File Details**")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Name: {current_file.name}")
    with col2:
        st.write(f"Size: {current_file.size / 1024:.2f} KB")

    # Generate reports button (only if reports not yet generated)
    if not st.session_state.reports_generated and st.button("Generate Reports"):
        with st.spinner("Generating reports..."):
            # Upload to Blob Storage
            note_id = f"note_{int(time.time())}"
            container_client = blob_service.get_container_client("case-notes")
            blob_path = f"arriving-files/{note_id}_{current_file.name}"
            try:
                container_client.upload_blob(blob_path, current_file.read(), overwrite=True)
            except Exception as e:
                st.error(f"Upload failed: {str(e)}")
                st.stop()

            # Poll for processed reports
            max_attempts = 30  # 60 seconds total
            processed_prefix = "processed/"
            client_name = current_file.name.split('.')[0].replace(' ', '_').lower()  # Fallback
            for attempt in range(max_attempts):
                blobs = list(container_client.list_blobs(name_starts_with=processed_prefix))
                gov_blob = next((b for b in blobs if "government_report.pdf" in b.name and note_id in b.name), None)
                emp_blob = next((b for b in blobs if "employer_report.pdf" in b.name and note_id in b.name), None)
                
                if not (gov_blob and emp_blob):
                    gov_blob = next((b for b in blobs if "government_report.pdf" in b.name), None)
                    emp_blob = next((b for b in blobs if "employer_report.pdf" in b.name), None)
                    if gov_blob:
                        client_name = gov_blob.name.split("processed/")[1].split("_government")[0]

                if gov_blob and emp_blob:
                    # Download PDFs and store in session state
                    st.session_state.gov_pdf = container_client.download_blob(gov_blob.name).readall()
                    st.session_state.emp_pdf = container_client.download_blob(emp_blob.name).readall()
                    st.session_state.reports_generated = True
                    st.success("Reports generated successfully!")
                    break
                time.sleep(2)
            else:
                st.error("Processing timed out. Please check the Azure Function logs or try again.")

    # Show download options if reports are generated
    if st.session_state.reports_generated:
        with st.expander("Job Support Compliance Report", expanded=True):
            st.download_button(
                label="Download Government Report",
                data=st.session_state.gov_pdf,
                file_name="government_report.pdf",
                mime="application/pdf",
                key="gov_download"
            )
        
        with st.expander("Employee Progress Report", expanded=True):
            st.download_button(
                label="Download Employer Report",
                data=st.session_state.emp_pdf,
                file_name="employer_report.pdf",
                mime="application/pdf",
                key="emp_download"
            )

# Close container div
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.write("Powered by Azure | JobAssistAI © 2025")