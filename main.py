from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend (React) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React runs on 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for a task
class Task(BaseModel):
    title: str
    description: str
    done: bool = False

# In-memory task list (you can replace with a DB later)
tasks = []

# ------------------ Routes ------------------

# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Create a new task
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task.dict())
    return {"message": "Task added successfully"}

# Mark task as done
@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks[task_id]["done"] = True
    return {"message": "Task marked as done"}

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks.pop(task_id)
    return {"message": "Task deleted successfully"}
