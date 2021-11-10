import requests


class ItemsGateway:
    AUTH_HOST = "http://inventory:8883"

    def get_tasks(self):
        response = requests.post(f"{self.AUTH_HOST}/items/get")
        return response.json()


item_gateway = ItemsGateway()
