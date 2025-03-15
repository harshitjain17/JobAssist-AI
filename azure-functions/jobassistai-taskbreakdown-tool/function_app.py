import azure.functions as func
import logging
import json
from openai import AzureOpenAI
from clients import openai_client
from config import OPENAI_DEPLOYMENT, system_prompt_mapping

app = func.FunctionApp()

@app.route(route="http_trigger_openai")
def http_trigger_openai(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Open AI HTTP trigger function processed a request.')

    # Get the JSON data from the incoming request
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    system_role = req_body.get('system_role')
    user_prompt = req_body.get('user_prompt')

    if system_role and user_prompt:
        # Prepare the system prompt based on the system role
        system_prompt = system_prompt_mapping.get(system_role, "")

        logging.info(f"Processing Open AI Request with System Role: {system_role}, System Prompt: {system_prompt}, User Prompt: {user_prompt}")

        # Call Azure OpenAI to get the response
        try:
            openai_response = openai_client.chat.completions.create(
                model=OPENAI_DEPLOYMENT,
                # response_format={"type": "json_object"},  # Enable JSON mode
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,    # Low temperature for structured output
                max_tokens=10000    # Increased to handle complex notes
            )
            response_message = openai_response.choices[0].message.content.strip()
            return func.HttpResponse(
                json.dumps({"message": response_message}),
                status_code=200,
                mimetype="application/json")
            
        except Exception as e:
            error_message = f"Azure OpenAI processing for system_prompt: {system_prompt} and user_prompt: {user_prompt} failed: {str(e)}"
            logging.error(error_message)
            return func.HttpResponse(f"{error_message}", status_code=400)

    else:
        return func.HttpResponse("Please provide both system role and user prompt", status_code=400)