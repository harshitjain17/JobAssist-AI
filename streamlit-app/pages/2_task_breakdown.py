import streamlit as st
import requests
from dotenv import load_dotenv
import os
from utils import with_layout

# Load environment variables
load_dotenv()

# Access FUNCTION_TASKBREAKDOWN_URL from .env
FUNCTION_TASKBREAKDOWN_URL = os.getenv("FUNCTION_TASKBREAKDOWN_URL")
SYSTEM_ROLE_TASKBREAKDOWN = os.getenv("SYSTEM_ROLE_TASKBREAKDOWN")

def content():
    st.title("Task Breakdown Tool")
    st.write("Enter a task and employee details for Azure AI-generated instructions.")

    # Input fields
    task = st.text_input("Task (e.g., 'Fold pizza boxes')")
    disability_type = st.text_input("Disability Type (e.g., 'Down Syndrome or Autism')")
    employee_info = st.text_area("Employee Profile (e.g., name, job role)")

    # Generate breakdown button
    if st.button("Generate Instructions"):
        if task and employee_info:
            user_prompt = f"Task to complete: {task}\n" + (f"Employee has disability: {disability_type}\n" if disability_type else "") + f"Employee Info: {employee_info}"

            # Prepare the payload
            payload = {"system_role" : SYSTEM_ROLE_TASKBREAKDOWN, "user_prompt" : user_prompt}

            with st.spinner("Processing with Azure AI...") as spinner:
                # Make POST request to Azure Function
                response = requests.post(FUNCTION_TASKBREAKDOWN_URL, json=payload)
                
                # Display the AI response
                if response.status_code == 200:
                    st.success("Instructions generated successfully!")
                    st.success(response.json()['message'])
                else:
                    st.error("Error: Could not get a response.")
        else:
            st.error("Please enter a task and employee profile.")

with_layout(content)