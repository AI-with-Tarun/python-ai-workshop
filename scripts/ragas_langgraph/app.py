# pip install fastapi
# pip install uvicorn: server ASGI server
from fastapi import FastAPI
from pydantic import BaseModel
from state import graph_builder
from typing import List

class Query(BaseModel):
    query: str

class Response(BaseModel):
    query: str
    context: List[str]
    answer: str

app = FastAPI()

@app.get("/healthcheck")
def health():
    return {"status": "Ok"}

graph = graph_builder()

@app.post("/rag", response_model=Response)
def get_response(request: Query):
    result = graph.invoke({"query":request.query})
    return result