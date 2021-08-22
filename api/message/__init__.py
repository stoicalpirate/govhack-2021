import logging
import os
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError
import azure.functions as func
import json
from datetime import datetime

url = os.environ["COSMOSDB_URL"]
key = os.environ["COSMOSDB_KEY"]
database_name = os.environ["COSMOSDB_DATABASE"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    This is an open API that any visitor to the website can access.
    It sends daily snapshot data to the home page to generate charts and
    graphics.
    """

    subpath = req.route_params.get("subpath")

    if subpath == "chartdata":

        try:
            
            # Initialise the connection to Cosmos DB
            client = CosmosClient(url, credential=key)
            database = client.get_database_client(database_name)
            container_name = "dailydata"
            container = database.get_container_client(container_name)
            
            # Search using a string of today's date retrieving 1 item only
            for item in container.query_items(
                    query="SELECT * FROM dailydata c WHERE c.yyyymmdd=@today",
                    parameters=[dict(
                        name="@today",
                        value=datetime.today().strftime("%Y-%m-%d")
                    )],
                    enable_cross_partition_query=True,
                    max_item_count=1):
                db_object = item
        
        except:  # TODO: change this to a more granular error later

            # DEMO ONLY: return demo data (as db may not contain today's data)
            db_object = {
                "topicflow": [
                    {
                        "x": ["14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29"],
                        "y": [20, 14, 23, 24, 30, 32, 30, 28, 27],
                        "name": "jobkeeper"
                    },
                    {
                        "x": ["14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29"],
                        "y": [32, 18, 29, 35, 28, 21, 29, 18, 15],
                        "name": "fruit farming"
                    },
                    {
                        "x": ["14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29"],
                        "y": [0, 0, 16, 21, 15, 9, 8, 8, 8],
                        "name": "vegetable farming"
                    },
                    {
                        "x": ["14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29"],
                        "y": [48, 68, 32, 20, 27, 38, 33, 46, 50],
                        "name": "employment"
                    },
                ],
                "wordcloud": [
                    ["jobs", 19],
                    ["employment", 16],
                    ["government", 17],
                    ["package", 13],
                    ["imperative", 9],
                    ["focus", 7],
                    ["Australians", 31],
                    ["working", 21],
                    ["national", 9]
                ],
                "speakertime": [
                    {
                        "x": [40, 23, 19, 21, 7, 6],
                        "y": ["Morrison", "Albanese", "Joyce", "Frydenberg", "Taylor", "Bandt"],
                        "marker": {
                            "color": [
                            "rgba(0,71,171,1)",
                            "rgba(222,53,51,1)",
                            "rgba(0,102,68,1)",
                            "rgba(0,71,171,1)",
                            "rgba(0,71,171,1)",
                            "rgba(16,194,91,1)"
                            ]
                        }
                    }
                ]
            }
        
        body = json.dumps(db_object)

    return func.HttpResponse(body=body)
