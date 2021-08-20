import logging

import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Return data
    body = json.dumps({"text": "Hello from the API!"})
    return func.HttpResponse(body=body)
