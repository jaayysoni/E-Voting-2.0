from pydantic import BaseModel
from datetime import datetime

class VoteModel(BaseModel):
    voter_id: str
    ec_id: str
    candidate: str
    timestamp: datetime