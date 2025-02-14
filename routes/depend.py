import os

import dotenv
import orjson
from cryptography.fernet import Fernet
from fastapi import Cookie, HTTPException

dotenv.load_dotenv()

cipherSuite = Fernet(os.getenv("fernet_key"))


async def user(token: str = Cookie(None)):
    if token is None:
        raise HTTPException(401)
    userInfo = orjson.loads(cipherSuite.decrypt(token))
    return userInfo["data"]
