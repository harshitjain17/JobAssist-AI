# config.py
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Environment variables
OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
OPENAI_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]

with open("system_prompt_mapping.json", "r") as file:
    system_prompt_mapping = json.load(file)