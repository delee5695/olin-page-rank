from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# MongoDB connection setup
uri = "mongodb+srv://kxiong:aR8ArPDmKeeQLfdV@cluster0.j0ztq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["page_rank"]  # Replace 'testdb' with your database name
collection = db["webpages"]  # Replace 'testcollection' with your collection name


# Fetch data from the MongoDB collection
data = list(
    collection.aggregate(
        [
            {"$search": {"text": {"query": "amon milner", "path": "fulltext"}}},
            {
                "$project": {
                    "_id": 0,
                    "title": 1,
                    "rank": 1,
                    "score": {"$meta": "searchScore"},
                }
            },
            {"$sort": {"rank": 1}},
        ],
    )
)  # Exclude the '_id' field for simplicity

print(data)
