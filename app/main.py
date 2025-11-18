from fastapi import FastAPI, HTTPException
from datetime import datetime
from bson import ObjectId

from .schemas import EntryStart, Entry
from .models import entries_collection, entry_helper

app = FastAPI(title="Time Tracker API")

#start a time entry using put
@app.put("/entries/", response_model=Entry)
def start_entry(entry: EntryStart):
    now = datetime.now()
    entry_dict = {
        "name": entry.name,
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
