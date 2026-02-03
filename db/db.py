import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables (.env for local, Render/AWS env vars in prod)
load_dotenv()

# ----------------------------
# MongoDB configuration
# ----------------------------
MONGO_URI = os.getenv("MONGO_URI")  # REQUIRED
MONGO_DB = os.getenv("MONGO_DB", "evoting_db")

# Initialize defaults (prevents import crashes)
client = None
db = None
ec_col = None
voters_col = None
votes_col = None
candidates_col = None

if not MONGO_URI:
    print("❌ MONGO_URI not set. Database is disabled.")
else:
    try:
        client = MongoClient(
            MONGO_URI,
            tls=True,
            serverSelectionTimeoutMS=5000
        )

        # Force connection test on startup
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
        print("⚠️ App will run, but DB operations will fail")