from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ---------------- Candidate Schema ----------------
class CandidateSchema(BaseModel):
    _id: str                    # unique ID for candidate
    name: str
    party: str
    moto: Optional[str] = None
    profile_pic: Optional[str] = None

# ---------------- Election Schema ----------------
class ElectionSchema(BaseModel):
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "Upcoming"        # Upcoming / Ongoing / Ended
    winner: Optional[str] = None
    candidates: List[CandidateSchema] = []

# ---------------- EC Base Schema ----------------
class ECBase(BaseModel):
    name: str
    email: EmailStr
    password: str

# ---------------- EC Create Schema ----------------
class ECCreate(ECBase):
    pass

# ---------------- EC Login Schema ----------------
class ECLogin(BaseModel):
    email: EmailStr
    password: str

# ---------------- EC Response Schema ----------------
class ECResponse(BaseModel):
    election_id: str
    name: str
    email: EmailStr
    election: ElectionSchema