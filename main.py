from fastapi import FastAPI

import routes


app = FastAPI()

app.include_router(routes.total_travel_plan.router)
app.include_router(routes.random_api.router)
app.include_router(routes.main_service.router)
app.include_router(routes.test.router)
# app.include_router(routes.db_test.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)
    # uvicorn.run(app, host="0.0.0.0", port=8080, reload=False, ssl_certfile="./server.crt", ssl_keyfile="./server.key")