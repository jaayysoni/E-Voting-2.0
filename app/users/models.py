from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ---------------- Base ----------------
class ECBase(BaseModel):
    name: str
    email: EmailStr


# ---------------- Create (Signup) ----------------
class ECCreate(ECBase):
    password: str
    confirm_password: str


# ---------------- Login ----------------
class ECLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------- Response (Safe to expose) ----------------
class ECResponse(BaseModel):
    election_id: str
    name: str
    email: EmailStr
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }