import azure.functions as func
import logging
from clients import knowledge_retention_container

app = func.FunctionApp()

@app.route(route="http_trigger_cosmos")
def http_trigger_cosmos(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the JSON data from the incoming request
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    if req_body:
        try:
            # Insert the document (id will act as partition key)
            knowledge_retention_container.create_item(body=req_body)

            return func.HttpResponse("Insight successfully added to Cosmos DB.", status_code=200)
        except Exception as e:
            return func.HttpResponse(f"Cosmos Insertion Error: {str(e)}", status_code=500)
    else:
        return func.HttpResponse("Please provide JSON data to insert into Cosmos DB.", status_code=400)