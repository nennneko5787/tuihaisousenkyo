import os

import twikit
import dotenv

dotenv.load_dotenv()


class XService:
    client: twikit.Client = None

    @classmethod
    async def login(cls):
        cls.client = twikit.Client(language="ja-JP")
        await cls.client.login(
            auth_info_1=os.getenv("x_account_id"),
            auth_info_2=os.getenv("x_account_email"),
            password=os.getenv("x_account_password"),
            cookies_file="cookie.json",
        )
