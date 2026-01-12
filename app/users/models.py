from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ECBase(BaseModel):
    name: str
    email: str
    password: str

class ECCreate(ECBase):
    pass

class ECLogin(BaseModel):
    election_id: str
    password: str

class ECResponse(BaseModel):
    election_id: str
    name: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]