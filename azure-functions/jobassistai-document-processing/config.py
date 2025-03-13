# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
DI_ENDPOINT = os.environ["AZURE_DI_ENDPOINT"]
DI_KEY = os.environ["AZURE_DI_KEY"]
BLOB_CONNECTION = os.environ["BLOB_CONNECTION_STRING"]
OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
OPENAI_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]