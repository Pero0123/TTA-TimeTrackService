from fastapi import FastAPI, APIRouter, HTTPException
from bson import ObjectId
from .configurations import collection, entries
from .schemas import all_users, serialize_entries, serialize_entry, User, Entry

app = FastAPI()
router = APIRouter()


@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@router.get("/users")
async def get_all_users():
    try:
        data = list(collection.find())
        return all_users(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")


@router.post("/users")
async def create_user(new_user: User):
    try:
        resp = collection.insert_one(new_user.dict())
        return {"status_code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")


@router.get("/entries")
async def get_all_entries():
    try:
        data = list(entries.find())
        return serialize_entries(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching entries: {e}")


@router.post("/entries")
async def create_entry(new_entry: Entry):
    try:
        resp = entries.insert_one(new_entry.dict())
        return {"status_code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")


@router.get("/entries/{entry_id}")
async def get_entry(entry_id: str):
    try:
        entry = entries.find_one({"_id": ObjectId(entry_id)})
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return serialize_entry(entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching entry: {e}")

app.include_router(router)
