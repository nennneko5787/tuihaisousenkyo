import os

from twikit.guest import GuestClient
import dotenv

dotenv.load_dotenv()


class XService:
    client: GuestClient = None

    @classmethod
    async def login(cls):
        cls.client = GuestClient()
        await cls.client.activate()
