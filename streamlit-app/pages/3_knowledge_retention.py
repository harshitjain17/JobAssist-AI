import streamlit as st
from utils import with_layout
from datetime import date
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access FUNCTION_HTTP_OPENAI_URL from .env
FUNCTION_COSMOSDB_URL = os.getenv("FUNCTION_COSMOSDB_URL")
FUNCTION_SEARCH_INSIGHTS_URL = os.getenv("FUNCTION_SEARCH_INSIGHTS_URL")
FUNCTION_HTTP_OPENAI_URL = os.getenv("FUNCTION_HTTP_OPENAI_URL")
SYSTEM_ROLE_SEARCH_INSIGHTS = os.getenv("SYSTEM_ROLE_SEARCH_INSIGHTS")

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
                data = response.json()
                search_results = data.get("search_results", [])
                message = data.get("message", "")

                # If results found
                if search_results:
                    category = search_results[0].get('category', '')
                    details = search_results[0].get('details', '')
                    if category and details:
                        user_prompt = f"Search query: {search_query} got the results with category: {category} and details: {details}"

                        # Prepare the payload
                        payload = {"system_role" : SYSTEM_ROLE_SEARCH_INSIGHTS, "user_prompt" : user_prompt}

                        with st.spinner("Processing with Azure AI...") as spinner:
                            # Make POST request to Azure Function
                            response = requests.post(FUNCTION_HTTP_OPENAI_URL, json=payload)
                            
                            # Display the AI response
                            if response.status_code == 200:
                                response_message = response.json()['message']
                                st.success(f"{response_message}")
                            else:
                                st.error("Error: Could not get a response from Azure Open AI.")
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