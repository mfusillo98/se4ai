"""
This script defines a Locust user for load testing a web API.

To start a locust test you have to create before a project and train it and store the
credentials inside the credentials variable

to start digit locust on terminal
"""

import json
import random
from locust import HttpUser, task, between



class QuickstartUser(HttpUser):
    """
    This class defines a Locust user for load testing a web API.
    """
    min_wait = 5000
    max_wait = 9000

    credentials = {"project_id": 34, "api_key": "H8RMIAIGWBCH90nBVSg12WaxNZvXdaV6"}

    @task
    def project_update(self):
        """
        Task to update a project.
        """

        body = {
            "api_key": self.credentials["api_key"],
            "name": "bookizon_" + str(random.randint(1, 100)),
            "selected_features_indexes": [
                4006, 3464, 395, 301, 1287, 2737, 3819, 206, 2233,
                2390, 2059, 1758, 1395, 1060, 1126, 4077, 2142,
                2440, 222, 3706, 26, 1068, 1193, 471, 3639, 562,
                3401, 1375, 1900, 1803, 967, 1940, 3276, 3606,
                818, 3990, 1027, 2442, 3968, 31, 443, 343, 2430,
                1464, 2126, 1843, 2493, 264, 800, 2830, 3395, 2070
            ]
        }

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.post("/api/projects/" + str(self.credentials["project_id"]) + "/update",
                         data=json.dumps(body),
                         headers=headers)

    @task
    def add_resource(self):
        """
        Task to add a new resource.
        """

        body = {
            "api_key": self.credentials["api_key"],
            "name": "resource_test_" + str(random.randint(1, 100)),
            "external_resource_id": str(random.randint(1, 100)),
            "images_url": [
                "https://www.salepepe.it/files/2014/03/come-fare-patate-fritte_05-1140x636.jpg"
            ]
        }

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.post("/api/projects/" + str(self.credentials["project_id"]) + "/resources/add",
                         data=json.dumps(body),
                         headers=headers)

    # Make a search
    @task
    def search(self):
        """
        Task to perform a search.
        """

        params = {
            "api_key": self.credentials["api_key"],
            "project_id": str(self.credentials["project_id"]),
            "limit": str(10),
            "image_url": "https://blog.giallozafferano.it/allacciateilgrembiule/"
                         "wp-content/uploads/2021/01/patatine-fritte-fatte-in-casa.jpg",
            "html": 0,
        }

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.get("/api/projects/search", params=params, headers=headers)
