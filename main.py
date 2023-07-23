from typing import Any, Dict, List, Tuple

from fastapi import FastAPI, Request
from pydantic.main import BaseModel

from operations import PineconeOperations

app = FastAPI()
pineconeOps = PineconeOperations()


class DataItem(BaseModel):
    label: str
    values: List[float]
    metadata: Dict[str, str]

class Data(BaseModel):
    payload: List[Tuple[str, List[float], Dict[str, str]]]

@app.get("/api/v1/health")
async def root():
    return {"message": "OK"}


@app.post("/api/v1/index")
async def create_index(name: str):
    return pineconeOps.create_index(index_name=name)

@app.get("/api/v1/connect")
async def create_index():
    return pineconeOps.connect_index()


@app.post("/api/v1/vectors")

# {
#     "payload": [
#         ["vec1", [0.1, 0.2, 0.3, 0.4], {"genre": "drama"}],
#         ["vec2", [0.2, 0.3, 0.4, 0.5], {"genre": "action"}]
#     ]
# }
async def create_index(data: Data):
    return pineconeOps.upsert(data=data.payload)


@app.post("/api/v1/search-vector")
# [0.1, 0.2, 0.3, 0.4]
async def create_index(payload: List[Any]):
    return pineconeOps.query(query_vector=payload)