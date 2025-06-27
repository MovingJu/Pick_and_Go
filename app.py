from fastapi import FastAPI

APP = FastAPI()

@APP.get('/')
def index():
    return {"Message": "Hellow world!"}

@APP.get("/items/{item_id}")
def items(item_id: int, q: str = "") -> dict[int, str]: 
    return {"Item id: ": item_id, "q: ": q} #type: ignore

@APP.get('/about')
def about():
    return {"Message": "This is about page."}
