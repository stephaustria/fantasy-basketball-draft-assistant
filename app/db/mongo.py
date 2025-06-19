from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["fantasy_draft"]
drafted_collection = db["drafted_players"]
scoring_collection = db["scoring_weights"]

default_weights = {
    "PTS": 1.0, "FG": 2.0, "FGA": -1.0, "FT": 1.0, "FTA": -1.0,
    "3P": 1.0, "TRB": 1.0, "AST": 2.0, "STL": 4.0, "BLK": 4.0, "TOV": -2.0
}

# Set default weights on startup if not present
if scoring_collection.count_documents({}) == 0:
    scoring_collection.insert_one({"weights": default_weights})
