from fastapi import FastAPI, APIRouter, HTTPException
from .configurations import collection
from .schemas import all_users, User
import uvicorn

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
        resp = collection.insert_one(dict(new_user))
        return {"status_code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

app.include_router(router)


