import bcrypt
import uuid
from db.db import ec_col

def register_ec(name: str, email: str, password: str):
    # Check if email already exists
    if ec_col.find_one({"email": email}):
        return False, "EC already exists"

    # Hash password
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Generate unique election ID
    election_id = str(uuid.uuid4())

    ec = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password_hash": hashed.decode("utf-8"),
        "election_id": election_id,
        "start_time": None,
        "end_time": None
    }

    ec_col.insert_one(ec)
    return True, election_id