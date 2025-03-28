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

SEARCH_ENDPOINT = os.getenv("AISEARCH_CONNECTION_URI")
SEARCH_KEY = os.getenv("AISEARCH_CONNECTION_KEY")
SEARCH_INDEX = os.getenv("AISEARCH_INDEX_NAME")

with open("system_prompt_mapping.json", "r") as file:
    system_prompt_mapping = json.load(file)