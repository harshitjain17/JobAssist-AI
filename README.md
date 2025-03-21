# JobAssist AI  
**Empowering Coaches, Transforming Lives**  

[![Deployed on Azure](https://img.shields.io/badge/Deployed%20on-Azure-blue?logo=microsoft-azure)](https://jobassistai-dhbzhtbxerdwedhh.eastus2-01.azurewebsites.net/)  
*Built for the Microsoft Innovation Challenge, March 2025*  

---

## 🚀 What is JobAssist AI?  

**JobAssist AI** is an innovative application crafted to enhance the productivity of job coaches in supported employment programs for individuals with disabilities, including those with intellectual, developmental, or physical challenges. Built entirely on **Microsoft Azure**, this solution optimizes workflows, delivers personalized support, and promotes independence for clients. 

By facilitating job matching in sectors such as retail, healthcare, IT, and manufacturing, automating report generation, and simplifying task breakdowns, JobAssist AI alleviates administrative burdens, enabling coaches to prioritize their core mission: empowering people.

Developed as part of the **Microsoft Innovation Challenge in March 2025**, this Flask-based application harnesses Azure's advanced AI and cloud capabilities to address pressing real-world challenges. JobAssist AI reflects a commitment to inclusion, transforming it from an aspiration into actionable impact.

**[Try it live here!](https://jobassistai-dhbzhtbxerdwedhh.eastus2-01.azurewebsites.net/)**  

---

## 🌟 The Problem We’re Solving  

Job coaches play a vital role, yet they face significant obstacles that hinder their effectiveness:  
- **Paperwork Overload:** Hours spent reformatting notes into reports for government agencies and employers.  
- **Personalized Guidance Gaps:** Crafting tailored task instructions for unique needs is slow and inconsistent.  
- **Lost Knowledge:** Insights vanish when coaches leave, leaving new hires scrambling.  
- **Bureaucratic Maze:** Navigating fragmented resources and guidelines steals time from coaching.

JobAssist AI redefines this landscape by automating repetitive tasks, centralizing expertise, and providing tailored support through a unified Azure-powered platform.

---

## ✨ Key Features  

### 1. AI Assistant  
- **What**: Real-time answers to compliance questions.  
- **How**: Azure AI Search and OpenAI analyze stored guidelines in Blob Storage.
- **Impact**: Minimizes administrative stress, keeping the focus on clients.

### 2. Automated Documentation  
- **What:** Upload notes, receive polished reports.  
- **How:** Azure AI Document Intelligence extracts text, Azure OpenAI (GPT-4o) crafts HTML reports, and PDFs are stored in Blob Storage.  
- **Impact:** Reduces paperwork time significantly, freeing coaches for client advocacy.

### 3. Centralized Knowledge Base  
- **What:** A comprehensive repository of strategies and contacts.  
- **How:** Coaches log insights into Azure Cosmos DB; Azure AI Search enables instant retrieval.  
- **Impact:** Preserves expertise, even as team members change.

### 4. Personalized Task Guidance  
- **What:** Detailed, step-by-step task guides customized for each client.  
- **How:** Azure OpenAI generates instructions; Azure Speech Services provides audio for accessibility.  
- **Impact:** Ensures consistent, client-specific support with minimal effort.

---

## 🛠️ Technical Architecture  

JobAssist AI integrates a robust set of Azure services with a Flask frontend:

- **Azure AI Document Intelligence**: Text extraction from notes.  
- **Azure OpenAI (GPT-4o)**: Report generation and task breakdowns.  
- **Azure Blob Storage**: Secure file storage with versioning.  
- **Azure Cosmos DB**: Scalable knowledge base.  
- **Azure AI Search**: Rapid data retrieval.  
- **Azure Speech Services**: Text-to-speech for accessibility.  
- **Azure Functions**: Workflow automation.
- **Azure Key Vault**: Secures sensitive credentials.

### System Architecture Diagram  
![JobAssist AI System Architecture](path/to/system-architecture.png)

---

## 📂 Project Structure  
```
JobAssistAI/
├── azure-functions/                       # Azure Functions for AI features
│   ├── jobassistai-document-processing/   # Auto-generates reports from notes
│   ├── jobassistai-http-trigger-openai/   # OpenAI-powered responses
│   ├── jobassistai-http-trigger-tts/      # Text-to-speech for task guides
│   ├── jobassistai-save-insights/         # [Placeholder: Details TBD]
│   ├── jobassistai-save-voice-insights/   # [Placeholder: Details TBD]
│   ├── jobassistai-search-insights/       # [Placeholder: Details TBD]
├── docs/                                  # Documentation
│   └── Microsoft-RAI-Impact-Assessment-JobAssistAI.pdf
├── onedrive/                              # OneDrive integration
│   └── onedrive_manager.py
├── static/                                # Frontend assets
│   ├── css/
│   └── js/
├── templates/                             # Flask HTML templates
│   ├── base.html
│   ├── consumer_detail.html
│   ├── dashboard.html
│   ├── knowledge_base.html
│   └── login.html
├── app.py                                 # Main Flask application
├── requirements.txt                       # Python dependencies
└── README.md                              # You’re here!
```

---

## 🔧 Azure Functions Deep Dive  

### `jobassistai-document-processing`  
**Purpose**: Turns handwritten notes into polished PDFs.  
- **Flow**: Extracts text → Generates HTML reports → Converts to PDF → Stores in Blob Storage.  
- **Diagram**: *[Insert architecture diagram here]*  
- **Details**: See [its README](azure-functions/jobassistai-document-processing/README.md).  

### `jobassistai-http-trigger-openai`  
**Purpose**: Powers AI responses with OpenAI + optional Azure Search citations.  
- **Flow**: Takes user prompts → Fetches system prompts → Returns JSON responses.  
- **Diagram**: *[Insert architecture diagram here]*  
- **Details**: See [its README](azure-functions/jobassistai-http-trigger-openai/README.md).  

### `jobassistai-http-trigger-tts`  
**Purpose**: Converts text instructions to audio with Azure SpeechSDK.  
- **Flow**: Accepts JSON text → Outputs MP3 audio.  
- **Diagram**: *[Insert architecture diagram here]*  
- **Details**: See [its README](azure-functions/jobassistai-http-trigger-tts/README.md).  

*More functions (`save-insights`, `save-voice-insights`, `search-insights`) coming soon!*  

---

## 🌍 Responsible AI  

We’re committed to ethical AI. For a detailed look at how JobAssist AI upholds responsible AI principles, check out our [Responsible AI Impact Assessment](docs/Microsoft-RAI-Impact-Assessment-JobAssistAI.pdf). 

---

## ⚙️ Setup & Installation  

### Prerequisites  
- **Azure Subscription**: Access to Blob Storage, Cosmos DB, OpenAI, Speech Services, and more.  
- **Python 3.12**: For Flask and Azure Functions.  
- **Azure Functions Core Tools**: For local testing.  
- **Git**: To clone this repo.  

### Steps  
1. **Clone the Repo**  
   ```bash
   git clone https://github.com/yourusername/jobassistai.git
   cd jobassistai
2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
4. **Configure Environment Variables**
   Create a .env file in the root directory:
   ```bash
   AZURE_STORAGE_CONNECTION_STRING="your_connection_string"
   AZURE_OPENAI_KEY="your_openai_key"
   AZURE_COSMOS_ENDPOINT="your_cosmos_endpoint"
   AZURE_SEARCH_KEY="your_search_key"
5. **Run Locally**
   ```bash
   python app.py  # Flask app
   func start     # Azure Functions (from azure-functions/)
## 📜 License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use, modify, and share!

## 🙌 Acknowledgements
This project was developed by the following team members:
- **Harshit Jain**
- **Joshua Kaelin**
- **Srujana Vanama**

