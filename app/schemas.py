from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    user_name: str
    password: str  

class Entry(BaseModel):
    mongo_id: str       # MongoDB ObjectId as string
    id: int             # Your regular integer ID
    entryName: str
    startTime: datetime
    endTime: datetime
    duration: int

# Single entry serializer
def serialize_entry(entry):
    return {
        "mongo_id": str(entry["_id"]),  # MongoDB ObjectId as string
        "id": entry["id"],              # Your own integer ID
        "entryName": entry["entryName"],
        "startTime": entry["startTime"],
        "endTime": entry["endTime"],
        "duration": entry["duration"]
    }

# Multiple entries
def serialize_entries(entries):
    return [serialize_entry(entry) for entry in entries]

def individual_data(user):
    return {
        "id": str(user["_id"]),
        "user_id": user["user_id"],
        "user_name": user["user_name"],
        "password": user.get("password")
    }

def all_users(users):
    return [individual_data(user) for user in users]
