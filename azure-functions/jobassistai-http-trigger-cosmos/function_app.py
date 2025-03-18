import azure.functions as func
import logging
import uuid
from clients import knowledge_retention_container, openai_client
from config import TEXT_EMBEDDING_MODEL

app = func.FunctionApp()

@app.route(route="http_trigger_cosmos")
def http_trigger_cosmos(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the JSON data from the incoming request
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    category = req_body.get('category')
    details = req_body.get('details')
    
    if category and details:
        try:
            details_vector_response = openai_client.embeddings.create(
                input = details,
                model= TEXT_EMBEDDING_MODEL
            )
            details_vector = details_vector_response.data[0].embedding

            # Insert document
            insight = {
                "id": str(uuid.uuid4()),  # Unique ID
                "category": category,
                "details": details,
                "detailsVector": details_vector  # Store vector representation
            }
            try:
                # Insert the document (id will act as partition key)
                knowledge_retention_container.create_item(insight)
                return func.HttpResponse("Insight successfully added to Cosmos DB.", status_code=200)
            except Exception as e:
                return func.HttpResponse(f"Save Insight - Cosmos Insertion Error: {str(e)}", status_code=500)
            
        except Exception as e:
            return func.HttpResponse(f"Save Insight - OpenAI Embedding Error: {str(e)}", status_code=500)
        
    else:
        return func.HttpResponse("Please provide JSON data to insert into Cosmos DB.", status_code=400)