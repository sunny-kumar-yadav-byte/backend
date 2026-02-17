from fastapi import FastAPI
from firebase import db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "API working"}

# ADD TASK TO FIRESTORE
@app.post("/task")
def add_task(title: str):
    db.collection("tasks").add({"title": title})
    return {"message": "Task added to Firestore"}

# GET TASKS FROM FIRESTORE
@app.get("/tasks")
def get_tasks():
    docs = db.collection("tasks").stream()
    tasks = []
    for doc in docs:
        data = doc.to_dict()
        tasks.append({
            "title": data.get("title"),
            "task_id": data.get("task_id")
        })
    return {"tasks": tasks}

# UPDATE TASK (using document id)
@app.put("/task/{task_id}")
def update_task(task_id: int, new_title: str):
    docs = db.collection("tasks").stream()

    for doc in docs:
        data = doc.to_dict()
        if data.get("task_id") == task_id:
            db.collection("tasks").document(doc.id).update({"title": new_title})
            return {"message": "Task updated"}

    return {"error": "Task not found"}


# DELETE TASK
@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    docs = db.collection("tasks").stream()

    for doc in docs:
        data = doc.to_dict()
        if data.get("task_id") == task_id:
            db.collection("tasks").document(doc.id).delete()
            return {"message": "Task deleted"}

    return {"error": "Task not found"}




