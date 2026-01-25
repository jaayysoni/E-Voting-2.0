import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

# ----------------------------
# MongoDB configuration (NO HARDCODED SECRETS)
# ----------------------------
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB = os.getenv("MONGO_DB", "evoting_db")
MONGO_URI = os.getenv("MONGO_URI")  # Optional full URI override

# Validate required environment variables
if not MONGO_USER or not MONGO_PASSWORD or not MONGO_CLUSTER:
    raise RuntimeError(
        "❌ Missing MongoDB environment variables. "
        "Make sure MONGO_USER, MONGO_PASSWORD, and MONGO_CLUSTER are set in .env"
    )

# Encode password safely
MONGO_PASSWORD_ENCODED = quote_plus(MONGO_PASSWORD)

# Build connection string if not provided
if not MONGO_URI:
    MONGO_URI = (
        f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD_ENCODED}"
        f"@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority"
    )
    print("ℹ️ Using MongoDB Atlas URI from environment variables")

# ----------------------------
# Connect to MongoDB
# ----------------------------
try:
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    client.admin.command("ping")
    print("✅ Connected to MongoDB successfully")

    db = client[MONGO_DB]

    # Collections
    ec_col = db["ec"]
    voters_col = db["voters"]
    votes_col = db["votes"]
    candidates_col = db["candidates"]

except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    client = db = ec_col = voters_col = votes_col = candidates_col = None
    print("⚠️ App will run, but DB operations will fail")