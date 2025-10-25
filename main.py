from fastapi import FastAPI
from datetime import datetime
import logging

import routes

logging.basicConfig(
    level=logging.INFO,           # 출력 레벨
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler(f"./log/{datetime.now().strftime("%Y-%m-%d_%H:%M")}.log"),  # 파일로 저장
        logging.StreamHandler()          # 콘솔 출력
    ]
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

app = FastAPI()

app.include_router(routes.total_travel_plan.router)
app.include_router(routes.random_api.router)
app.include_router(routes.main_service.router)
app.include_router(routes.test.router)
app.include_router(routes.attraction_detail.router)
app.include_router(routes.test.router)
# app.include_router(routes.db_test.router)

logging.info("Server started.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)
    # uvicorn.run(app, host="0.0.0.0", port=8080, reload=False, ssl_certfile="./server.crt", ssl_keyfile="./server.key")

logging.info("Server closed gracefully.")