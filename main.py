import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import callback, pollapi, pollpage, xlookupapi
from services.database import DatabaseService
from services.x import XService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseService.connect()
    await XService.login()
    yield
    async with asyncio.timeout(10):
        await DatabaseService.pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(callback.router)
app.include_router(pollapi.router)
app.include_router(pollpage.router)
app.include_router(xlookupapi.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
