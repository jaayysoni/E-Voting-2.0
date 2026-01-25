import os
from dotenv import load_dotenv
from pymongo import MongoClient  # type: ignore

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from environment or fallback to default
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("⚠️ MONGO_URI not found in .env, using default localhost")
    MONGO_URI = "mongodb://127.0.0.1:27017"

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    # Ping the server to check connection
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully")

    # Select database
    db = client["evoting_db"]

    # Collections
    ec_col = db["ec"]
    voters_col = db["voters"]
    votes_col = db["votes"]
    candidates_col = db["candidates"]

except Exception as e:
    print(f"❌ Could not connect to MongoDB: {e}")
    client = None
    db = None
    ec_col = None
    voters_col = None
    votes_col = None
    candidates_col = None
    print("⚠️ App will still run, but DB operations will fail until MongoDB is available")