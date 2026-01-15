from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ---------------- Base Voter Model ----------------
class VoterBase(BaseModel):
    """
    Base model for voter creation or internal use.
    """
    name: str
    email: EmailStr
    password: str  # plaintext, will be hashed before saving
    election_id: str  # reference to the election/EC

# ---------------- Voter Login Model ----------------
class VoterLogin(BaseModel):
    """
    Model for voter login.
    """
    email: EmailStr
    password: str

# ---------------- Voter Response Model ----------------
class VoterResponse(BaseModel):
    """
    Model for returning voter info.
    '_id' is stored as string to avoid ObjectId issues.
    """
    id: str = Field(..., alias="_id")  # maps MongoDB '_id' to 'id'
    name: str
    email: EmailStr
    has_voted: bool = False
    voted_for: Optional[str] = None  # candidate ID if voted
    election_id: str
    password_hash: Optional[str] = None  # optional, internal use only

    model_config = {
        "from_attributes": True  # allows parsing MongoDB documents directly
    }