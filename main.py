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
        task = doc.to_dict()
        task["id"] = doc.id   # this line adds document id
        tasks.append(task)

    return {"tasks": tasks}

# UPDATE TASK (using document id)
@app.put("/task/{doc_id}")
def update_task(doc_id: str, new_title: str):
    db.collection("tasks").document(doc_id).update({"title": new_title})
    return {"message": "Task updated"}

# DELETE TASK
@app.delete("/task/{doc_id}")
def delete_task(doc_id: str):
    db.collection("tasks").document(doc_id).delete()
    return {"message": "Task deleted"}


