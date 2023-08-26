import time
from random import *
from locust import HttpUser, task, between
import json

'''
To start a locust test you have ti create before a user and store the
credentials inside the credentials variable

to start digit locust on terminal
'''


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    credentials = {"project_id": 36, "api_key": "V3O9ZGg4t06BEzO3BLK5UX2bQd0egUlW"}

    # Edit a project name
    @task
    def project_update(self):
        body = {
            "api_key": self.credentials["api_key"],
            "name": "locust_test_" + str(randint(1, 100)),
            "selected_features_indexes": []
        }

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.post("/api/projects/" + str(self.credentials["project_id"]) + "/update", data=json.dumps(body),
                         headers=headers)

    # Add a new resource
    @task
    def project_update(self):
        body = {
            "api_key": self.credentials["api_key"],
            "name": "resource_test_" + str(randint(1, 100)),
            "external_resource_id": str(randint(1, 100)),
            "images_url": [
                "https://media.istockphoto.com/id/1322277517/photo/wild-grass-in-the-mountains-at-sunset.jpg?s=612x612&w=0&k=20&c=6mItwwFFGqKNKEAzv0mv6TaxhLN3zSE43bWmFN--J5w="]
        }

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.post("/api/projects/" + str(self.credentials["project_id"]) + "/resources/add",
                         data=json.dumps(body),
                         headers=headers)

    # Make a search
    @task
    def search(self):
        params = {
            "api_key": self.credentials["api_key"],
            "project_id": str(self.credentials["project_id"]),
            "limit": str(10),
            "offset": str(1),
            "images_url": "https://media.istockphoto.com/id/1322277517/photo/wild-grass-in-the-mountains-at-sunset.jpg?s=612x612&w=0&k=20&c=6mItwwFFGqKNKEAzv0mv6TaxhLN3zSE43bWmFN--J5w=",
            "html": 0
        }

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.get("/api/projects/search",
                        params=json.dumps(params),
                        headers=headers)
