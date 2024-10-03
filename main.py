from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

# In memory storage for items
items = []
next_id = 1

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Pydantic model do define the Item Structure
class Item(BaseModel):
  id: int = None
  name: str

@app.get("/", response_class=HTMLResponse)
def read_index():
  with open("static/index.html") as f:
    return HTMLResponse(content=f.read())

# Function to render the list of items
def render_items_list(request: Request):
  return templates.TemplateResponse("items_list.html", {
      "request": request,
      "items": items
  })

@app.get("/items", response_class=HTMLResponse)
async def get_items(request: Request):
  return render_items_list(request)

@app.post("/items", response_class=HTMLResponse)
async def create_item(request: Request, name: str = Form(...)):
  global items
  global next_id

  if any(item.name == name for item in items):
    return render_items_list(request)

  item = Item(id=next_id, name=name)
  next_id += 1
  items.append(item)

  return render_items_list(request)

@app.get("/items/{item_id}/edit", response_class=HTMLResponse)
async def edit_item(request: Request, item_id: int):
    item = next((i for i in items if i.id == item_id), None)
    if not item:
        return "Item not found"

    return templates.TemplateResponse("edit_item.html", {"request": request, "item": item})

@app.get("/items/{item_id}/cancel", response_class=HTMLResponse)
async def cancel_edit(request: Request, item_id: int):
    item = next((i for i in items if i.id == item_id), None)
    if not item:
        return "Item not found"

    return render_items_list(request)

@app.put("/items/{item_id}", response_class=HTMLResponse)
async def update_item(request: Request, item_id: int):
  form_data = await request.form()
  new_name = form_data.get("name")

  # Update the item in the list
  for item in items:
      if item.id == item_id:
          item.name = new_name

  # Return updated content to be swapped in
  return render_items_list(request)

@app.delete("/items/{item_id}")
async def delete_item(request: Request, item_id: int):
  global items  # Explicitly declare that we're modifying the global 'items'
  print(f"Items before deletion: {[item.id for item in items]}")

  # Filter out the item with the specified id
  items = [item for item in items if item.id != item_id]

  # Debug logging for items after deletion
  print(f"Items after deletion: {[item.id for item in items]}")

  return render_items_list(request)
