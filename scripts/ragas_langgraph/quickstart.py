from fastapi import FastAPI # pip install fastapi
from typing import Optional
from pydantic import BaseModel
from fastapi import Body

app = FastAPI()
# localhost || Swagger UI
# GET METHOD
@app.get("/")
def index():
    return {"message": "Welcome to this Endpoint"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "OK"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/item/{item_id}")
def read_item_query(item_id: int, q: Optional[str] = None, page: Optional[int] = None):
    return {"item_id": item_id,"query":q,"page":page}

class User(BaseModel):
    name: str
    age: int

@app.post("/users/")
def create_user(user: User):
    return {"message":f"Welcome {user.name}. You are {user.age} years old."}


# uvicorn quickstart:app --reload
