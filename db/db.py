from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["evoting_db"]

ec_col = db["ec"]
voters_col = db["voters"]
votes_col = db["votes"]
candidates_col = db["candidates"]