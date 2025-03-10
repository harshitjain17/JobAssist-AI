import streamlit as st

# Set page config for a modern look
st.set_page_config(page_title="JobAssist AI", layout="wide", initial_sidebar_state="expanded")

# Title and intro
st.title("JobAssist AI")
st.write("Your Azure-powered companion for supported employment. Navigate using the sidebar to access AI-driven tools built on Azure services.")

# Sidebar
st.sidebar.header("JobAssist Tools")
st.sidebar.write("Select a tool below, powered by Azure:")

# Landing page content
st.subheader("How It Works")
st.write("""
- **Administrative Overload**: Automate reports with Azure Cognitive Services.
- **Task Breakdown**: Generate instructions using Azure AI.
- **Knowledge Retention**: Access insights via Azure Cosmos DB.
- **Caseload Tracking**: Monitor progress with Azure Machine Learning.
""")
st.write("Built entirely on Azure for seamless integration and scalability.")