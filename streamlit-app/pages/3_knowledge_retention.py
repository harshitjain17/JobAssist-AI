import streamlit as st
from utils import with_layout
from datetime import date
import requests
import uuid
from dotenv import load_dotenv
import os
# Placeholder imports
# from azure.cosmos import CosmosClient
# from azure.search.documents import SearchClient

# Load environment variables
load_dotenv()

# Access FUNCTION_TASKBREAKDOWN_URL from .env
FUNCTION_COSMOSDB_URL = os.getenv("FUNCTION_COSMOSDB_URL")

def content():
    st.title("Knowledge Retention Tool")
    st.write("Search or contribute to the Azure Cosmos DB knowledge base.")

    # Search bar
    search_query = st.text_input("Search Insights (e.g., 'Safeway contact')")

    # Placeholder for Azure Cosmos DB connection
    # client = CosmosClient(AZURE_COSMOS_ENDPOINT, AZURE_COSMOS_KEY)
    # db = client.get_database_client("JobAssistDB")
    # container = db.get_container_client("KnowledgeBase")
    knowledge_base = {
        "Safeway Contact": "John Doe, Manager, 555-1234",
        "Task Strategy": "Use visual aids for employees with Down Syndrome."
    }

    if search_query:
        # Placeholder for Azure Search logic
        # search_client = SearchClient(AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_INDEX, AZURE_SEARCH_KEY)
        # results = search_client.search(search_query)
        results = [f"{key}: {value}" for key, value in knowledge_base.items() if search_query.lower() in key.lower()]
        if results:
            st.markdown("### Results")
            for result in results:
                st.write(result)
        else:
            st.write("No matches found.")

    # Add new insight
    st.subheader("Add Insight")
    # Capture fields
    employee_name = st.text_input("Employee Name", placeholder="Enter employee name to track progress")
    entry_date = st.date_input("Date", value=date.today())
    workplace = st.text_input("Workplace/Environment", placeholder="Context of employment")
    task_details = st.text_area("Task Details", placeholder="Describe the task being coached")
    challenges_faced = st.text_area("Challenges Faced", placeholder="Describe challenges faced during task")
    strategies_used = st.text_area("Strategies Used", placeholder="Describe strategies employed")
    outcome = st.text_area("Outcome/Progress", placeholder="Result of coaching session")
    future_recommendations = st.text_area("Future Recommendations", placeholder="Suggestions for next session")
    tags_input = st.text_input("Tags (comma-separated)", placeholder="e.g., communication, retail, visual aids")

    # Submit button
    if st.button("Add Insights"):
        if employee_name and task_details:
            # Prepare JSON data
            data = {
                "id": str(uuid.uuid4()),  # Unique ID
                "employeeName": employee_name,
                "date": str(entry_date),
                "workplace": workplace,
                "taskDetails": task_details,
                "challengesFaced": challenges_faced,
                "strategiesUsed": strategies_used,
                "outcome": outcome,
                "futureRecommendations": future_recommendations,
                "tags": [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            }

            # Call Azure Function
            try:
                response = requests.post(FUNCTION_COSMOSDB_URL, json=data)
                if response.status_code == 200:
                    st.success("Insights saved successfully!")
                else:
                    st.error(f"Failed to save Insights. Status code: {response.status_code}, Response: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill out required fields: Employee Name and Task Details.")

with_layout(content)