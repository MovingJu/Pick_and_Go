from fastapi import FastAPI

import routes, modules
import routes.db_test

app = FastAPI()

app.include_router(routes.db_test.router)
app.include_router(routes.Pick_n_Go.router)
app.include_router(routes.images_show.router)