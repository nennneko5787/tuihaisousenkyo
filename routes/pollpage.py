import os

import dotenv
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

dotenv.load_dotenv()
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def loginWithX(request: Request):
    return RedirectResponse(
        f"https://x.com/i/oauth2/authorize?response_type=code&client_id={os.getenv("x_oauth2_clientid")}&redirect_uri={os.getenv('redirect_uri')}&scope=tweet.read%20users.read%20offline.access&state=state&code_challenge=challenge&code_challenge_method=plain"
    )


@router.get("/", response_class=HTMLResponse)
async def pollPage(request: Request):
    return templates.TemplateResponse(
        request=request, name="poll.html", context=request.cookies
    )
