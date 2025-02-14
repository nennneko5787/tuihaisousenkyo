import asyncio
import os

import dotenv
from httpx import AsyncClient

dotenv.load_dotenv()


async def main():
    http = AsyncClient()
    response = await http.get(
        f"https://api.x.com/2/users/1794349365093662720",
        headers={"Authorization": f"Bearer {os.getenv('x_bearer_token')}"},
    )
    print(response.json())


asyncio.run(main())
