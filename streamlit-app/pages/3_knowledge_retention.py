import streamlit as st
from utils import with_layout
from datetime import date
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access FUNCTION_TASKBREAKDOWN_URL from .env
FUNCTION_COSMOSDB_URL = os.getenv("FUNCTION_COSMOSDB_URL")
FUNCTION_SEARCH_INSIGHTS_URL = os.getenv("FUNCTION_SEARCH_INSIGHTS_URL")

def content():
    st.title("Knowledge Retention Tool")
    st.write("Search or contribute to the Azure Cosmos DB knowledge base.")

    # Search bar
    search_query = st.text_input("Search Insights (e.g., 'Safeway contact')")

    if search_query:
        # Prepare JSON payload
        payload = {"search_query": search_query}

        # Call Azure Function
        try:
            response = requests.post(FUNCTION_SEARCH_INSIGHTS_URL, json=payload)
            if response.status_code == 200:
                data = response.json
                search_results = data.get("search_results", [])
                message = data.get("message", "")

                # If results found
                if search_results:
                    st.success("Found relevant insights!")
                    for result in search_results:
                        st.markdown(f"**Category**: {result.get('category', 'N/A')}")
                        st.markdown(f"**Details**: {result.get('details', 'N/A')}")
                        st.markdown("---")  # Line separator between results
                else:
                    # No relevant data found
                    st.warning(message or "No relevant data found.")
            else:
                st.error(f"Failed to search Insights. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            st.error(f"Search Insights - An error occurred: {str(e)}")

    # Add new insight
    st.subheader("Add Insight")
    # Capture fields
    category = st.text_input("Category", placeholder="Enter category (e.g., 'Workplace', 'Task')")
    details = st.text_input("Details", placeholder="Enter details")
    

    # Submit button
    if st.button("Add Insights"):
        if category and details:
            # Prepare JSON payload
            payload = {
                "category": category,
                "details": details
            }

            # Call Azure Function
            try:
                response = requests.post(FUNCTION_COSMOSDB_URL, json=payload)
                if response.status_code == 200:
                    st.success("Insights saved successfully!")
                else:
                    st.error(f"Failed to save Insights. Status code: {response.status_code}, Response: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill out required fields: Employee Name and Task Details.")

with_layout(content)