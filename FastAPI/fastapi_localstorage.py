from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

DATA_FILE = "items.json"

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_items(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=4)

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    items = load_items()
    return items.get(str(item_id), {"error": "Item not found"})

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items = load_items()
    items[str(item_id)] = item.dict()
    save_items(items)
    return {"saved": items[str(item_id)]}
