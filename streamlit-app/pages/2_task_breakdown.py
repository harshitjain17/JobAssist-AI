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
FUNCTION_HTTP_TEXT_TO_SPEECH_URL = os.getenv("FUNCTION_HTTP_TEXT_TO_SPEECH_URL")

def content():
    st.title("Task Breakdown Tool")
    st.write("Enter a task and employee details for Azure AI-generated instructions.")

    # Placeholder for response message from Azure Open AI
    if 'response_message' not in st.session_state:
        st.session_state.response_message = None  # Initialize message in session

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
                    st.session_state.response_message = response.json()['message']
                else:
                    st.error("Error: Could not get a response.")
                    st.session_state.response_message = None  # Clear message on failure
        else:
            st.error("Please enter a task and employee profile.")

    # If response message is received, show Generate Audio button
    if st.session_state.response_message:
        col1, col2 = st.columns([4, 1]) 
        with col1:
                st.success(f"Instructions generated successfully!\n\n{st.session_state.response_message}")
        with col2:
            if st.button("🎵 🔊 Generate Audio"):
                payload = {"text" : st.session_state.response_message}
                with st.spinner(f"Processing with Azure Text to Speech Service...") as spinner:
                    response = requests.post(FUNCTION_HTTP_TEXT_TO_SPEECH_URL, json=payload)
                    if response.status_code == 200:
                        audio_bytes = response.content  # Get the audio bytes
                        st.audio(audio_bytes, format='audio/mpeg')  # Play audio in Streamlit
                    else:
                        st.error("Error: Failed to generate audio.")

with_layout(content)