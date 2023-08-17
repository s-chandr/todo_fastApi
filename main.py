from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from pymongo import MongoClient


from typing import Optional 
# for query params


app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
todos = db["todos_new"]

class Todo(BaseModel):
    """
    Model for a Todo item
    """
    id: int
    task: str
    done: bool = False

# ------------------------------------------------------------------------------------------------
@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo):
    """
    Endpoint for creating a Todo item
    """
    inserted_id = todos.insert_one(todo.dict()).inserted_id
    return todos.find_one({"_id": inserted_id})

# Example request:
# POST /todos/
# {
#   "id":1,
#   "task": "Buy groceries",
#   "done": false
# }



# ------------------------------------------------------------------------------------------------
@app.get("/todos/", response_model=list[Todo])
async def get_todo():
    return todos.find({})


@app.get("/todos/{title}", response_model=Todo)
async def get_todo_by_title(title :str ):
  
    todo = todos.find_one({"task": title})
    
    if todo:
        return todo
    raise HTTPException(404, f"There is no todo with the title {title}")

# Example request:
# GET /todos/Bring_milk

# ------------------------------------------------------------------------------------------------
@app.put("/todos/{id}", response_model=Todo)
async def update_todo(id: int, todo: Todo):
    """
    Endpoint for updating a Todo item by ID
    """
    result = todos.update_one({"id": id}, {"$set": todo.dict()})
    if result.modified_count:
        return todos.find_one({"id": id})
    else:
        raise HTTPException(status_code=404, detail="Todo with id not found")

# Example request:
# PUT /todos/2
# {
#   "id":1,
#   "task": "Buy more groceries",
#   "done": true
# }

# ------------------------------------------------------------------------------------------------
@app.delete("/todos/{id}", response_model=Todo)
async def delete_todo(id: int):
    """
    Endpoint for deleting a Todo item by ID
    """
    todo = todos.find_one({"id": id})
    if todo:
        todos.delete_one({"id": id})
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

# Example request:
# DELETE /todos/2


@app.get("/")
async def root():
    return {"message": "Hello World"}