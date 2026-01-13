from pydantic import BaseModel

class VoteBase(BaseModel):
    voter_id: str
    election_id: str
    candidate_id: str

class VoteResponse(BaseModel):
    message: str
    vote_token: str