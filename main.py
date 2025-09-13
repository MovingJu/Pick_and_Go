import sys
import asyncio
from fastapi import FastAPI

import routes


app = FastAPI()

app.include_router(routes.total_travel_plan.router)
app.include_router(routes.random_api.router)
app.include_router(routes.main_service.router)
app.include_router(routes.test.router)
app.include_router(routes.attraction_detail.router)
# app.include_router(routes.db_test.router)


async def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1] != "test"):
            return

        import test_files

        await test_files.main()

        return

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)
    # uvicorn.run(app, host="0.0.0.0", port=8080, reload=False, ssl_certfile="./server.crt", ssl_keyfile="./server.key")


if __name__ == "__main__":
    asyncio.run(main())