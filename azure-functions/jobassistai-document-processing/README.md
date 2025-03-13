# JobAssistAI Document Processing Azure Function

## Overview

This Azure Function automates the processing of handwritten job coach notes for a supported employment program. It extracts text from uploaded documents, generates structured HTML reports using Azure OpenAI, converts them to professional PDF formats, and stores them in Azure Blob Storage. The function supports two report types: a **Job Support Compliance Report** for government agencies and an **Employee Progress Report** for employers, reducing administrative overhead for job coaches.

## Features

- **Text Extraction**: Uses Azure Document Intelligence to extract text from handwritten notes (TXT, PDF, PNG, etc.).
- **Report Generation**: Leverages Azure OpenAI (GPT-4o) to create structured HTML reports from raw text.
- **PDF Creation**: Converts HTML to styled PDFs using ReportLab, with bold headers and spaced fields.
- **Storage**: Uploads PDFs to Azure Blob Storage at `case-notes/processed/{client_name}_{report_type}_report.pdf`.
- **Modular Design**: Organized into reusable modules for configuration, clients, report generation, and PDF creation.

## Directory Structure
```
jobassistai-document-processing/
├── function_app.py      # Main entry point with the Azure Function
├── config.py            # Environment variables and configuration
├── clients.py           # Client initializations (Document Intelligence, Blob, OpenAI)
├── report_generator.py  # Logic for generating HTML reports with OpenAI
├── pdf_creator.py       # Logic for creating and uploading PDFs
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation (this file)
└── host.json            # Azure Functions configuration (auto-generated or customized)
```

## Prerequisites

- **Azure Subscription**: Access to Azure Blob Storage, Document Intelligence, and OpenAI services.
- **Python 3.12**: Compatible with Azure Functions Python runtime.
- **Azure Functions Core Tools**: For local testing and deployment.

## Usage

1. **Upload a Note**: Place a handwritten note in `case-notes/arriving-files/` in Blob Storage.
2. **Processing**:
   - The function extracts text using Document Intelligence.
   - OpenAI generates HTML for government and employer reports.
   - PDFs are created and uploaded to `case-notes/processed/`.
3. **Output**: PDFs are stored as `processed/{client_name}_{report_type}_report.pdf`.

## Dependencies

See `requirements.txt`:
- `azure-storage-blob>=12.19.0`
- `azure-ai-documentintelligence>=1.0.0`
- `azure-functions>=1.18.0`
- `openai>=1.0.0`
- `python-dotenv>=1.0.0`
- `reportlab>=4.2.0`