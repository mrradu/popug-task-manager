from http import HTTPStatus

import requests
from loguru import logger

from frontoffice.entity import User


class AuthGateway:
    AUTH_HOST = "http://auth:8881"

    def check_auth_user(self, cookies):
        logger.info(f"Check user authentication{cookies}")
        response = requests.get(
            f"{self.AUTH_HOST}/auth/me",
            headers=cookies,
        )
        logger.info(response.json())

        try:
            return User(**response.json())
        except:
            raise


auth_gateway = AuthGateway()
