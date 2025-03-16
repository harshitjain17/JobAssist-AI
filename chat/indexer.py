import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from datetime import datetime

from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
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
    AzureOpenAIVectorizerParameters,
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SplitSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    AzureOpenAIEmbeddingSkill,
    OcrSkill,
    SearchIndexerIndexProjection,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    IndexProjectionMode,
    SearchIndexerSkillset,
    AIServicesAccountKey,
    AIServicesAccountIdentity,
    DocumentIntelligenceLayoutSkill    
)
from azure.search.documents.indexes.models import NativeBlobSoftDeleteDeletionDetectionPolicy

class JobAssistIndexer():
    def __init__(self):

        load_dotenv()

        self.openi_endpoint = os.getenv("OPENAI_SERVICE_URI")
        self.openai_key = os.getenv("OPENAI_SERVICE_KEY")
        self.openai_version = os.getenv("OPENAI_SERVICE_VERSION")
        self.openai_model = os.getenv("CHAT_MODEL")

        self.search_endpoint = os.getenv("AISEARCH_CONNECTION_URI")
        self.search_key = os.getenv("AISEARCH_CONNECTION_KEY")
        # self.search_index_name = os.getenv("AISEARCH_INDEX_NAME")
        self.search_index_name = os.getenv("AISEARCH_INDEX_CASEDOCS_NAME")
        self.search_key_credential = AzureKeyCredential(self.search_key)

        self.blob_container_name = os.getenv("BLOB_CONTAINER_NAME")
        self.blob_connection_string = os.getenv("BLOB_CONNECTION_STRING")

        self.openai_embeddings_model = os.getenv("OPENAI_EMBEDDINGS_MODEL")
        self.openai_embeddings_deployment = os.getenv("OPENAI_EMBEDDINGS_DEPLOYMENT")
        self.openai_embeddings_dimensions = os.getenv("OPENAI_EMBEDDINGS_DIMENSIONS")

        self.OpenAIClient = AzureOpenAI(
            api_version=self.openai_version,
            azure_endpoint=self.openi_endpoint,
            api_key=self.openai_key,
        )
        self.SearchIndexClient = SearchIndexClient(
            endpoint=self.search_endpoint,
            credential=self.search_key_credential,
        )
        
    def generate_doc_embeddings(self, doc, id=None, title=None, content=None, category=None):
        pass
    def generate_text_embeddings(self, doc, id=None, title=None, content=None, category=None):
        pass
    def create_search_indexer(self):
        # Create a data source 
        self.SearchIndexerClient = SearchIndexerClient(self.search_endpoint, self.search_key_credential)
        container = SearchIndexerDataContainer(name=self.blob_container_name)
        data_source_connection = SearchIndexerDataSourceConnection(
            name=f"{self.search_index_name}-blob",
            type="azureblob",
            connection_string=self.blob_connection_string,
            container=container,
            data_deletion_detection_policy=NativeBlobSoftDeleteDeletionDetectionPolicy()
        )
        data_source = self.SearchIndexerClient.create_or_update_data_source_connection(data_source_connection)

    def create_search_index(self, index_name, model_name, 
                            search_dimensions=1536, 
                            add_page_numbers=False, 
                            use_document_layout=False):        
        # index_fields = [
        #     SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
        #     SearchableField(name="title", type=SearchFieldDataType.String),
        #     SearchableField(name="content", type=SearchFieldDataType.String),
        #     SearchableField(name="category", type=SearchFieldDataType.String,filterable=True),
        #     SearchField(name="titleVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        #                 searchable=True, vector_search_dimensions=search_dimensions, vector_search_profile_name="hnsw-profile"),
        #     SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        #                 searchable=True, vector_search_dimensions=search_dimensions, vector_search_profile_name="hnsw-profile"),
        # ]
        index_fields = [
            SearchField(name="parent_id", type=SearchFieldDataType.String, sortable=True, filterable=True, facetable=True),  
            SearchField(name="title", type=SearchFieldDataType.String),  
            SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
            SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),  
            SearchField(name="vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=self.openai_embeddings_dimensions, vector_search_profile_name="hnsw-profile"),  
        ]
        if add_page_numbers:
            index_fields.append(
                SearchField(name="page_number", type=SearchFieldDataType.String, sortable=True, filterable=True, facetable=False)
            )

        if use_document_layout:
            index_fields.extend([
                SearchField(name="header_1", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),
                SearchField(name="header_2", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),
                SearchField(name="header_3", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False)
            ])

        # Configure the vector search configuration  
        vector_search = VectorSearch(  
            algorithms=[  
                HnswAlgorithmConfiguration(name="hnsw-profile"),
            ],  
            profiles=[  
                VectorSearchProfile(  
                    name="hnsw-profile",  
                    algorithm_configuration_name="hnsw-config",  
                    vectorizer_name="openai-vectorizer",  
                )
            ],  
            vectorizers=[  
                AzureOpenAIVectorizer(  
                    vectorizer_name="openai-vectorizer",  
                    kind="azureOpenAI",  
                    parameters=AzureOpenAIVectorizerParameters(  
                        resource_url=self.openi_endpoint,  
                        deployment_name=self.openai_embeddings_deployment,
                        model_name=self.openai_embeddings_model,
                        api_key=self.openai_key,
                    ),
                ),  
            ],  
        )  
        
        semantic_config = SemanticConfiguration(  
            name="semantic-config",  
            prioritized_fields=SemanticPrioritizedFields(  
                content_fields=[SemanticField(field_name="chunk")],
                title_field=SemanticField(field_name="title")
            ),  
        )
        
        # Create the semantic search with the configuration  
        semantic_search = SemanticSearch(configurations=[semantic_config])  
        
        # Create the search index
        index = SearchIndex(name=index_name, fields=index_fields, vector_search=vector_search, semantic_search=semantic_search)  
        result = self.SearchIndexClient.create_or_update_index(index)

    def update_search_index(self, index_name, model_name):
        pass

    def create_skillset(self, skillset_name, index_name):
        split_skill = SplitSkill(  
            description="Split skill to chunk documents",  
            text_split_mode="pages",  
            context="/document",  
            maximum_page_length=2000,  
            page_overlap_length=500,  
            inputs=[  
                InputFieldMappingEntry(name="text", source="/document/content"),  
            ],  
            outputs=[  
                OutputFieldMappingEntry(name="textItems", target_name="pages")  
            ]
        )

        embedding_skill = AzureOpenAIEmbeddingSkill(  
            description="Skill to generate embeddings via Azure OpenAI",  
            context="/document/pages/*",  
            resource_url=self.openi_endpoint,  
            deployment_name=self.openai_embeddings_deployment,  
            model_name=self.openai_embeddings_model,
            dimensions=self.openai_embeddings_dimensions,
            api_key=self.openai_key,  
            inputs=[  
                InputFieldMappingEntry(name="text", source="/document/pages/*"),  
            ],  
            outputs=[
                OutputFieldMappingEntry(name="embedding", target_name="vector")  
            ]
        )

        index_projections = SearchIndexerIndexProjection(  
            selectors=[  
                SearchIndexerIndexProjectionSelector(  
                    target_index_name=index_name,  
                    parent_key_field_name="parent_id",  
                    source_context="/document/pages/*",  
                    mappings=[
                        InputFieldMappingEntry(name="chunk", source="/document/pages/*"),  
                        InputFieldMappingEntry(name="vector", source="/document/pages/*/vector"),
                        InputFieldMappingEntry(name="title", source="/document/metadata_storage_name")
                    ]
                )
            ],  
            parameters=SearchIndexerIndexProjectionsParameters(  
                projection_mode=IndexProjectionMode.SKIP_INDEXING_PARENT_DOCUMENTS  
            )  
        )

        skills = [split_skill, embedding_skill]

        return SearchIndexerSkillset(  
            name=skillset_name,  
            description="Skillset to chunk documents and generating embeddings",  
            skills=skills,  
            index_projection=index_projections
        )