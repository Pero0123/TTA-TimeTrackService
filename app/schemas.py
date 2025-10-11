# app/schemas.py
from pydantic import BaseModel, EmailStr, constr, conint

class User(BaseModel):
    user_id:int
    user_name:str
    password:str


def individual_data(user):
    return{
        "id": str(user["_id"]),
        "user_id": user["user_id"],
        "user_name": user["user_name"],
        "password": user["password"]
    }


def all_users(users):
    return [individual_data(user) for user in users]