# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
SPEECH_KEY = os.environ["AZURE_SPEECH_KEY"]
SERVICE_REGION = os.environ["AZURE_SPEECH_SERVICE_REGION"]