import azure.functions as func
import logging
from clients import speech_synthesizer, audio_completed

app = func.FunctionApp()

@app.route(route="http_trigger_tts")
def http_trigger_tts(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Text To Speech HTTP trigger function processed a request.')

    # Get the JSON data from the incoming request
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    text = req_body.get('text')

    if text:
        # Synthesize the text to speech
        result = speech_synthesizer.speak_text_async(text).get()
        # Check the result
        if result.reason == audio_completed:
            logging.info("Speech synthesized successfully.")
            audio_date = result.audio_data
            return func.HttpResponse(body=audio_date, status_code=200, mimetype="audio/mpeg")
        else:
            return func.HttpResponse(f"Speech synthesis failed with result reason - {result.reason}", status_code=400)
    else:
        return func.HttpResponse("Please provide text you would like to convert to audio using Azure Text-to-Speech.", status_code=400)