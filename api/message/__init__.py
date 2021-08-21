import logging
import os

import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    subpath = req.route_params.get("subpath")

    if subpath == "ping":

        body = json.dumps({"text": "Hello from the API!"})

    elif subpath == "chartdata":

        db_object = {
            "topicflow": [
                {
                    "x": ["14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29"],
                    "y": [20, 14, 23, 24, 30, 32, 30, 28, 27],
                    "name": "jobkeeper",
                    "type": "bar"
                },
                {
                    "x": ["14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29"],
                    "y": [32, 18, 29, 35, 28, 21, 29, 18, 15],
                    "name": "fruit farming",
                    "type": "bar"
                },
                {
                    "x": ["14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29"],
                    "y": [0, 0, 16, 21, 15, 9, 8, 8, 8],
                    "name": "vegetable farming",
                    "type": "bar"
                },
                {
                    "x": ["14:21", "14:22", "14:23", "14:24", "14:25", "14:26", "14:27", "14:28", "14:29"],
                    "y": [48, 68, 32, 20, 27, 38, 33, 46, 50],
                    "name": "employment",
                    "type": "bar"
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
                    "type": "bar",
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
                    },
                    "orientation": "h"
                    }
            ],
            "databasename": os.environ["COSMOSDB_DATABASE"]
        }
        body = json.dumps(db_object)

    return func.HttpResponse(body=body)
