from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EntryStart(BaseModel):
    name: str = Field(..., example="Work on project")

class Entry(BaseModel):
    id: str
    name: str
    starttime: datetime
    endtime: Optional[datetime] = None
    duration: Optional[int] = None  #ime in seconds


#*********************Project managment models*************************
class ProjectCreate(BaseModel):
    name: str = Field(..., example="Serial Link"),
    description: str = Field(..., example="My main project"),

class Project(BaseModel):
    id: str
    owner_id: str
    name: str
    description: str
    
class ProjectOfUser:
    owner_id: str
