from fastapi import FastAPI

import routes

app = FastAPI()


@app.get("/")
def read_root():
    return {"To read API document, go to ": "localhost/docs"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None) -> dict[str, int | str | None]:
    return {"item_id": item_id, "q": q}

app.include_router(routes.images_show.router)
