from pydantic import BaseModel, EmailStr
from typing import Optional

# Base fields shared by create & response
class VoterBase(BaseModel):
    name: str
    email: EmailStr

# Input schema for creating a voter
class VoterCreate(VoterBase):
    password: str  # plaintext password received from form

# Output schema for returning voter info (API or internal)
class VoterResponse(VoterBase):
    id: str
    election_id: str
    has_voted: bool = False
    # password_hash is optional here, can be included internally if needed
    password_hash: Optional[str] = None