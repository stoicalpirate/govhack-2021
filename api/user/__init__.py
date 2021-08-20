import logging
import base64
import json
import os
import uuid
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError
import azure.functions as func

url = os.environ["COSMOSDB_URL"]
key = os.environ["COSMOSDB_KEY"]
database_name = os.environ["COSMOSDB_DATABASE"]

def main(req: func.HttpRequest) -> func.HttpResponse:

    # Read the auth header from frontend
    auth_header = req.headers.get("x-ms-client-principal", None)
    decoded = json.loads(base64.b64decode(auth_header).decode("utf-8"))

    subpath = req.route_params.get("subpath")

    if subpath == "get-id":

        body = json.dumps({"text": f"User ID is {decoded['userId']}"})

    elif subpath == "upsert-user":

        # Read the form data submitted from the frontend
        data = dict(req.form)
        
        if len(data) == 0:
            # Return an error response if there is no data
            return func.HttpResponse("Form not found", status_code=400)
        
        else:
            logging.info(decoded)
            logging.info(data)

            # Initialise the connection to Cosmos DB
            client = CosmosClient(url, credential=key)
            database = client.get_database_client(database_name)
            container_name = "items"
            container = database.get_container_client(container_name)
            
            try:
                # Try to retrieve the user object
                item = container.read_item(
                    item=decoded["userId"],
                    partition_key=decoded["userId"],
                    )
            except CosmosHttpResponseError:
                # Create a new user object
                logging.info("User does not yet exist. Creating new user.")
                item = {}
                item["id"] = decoded["userId"]  # id = Azure AD B2C id
                item["_uid"] = str(uuid.uuid4())  # prepend "_" internal use
                item["userDetails"] = decoded["userDetails"]
                item["_userRoles"] = decoded["userRoles"]  # internal use
            
            # Upsert the new or revised object, overwriting any existing object
            item[data["key_data"]] = data["value_data"]  # New data
            updated_item = container.upsert_item(item)

            # Remove sensitive data then return the item to the frontend
            for k, v in list(updated_item.items()):
                if k.startswith("_"):
                    del updated_item[k]
            logging.info(updated_item)
            body = json.dumps(updated_item)
            
    return func.HttpResponse(body=body)
