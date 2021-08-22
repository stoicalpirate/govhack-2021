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
    """
    This is currently an open API accessible to any visitor from the 'profile'
    page. In future iterations the 'profile' page will be password-protected,
    so this API will only be accessible after reading the auth_header and
    decoding the 'x-ms-client-principal' data.
    """

    # DEMO: read the auth header from frontend (mock data for now)
    decoded = {"userId": "d75b260a64504067bfc5b2905e3b8181"}

    try:
        
        # Initialise the connection to Cosmos DB
        client = CosmosClient(url, credential=key)
        database = client.get_database_client(database_name)
        container_name = "users"
        container = database.get_container_client(container_name)
        
        # Try to retrieve the user object
        user = container.read_item(
            item=decoded["userId"],
            partition_key=decoded["userId"],
            )
    
    except CosmosHttpResponseError:
    
        # Create a new user object
        logging.info("User does not yet exist. Creating new user.")
        user = {}
        user["id"] = decoded["userId"]  # id = Azure AD B2C id
        user["_uid"] = str(uuid.uuid4())  # prepend "_" internal use
        user["userDetails"] = decoded["userDetails"]
        user["_userRoles"] = decoded["userRoles"]  # internal use
        user["topics"] = []
        container.upsert_item(user)

    subpath = req.route_params.get("subpath")

    if subpath == "topicdata":

        try:

            # Initialise the connection to Cosmos DB
            client = CosmosClient(url, credential=key)
            database = client.get_database_client(database_name)
            container_name = "topics"
            container = database.get_container_client(container_name)

            # Create an object of the user's topics to return to the frontend
            db_object = {
                "selected_topics": [],
                "unselected_topics": []
            }

            # Retrieve topics that the user has selected
            for item in container.query_items(
                    query="SELECT * FROM topics c WHERE ARRAY_CONTAINS(@usertopics, c.name)",
                    parameters=[dict(
                        name="@usertopics",
                        value=user["topics"]
                    )],
                    enable_cross_partition_query=True):
                db_object["selected_topics"].append(item)

            # Retrieve topics that the user has NOT selected
            for item in container.query_items(
                    query="SELECT * FROM topics",
                    enable_cross_partition_query=True):
                if item["name"] not in user["topics"]:
                    db_object["unselected_topics"].append(item)

            # If we have no data from the db then there's a problem...
            if len(db_object) == 0:
                raise ValueError

        except:  # TODO: change this to a more granular error later

            logging.info("Error with data. Using static data instead.")

            # DEMO ONLY: return demo data (as db may not contain user topics)
            db_object = {
                "selected_topics": [
                    {
                        "name": "environment",
                        "federal_trend": {
                            "x": ["2021-08-3", "2021-08-4", "2021-08-5", "2021-08-9", "2021-08-10", "2021-08-11", "2021-08-12"],
                            "y": [12, 23, 19, 8, 7, 2, 9]
                        },
                        "state_trend": {
                            "x": ["2021-08-3", "2021-08-4", "2021-08-5", "2021-08-10", "2021-08-11", "2021-08-12"],
                            "y": [4, 18, 3, 5, 7, 2]
                        },
                        "active_speakers": ["Politician A", "Politician B", "Politician C"],
                        "followers_by_electorate": {
                            "Fremantle": 279
                        },
                        "ranking_by_electorate": {
                            "Fremantle": 4
                        },
                        "local_member": "Info on the local member's engagement with this topic...",
                        "datasets": [
                            {
                                "name": "ABS Census Data",
                                "reference": "url..."
                            },
                            {
                                "name": "State Government Report 2020",
                                "reference": "url..."
                            }
                        ] 
                    },
                    {
                        "name": "homelessness",
                        "federal_trend": {
                            "x": ["2021-08-3", "2021-08-4", "2021-08-5", "2021-08-9", "2021-08-10", "2021-08-11", "2021-08-12"],
                            "y": [0, 0, 4, 0, 1, 0, 3]
                        },
                        "state_trend": {
                            "x": ["2021-08-3", "2021-08-4", "2021-08-5", "2021-08-10", "2021-08-11", "2021-08-12"],
                            "y": [0, 9, 1, 0, 0, 2]
                        },
                        "active_speakers": ["Politician B", "Politician D"],
                        "followers_by_electorate": {
                            "Fremantle": 218
                        },
                        "ranking_by_electorate": {
                            "Fremantle": 6
                        },
                        "local_member": "Info on the local member's engagement with this topic...",
                        "datasets": [
                            {
                                "name": "ABS Census Data",
                                "reference": "url..."
                            },
                            {
                                "name": "State Government Report 2020",
                                "reference": "url..."
                            }
                        ] 
                    },
                ],
                "unselected_topics": [
                    {
                        "name": "covid"
                    },
                    {
                        "name": "domestic violence"
                    },
                    {
                        "name": "mental health"
                    }
                ]
            }
        
        body = json.dumps(db_object)

    elif subpath == "followtopic":

        # Read the form data submitted from the frontend
        data = dict(req.form)
        
        if len(data) == 0:
            # Return an error response if there is no data
            return func.HttpResponse("Form not found", status_code=400)
        else:
            topic = data["selected_topic"]

        # Update the database to show user is now following the topic
        user["topics"].append(topic)
        container.upsert_item(user)

        body = json.dumps({"text": f"You are now following {topic}."})

    elif subpath == "newtopic":

        # Read the form data submitted from the frontend
        data = dict(req.form)
        
        if len(data) == 0:
            # Return an error response if there is no data
            return func.HttpResponse("Form not found", status_code=400)
        else:
            new_topic = data["new_topic"]

        # Get the CosmosDB container
        container_name = "topics"
        container = database.get_container_client(container_name)
        already_exists = False
        try:
            # Search the container to see if the topic already exists
            for item in container.query_items(
                    query="SELECT * FROM topics c WHERE c.name=@topic",
                    parameters=[dict(
                        name="@topic",
                        value=new_topic
                    )],
                    enable_cross_partition_query=True):
                if item["name"] == new_topic:
                    already_exists = True
                    logging.info("Item already exists")
        except CosmosHttpResponseError:
            return func.HttpResponse("Form not found", status_code=400)
        
        if not already_exists:
            # Create a new topic object if it doesn't already exist
            logging.info("Topic does not yet exist. Creating new topic.")
            item = {}
            item["name"] = new_topic
            container.upsert_item(item)

        body = json.dumps({"text": (
            f"Thank you for suggesting {new_topic} as a new topic.")
        })

    return func.HttpResponse(body=body)
