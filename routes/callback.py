import os

import dotenv
from cryptography.fernet import Fernet
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

dotenv.load_dotenv()

router = APIRouter()
http = AsyncClient()
cipherSuite = Fernet(os.getenv("fernet_key"))


@router.get("/callback")
async def callback(state: str, code: str):
    response = await http.post(
        "https://api.twitter.com/2/oauth2/token",
        headers={"Authorization": f"Basic {os.getenv('x_oauth2_client_key')}"},
        data={
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": os.getenv("redirect_uri"),
            "code_verifier": "challenge",
            "client_id": os.getenv("x_oauth2_clientid"),
        },
    )
    jsonData: dict = response.json()
    accessToken = jsonData.get("access_token")
    response = await http.get(
        "https://api.x.com/2/users/me",
        headers={"Authorization": f"Bearer {accessToken}"},
    )
    if response.status_code != 200:
        raise HTTPException(403)
    userInfo = response.text
    response = RedirectResponse("/")
    response.set_cookie(
        "token",
        value=cipherSuite.encrypt(userInfo.encode()).decode(),
        max_age=60 * 60 * 24 * 365 * 10,
    )
    return response
