import azure.functions as func
import logging
import requests
import json
from clients import openai_client, AZURE_SEARCH_URL, azure_search_headers
from config import TEXT_EMBEDDING_MODEL

app = func.FunctionApp()

@app.route(route="search_insights")
def search_insights(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the JSON data from the incoming request
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    search_query = req_body.get('search_query')
    logging.info(f"Search query: {search_query}")

    if search_query:
        try:
            search_query_vector_response = openai_client.embeddings.create(
                input = search_query,
                model= TEXT_EMBEDDING_MODEL
            )
            search_query_vector = search_query_vector_response.data[0].embedding
            
            try:
                payload = {
                    "vector": {
                        "value": search_query_vector,
                        "fields": "detailsVector",
                        "k": 5  # Return only the top 1 best match
                    }
                }

                response = requests.post(AZURE_SEARCH_URL, json=payload, headers=azure_search_headers)
                logging.info(f"Azure AI Search response: {response.json()}")
                results = response.json().get("value", [])
                logging.info(f"Search results: {results}")
                message = "No relevant data found." if not results else "Success"

                return func.HttpResponse(
                    json.dumps({"search_results": results, "message": message}),
                    status_code=200,
                    mimetype="application/json")
            except Exception as e:
                return func.HttpResponse(f"Search Insight - Azure AI Search Error: {str(e)}", status_code=500)
        
        except Exception as e:
            return func.HttpResponse(f"Search Insight - OpenAI Embedding Error: {str(e)}", status_code=500)
    else:
        return func.HttpResponse(
             "Please provide a search query to retrieve insights.",status_code=200)