import os

import dotenv
from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient
from pydantic import BaseModel, Field

from services.database import DatabaseService
from services.x import XService

from .depend import user

dotenv.load_dotenv()

router = APIRouter()
http = AsyncClient()
cipherSuite = Fernet(os.getenv("fernet_key"))


class PollModel(BaseModel):
    to: str
    reason: str = Field(..., min_length=5)


@router.post("/api/poll")
async def poll(model: PollModel, userInfo: dict[str, str] = Depends(user)):
    row = await DatabaseService.pool.fetchrow(
        'SELECT * FROM "2" WHERE id = $1', int(userInfo["id"])
    )
    if row:
        return ORJSONResponse(
            status_code=400,
            detail="1ユーザーが投票できる回数は一回までです。次回以降の投票をお待ちしております。",
        )
    if model.to == userInfo["id"]:
        return ORJSONResponse(
            status_code=400, content={"detail": "自分自身に投票することはできません。"}
        )

    """
    response = await http.get(
        f"https://api.x.com/2/users/{model.to}",
        headers={"Authorization": f"Bearer {os.getenv('x_bearer_token')}"},
    )
    if response.status_code != 200:
    """
    try:
        await XService.client.get_user_by_id(model.to)
    except:
        return ORJSONResponse(status_code=400, content={"detail": "無効な投票先"})

    await DatabaseService.pool.execute(
        'INSERT INTO "2" (id, "to", "reason") VALUES ($1, $2, $3);',
        int(userInfo["id"]),
        int(model.to),
        model.reason,
    )
    return {"detail": "投票しました。"}
