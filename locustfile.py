import time
from locust import HttpUser, task, between
from server import loadCompetitions


class SimulatingUser(HttpUser):

    wait_time = between(1, 3)
    competitions = loadCompetitions()

    def on_start(self):
        self.client.get("")
        self.client.post("showSummary", {"email": "john@simplylift.co"})

    def on_stop(self):
        self.client.get("logout")

    @task
    def getBook(self):
        self.client.get("book/TEST/Simply Lift")


    @task
    def getPurchasePlaces(self):
        self.client.post(
            "purchasePlaces",
            {"places": 1,
             "club": "Simply Lift",
             "competition": "TEST"
             },
        )
