from pydantic import BaseModel, EmailStr
from typing import Optional

class VoterBase(BaseModel):
    name: str
    email: EmailStr

class VoterCreate(VoterBase):
    password: str

class VoterResponse(VoterBase):
    id: str
    election_id: str
    has_voted: bool = False