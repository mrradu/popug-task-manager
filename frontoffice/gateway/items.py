import requests
from loguru import logger


class ItemsGateway:
    AUTH_HOST = "http://inventory:8883"

    def get_tasks(self):
        response = requests.post(f"{self.AUTH_HOST}/items/get")
        return response.json()

    def add_tasks(self, task_title: str, task_description: str):
        logger.info(f"Create task {task_title}, with description {task_description}")
        response = requests.post(
            f"{self.AUTH_HOST}/items/add",
            json={"title": task_title, "description": task_description},
        )
        print(response.content)
        # return response.json()


item_gateway = ItemsGateway()
