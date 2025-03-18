from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField

# Replace with your Azure details
service_endpoint = "https://<your-search-service>.search.windows.net"
api_key = "<your-api-key>"
index_name = "example-index"

# Create an index
def create_index():
    index_client = SearchIndexClient(endpoint=service_endpoint, credential=AzureKeyCredential(api_key))
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="content", type="Edm.String", analyzer_name="en.microsoft"),
    ]
    index = SearchIndex(name=index_name, fields=fields)
    index_client.create_index(index)
    print(f"Index '{index_name}' created.")

# Add documents to the index
def add_documents(documents):
    search_client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))
    result = search_client.upload_documents(documents=documents)
    print(f"Documents added: {result}")

# Query the index
def query_index(search_text):
    search_client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))
    results = search_client.search(search_text)
    for result in results:
        print(f"Found document: {result}")

if __name__ == "__main__":
    # Example usage
    create_index()
    documents = [
        {"id": "1", "content": "This is a sample document about OpenAI."},
        {"id": "2", "content": "Azure Cognitive Search is a powerful tool for indexing and querying data."},
    ]
    add_documents(documents)
    query_index("OpenAI")