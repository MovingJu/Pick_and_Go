from fastapi import FastAPI

import routes

app = FastAPI()

app.include_router(routes.images_show.router)
app.include_router(routes.Pick_n_Go.router)