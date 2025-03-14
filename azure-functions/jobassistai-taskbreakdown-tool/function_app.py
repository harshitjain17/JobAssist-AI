import azure.functions as func
import logging
import json
from openai import AzureOpenAI
from clients import openai_client
from config import OPENAI_DEPLOYMENT

app = func.FunctionApp()

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the JSON data from the incoming request
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    task = req_body.get('task')
    disability_type = req_body.get('disability_type')
    employee_info = req_body.get('employee_info')

    if task and employee_info:
        # Create the prompt for OpenAI
        system_prompt = f"""
            You are a supportive AI assistant helping job coaches create notes for employee with disabilities in a supported employment program.
            Be respectful, sensitive and never use stigmatizing language. 
            Break down tasks into simple, numbered steps (Format: 1. [Step] 2. [Step]. 
            Note to Job Coach (Optional). Additional training resources (Optional).
            using clear, easy-to-understand language. 
            Steps should be small, specific, and achievable, focusing on one action at a time.
            Adjust instructions to fit the employee's disability and cognitive abilities.
            """
        
        user_prompt = f"Task to complete : {task} \n Employee has disability : {disability_type} \n Employee Info {employee_info}"

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
            response_instructions = openai_response.choices[0].message.content.strip()
            logging.info(f"Instructions for {task} about employee {employee_info}: {response_instructions}")
            return func.HttpResponse(
                json.dumps({"message": response_instructions}),
                status_code=200,
                mimetype="application/json")
            
        except Exception as e:
            error_message = f"OpenAI processing failed: {str(e)}"
            logging.error(error_message)
            return func.HttpResponse(f"{error_message}", status_code=400)

    else:
        return func.HttpResponse("Please provide both task and employee name", status_code=400)