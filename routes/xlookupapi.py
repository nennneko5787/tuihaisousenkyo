import dotenv
from fastapi import APIRouter, Depends, HTTPException

from services.x import XService

from .depend import user

dotenv.load_dotenv()

router = APIRouter()


@router.get("/api/x/lookup/{userName:str}")
async def xLookup(userName: str, userInfo: dict[str, str] = Depends(user)):
    try:
        user = await XService.client.get_user_by_screen_name(userName)
        return {
            "id": str(user.id),
            "userName": user.screen_name,
            "name": user.name,
            "iconUrl": user.profile_image_url.replace("normal", "400x400"),
        }
    except:
        raise HTTPException(404, "ユーザーが存在しません。")
