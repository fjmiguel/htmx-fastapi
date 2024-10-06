from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow these origins to access the API
origins = [
  "http://127.0.0.1:5500",
  "http://localhost:5500",
]

# Allow these methods to be used
methods = ["*"]

# Only these headers are allowed
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)

# In memory storage for items
items = []
next_id = 1

# Pydantic model do define the Item Structure
class Item(BaseModel):
  id: int
  name: str

# READ: get all items
@app.get("/items", response_model=List[Item])
async def get_items():
  return items

# CREATE: add a new item
@app.post("/items", response_model=Item)
async def create_item(name: str = Form(...)):
  global next_id

  if any(item.name == name for item in items):
    raise HTTPException(status_code=200, detail="Item already exists")

  new_item = Item(id=next_id, name=name)
  items.append(new_item)
  next_id += 1
  return new_item

# EDIT an item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, name: str = Form(...)):
    for item in items:
      if item.id == item_id:
        item.name = name
        return item

    raise HTTPException(status_code=404, detail="Item not found")

# DELETE an item
@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
  global items

  # Filter out the item with the specified id
  items = [item for item in items if item.id != item_id]

  return {"detail": "Item deleted"}
