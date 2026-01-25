import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env
load_dotenv()

# ----------------------------
# MongoDB configuration
# ----------------------------
MONGO_USER = os.getenv("MONGO_USER", "jaayysoni_db_user")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "Jay4801")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER", "cluster1.15omtbj.mongodb.net")
MONGO_DB = os.getenv("MONGO_DB", "evoting_db")
MONGO_URI = os.getenv("MONGO_URI")  # Optional: full URI from .env

# URL-encode the password to handle special characters safely
MONGO_PASSWORD_ENCODED = quote_plus(MONGO_PASSWORD)

# Construct the connection URI if not provided
if not MONGO_URI:
    MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD_ENCODED}@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority"
    print("ℹ️ Using MongoDB Atlas URI constructed from .env variables")

# ----------------------------
# Connect to MongoDB
# ----------------------------
try:
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    client.admin.command('ping')  # Test connection
    print("✅ Connected to MongoDB successfully")

    # Select database
    db = client[MONGO_DB]

    # Collections
    ec_col = db["ec"]
    voters_col = db["voters"]
    votes_col = db["votes"]
    candidates_col = db["candidates"]

except Exception as e:
    print(f"❌ Could not connect to MongoDB: {e}")
    client = db = ec_col = voters_col = votes_col = candidates_col = None
    print("⚠️ App will still run, but DB operations will fail until MongoDB is available")