from fastapi import FastAPI

import routes, modules


app = FastAPI()

app.include_router(routes.random_api.router)
app.include_router(routes.main_service.router)
app.include_router(routes.test.router)
# app.include_router(routes.db_test.router)