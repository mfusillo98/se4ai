import time
from random import *
from locust import HttpUser, task, between
import json

'''
To start a locust test you have to create before a project and train it and store the
credentials inside the credentials variable

to start digit locust on terminal
'''


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    credentials = {"project_id": 34, "api_key": "H8RMIAIGWBCH90nBVSg12WaxNZvXdaV6"}

    # Edit a project name
    @task
    def project_update(self):
        body = {
            "api_key": self.credentials["api_key"],
            "name": "bookizon_" + str(randint(1, 100)),
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
            "images_url": ["https://www.salepepe.it/files/2014/03/come-fare-patate-fritte_05-1140x636.jpg"]
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
            "image_url": "https://blog.giallozafferano.it/allacciateilgrembiule/wp-content/uploads/2021/01/patatine-fritte-fatte-in-casa.jpg",
            "html": 0,
        }

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.get("/api/projects/search", params=params, headers=headers)
