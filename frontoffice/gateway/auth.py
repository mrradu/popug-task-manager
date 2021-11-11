from http import HTTPStatus

import requests
from loguru import logger

from frontoffice.entity import User


class AuthGateway:
    AUTH_HOST = "http://auth:8881"

    def get_users(self):
        response = requests.get(f"{self.AUTH_HOST}/user/?skip=0&limit=100")
        return response.json()

    def create_user(self, full_name: str, email: str, password: str):
        response = requests.post(
            f"{self.AUTH_HOST}/user/create",
            json={
                "email": email,
                "full_name": full_name,
                "password": password,
            },
        )
        return response

    def update_user(self, full_name, role, user_id):
        response = requests.post(
            f"{self.AUTH_HOST}/user/update",
            json={
                "role": role,
                "full_name": full_name,
                "user_id": user_id,
            },
        )
        return response

    def check_auth_user(self, cookies):
        logger.info("Check user authentication")
        response = requests.get(
            f"{self.AUTH_HOST}/auth/me",
            headers={"Authorization": cookies["Authorization"]},
        )
        print(response.json())
        print(User(**response.json()))

        try:
            return User(**response.json())
        except:
            raise

    def auth_user(self, email, password):
        response = requests.post(
            f"{self.AUTH_HOST}/auth/login",
            data={"username": email, "password": password},
        )

        logger.info(f"Auth user response: {response.json()}")
        return response


auth_gateway = AuthGateway()
