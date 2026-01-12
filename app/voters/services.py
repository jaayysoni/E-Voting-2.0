import bcrypt
import uuid
from db.db import voters_col

def register_voter(name, email, password, ec_id):
    if voters_col.find_one({"email": email}):
        return False, "Voter already exists"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    voter = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password_hash": hashed.decode('utf-8'),
        "ec_id": ec_id,
        "voted": False
    }
    voters_col.insert_one(voter)
    return True, "Voter registered"

def login_voter(email, password):
    voter = voters_col.find_one({"email": email})
    if not voter:
        return False, "Voter not found"
    if bcrypt.checkpw(password.encode('utf-8'), voter['password_hash'].encode('utf-8')):
        return True, "Login successful"
    return False, "Invalid password"