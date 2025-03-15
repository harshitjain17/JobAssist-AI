import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from datetime import datetime


from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    SearchField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch,
    SearchIndex,
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters
)


class JobAssistIndexer():
    def __init__(self):

        load_dotenv()

        self.openi_endpoint = os.getenv("OPENAI_SERVICE_URI")
        self.openai_key = os.getenv("OPENAI_SERVICE_KEY")
        self.openai_version = os.getenv("OPENAI_SERVICE_VERSION")
        self.openai_model = os.getenv("CHAT_MODEL")

        self.search_endpoint = os.getenv("AISEARCH_CONNECTION_URI")
        self.search_key = os.getenv("AISEARCH_CONNECTION_KEY")
        self.search_index_name = os.getenv("AISEARCH_INDEX_NAME")

        self.OpenAIClient = AzureOpenAI(
            api_version=self.openai_version,
            azure_endpoint=self.openi_endpoint,
            api_key=self.openai_key,
        )
        self.SearchIndexClient = SearchIndexClient(
            endpoint=self.search_endpoint,
            credential=self.AzureKeyCredential(self.search_key),
        )
        
    def generate_doc_embeddings(self, doc, id=None, title=None, content=None, category=None):
        pass
    def generate_text_embeddings(self, doc, id=None, title=None, content=None, category=None):
        pass
    def update_search_index(self, index_name, model_name):
        # Define the embedding dimensions for Azure OpenAI model (typically 1536 for text-embedding-ada-002)
        azure_openai_embedding_dimensions = 1536

        index_fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
            SearchableField(name="title", type=SearchFieldDataType.String),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchableField(name="category", type=SearchFieldDataType.String,
                            filterable=True),
            SearchField(name="titleVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=azure_openai_embedding_dimensions, vector_search_profile_name="myHnswProfile"),
            SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=azure_openai_embedding_dimensions, vector_search_profile_name="myHnswProfile"),
        ]