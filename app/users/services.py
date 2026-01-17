# app/users/services.py

import bcrypt
import uuid
from db.db import ec_col
from datetime import datetime

# -------------------- REGISTER EC --------------------
def register_ec(name: str, email: str, password: str):
    """
    Register a new Election Commissioner (EC) with an embedded election object.
    """
    # Check if email already exists
    if ec_col.find_one({"email": email}):
        return False, "EC with this email already exists"

    # Hash password
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Generate unique IDs
    ec_id = str(uuid.uuid4())           # EC document _id
    election_id = str(uuid.uuid4())     # Unique election ID

    # Create EC document with embedded election
    ec_doc = {
        "_id": ec_id,
        "name": name,
        "email": email,
        "password_hash": hashed.decode("utf-8"),
        "election_id": election_id,
        "election": {
            "name": "",                 # Will be set later
            "start_date": None,
            "end_date": None,
            "status": "Upcoming",       # Upcoming / Ongoing / Ended
            "winner": None,
            "candidates": []            # List of candidates
        }
    }

    # Insert EC document into DB
    ec_col.insert_one(ec_doc)

    return True, election_id


# -------------------- CREATE ELECTION --------------------
def create_election(election_id: str, name: str, start_date: datetime, end_date: datetime):
    """
    Update the election details for an EC.
    """
    result = ec_col.update_one(
        {"election_id": election_id},
        {"$set": {
            "election.name": name,
            "election.start_date": start_date,
            "election.end_date": end_date,
            "election.status": "Upcoming"
        }}
    )
    return result.modified_count > 0


# -------------------- ADD CANDIDATE --------------------
def add_candidate(election_id: str, name: str, party: str, moto: str = None, profile_pic: str = None):
    """
    Add a candidate to the EC's election, including profile picture path.
    """
    candidate_id = str(uuid.uuid4())

    # Store relative path only, default GIF
    candidate = {
        "_id": candidate_id,
        "name": name,
        "party": party,
        "moto": moto,
        "profile_pic": profile_pic or "uploads/candidates/default.gif",  # default candidate GIF
        "party_symbol": "uploads/party/party_default.gif"                 # default party GIF
    }

    result = ec_col.update_one(
        {"election_id": election_id},
        {"$push": {"election.candidates": candidate}}
    )

    if result.modified_count:
        return True, candidate_id
    return False, "Failed to add candidate"


# -------------------- REMOVE CANDIDATE --------------------
def remove_candidate(election_id: str, candidate_id: str):
    """
    Remove a candidate from the EC's election.
    """
    result = ec_col.update_one(
        {"election_id": election_id},
        {"$pull": {"election.candidates": {"_id": candidate_id}}}
    )
    return result.modified_count > 0


# -------------------- FETCH DASHBOARD --------------------
def get_ec_dashboard(election_id: str):
    """
    Fetch EC document with embedded election and candidates for dashboard rendering.
    """
    ec = ec_col.find_one({"election_id": election_id})
    if not ec:
        return None

    from db.db import voters_col
    voters = list(voters_col.find({"election_id": election_id}))

    total_voters = len(voters)
    votes_cast = sum(1 for v in voters if v.get("has_voted"))

    # Ensure all candidates have profile_pic and party_symbol
    candidates = []
    for c in ec["election"]["candidates"]:
        candidate_copy = c.copy()
        candidate_copy["profile_pic"] = f"/static/{c.get('profile_pic') or 'uploads/candidates/default.gif'}"
        candidate_copy["party_symbol"] = f"/static/{c.get('party_symbol') or 'uploads/party/party_default.gif'}"
        candidates.append(candidate_copy)

    return {
        "ec": ec,
        "voters": voters,
        "total_voters": total_voters,
        "votes_cast": votes_cast,
        "candidates": candidates
    }