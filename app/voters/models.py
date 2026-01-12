from pydantic import BaseModel

class VoterBase(BaseModel):
    name: str
    email: str
    password: str
    ec_id: str

class VoterLogin(BaseModel):
    email: str
    password: str

class VoterResponse(BaseModel):
    name: str
    email: str
    voted: bool
    ec_id: str