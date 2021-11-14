import requests
from loguru import logger


class ItemsGateway:
    INVENTORY_HOST = "http://inventory:8883"

    def get_tasks(self, cookies):
        response = requests.post(
            f"{self.INVENTORY_HOST}/items/get",
            cookies=cookies,
        )
        print("content", response.content)
        try:
            return response.json()
        except Exception:
            return []

    def add_tasks(self, task_title: str, task_description: str):
        logger.info(f"Create task {task_title}, with description {task_description}")
        response = requests.post(
            f"{self.INVENTORY_HOST}/items/add",
            json={"title": task_title, "description": task_description},
        )
        print(response.content)
        # return response.json()


item_gateway = ItemsGateway()
