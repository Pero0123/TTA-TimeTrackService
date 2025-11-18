from fastapi import FastAPI, HTTPException
from datetime import datetime
from bson import ObjectId

from .schemas import EntryStart, Entry, ProjectCreate, Project
from .models import entry_helper, project_helper
from .configurations import db, entries_collection, projects_collection
app = FastAPI(title="Time Tracker API")
currentUser = "691c8bf8d691e46d00068bf3"
#start a time entry using put
@app.put("/entries/", response_model=Entry)
def start_entry(entry: EntryStart):
    now = datetime.now()
    entry_dict = {
        "name": entry.name,
        "project_group_id": ObjectId(entry.project_group_id),
        "starttime": now,
        "endtime": None,
        "duration": None
    }
    result = entries_collection.insert_one(entry_dict)
    created_entry = entries_collection.find_one({"_id": result.inserted_id})
    return entry_helper(created_entry)

#complete a time entry
@app.patch("/entries/{entry_id}", response_model=Entry)
def end_entry(entry_id: str):
    entry = entries_collection.find_one({"_id": ObjectId(entry_id)})
    
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    if entry.get("endtime") is not None:
        raise HTTPException(status_code=400, detail="Entry already ended")
    
    now = datetime.now()
    starttime = entry["starttime"]
    duration_seconds = int((now - starttime).total_seconds())
    
    entries_collection.update_one(
        {"_id": ObjectId(entry_id)},
        {"$set": {"endtime": now, "duration": duration_seconds}}
    )
    
    updated_entry = entries_collection.find_one({"_id": ObjectId(entry_id)})
    return entry_helper(updated_entry)

# List all entries
@app.get("/entries/", response_model=list[Entry])
def list_entries():
    entries = entries_collection.find()
    return [entry_helper(e) for e in entries]

#list entries belongin to a project
@app.get("/entries/project/{project_id}", response_model=list[Entry])
def list_entries_from_project(project_id: str):

    #validate ObjectId format
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project id")

    # check if project exists
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    #fetch entries belonging to project
    entries = entries_collection.find({"project_group_id": ObjectId(project_id)})

    return [entry_helper(e) for e in entries]

#********************project Managment*******************************
@app.put("/projects/", response_model=Project)
def create_project(project: ProjectCreate):
    project_dict = {
        "name": project.name,
        "description": project.description,
        "owner_id": ObjectId(currentUser)
    }
    result = projects_collection.insert_one(project_dict)
    created_project = projects_collection.find_one({"_id": result.inserted_id})
    return project_helper(created_project)

# list all projects
@app.get("/projects/", response_model=list[Project])
def list_projects():
    projects = projects_collection.find()
    return [project_helper(p) for p in projects]

#list projects belongin to the current user
@app.get("/projects/user", response_model=list[Project])
def list_users_projects():
    projects = projects_collection.find({"owner_id": ObjectId(currentUser)})
    return [project_helper(p) for p in projects]


# python -m uvicorn app.main:app --reload