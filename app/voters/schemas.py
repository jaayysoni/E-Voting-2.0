from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ---------------- Base Voter Schema ----------------
class VoterBase(BaseModel):
    """
    Shared fields between create and response schemas.
    """
    name: str
    email: EmailStr

# ---------------- Voter Create Schema ----------------
class VoterCreate(VoterBase):
    """
    Schema for creating a new voter.
    'password' is plaintext received from form and hashed in service.
    """
    password: str
    election_id: str  # must include election_id when creating a voter

# ---------------- Voter Response Schema ----------------
class VoterResponse(VoterBase):
    """
    Schema for returning voter info.
    '_id' stored as string to avoid ObjectId issues.
    """
    id: str = Field(..., alias="_id")  # maps MongoDB '_id' to 'id' in response
    election_id: str
    has_voted: bool = False
    voted_for: Optional[str] = None  # candidate ID if voted
    password_hash: Optional[str] = None  # optional, internal use only

    model_config = {
        "from_attributes": True  # allows Pydantic v2 to parse MongoDB dicts
    }