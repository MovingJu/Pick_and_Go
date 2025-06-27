from fastapi import FastAPI

# Something will come here..
import models

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

@APP.get("/model")
def model():
    model1 = models.Model1()
    del model1
    return {"Message": "still developing.."}