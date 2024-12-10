from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB connection setup
uri = "mongodb+srv://kxiong:aR8ArPDmKeeQLfdV@cluster0.j0ztq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["page_rank"]  # Replace 'testdb' with your database name
collection = db["webpages"]  # Replace 'testcollection' with your collection name


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get search query from the form
        query = request.form.get("query", "")
        # Fetch data from the MongoDB collection
        results = list(
            collection.aggregate(
                [
                    {"$search": {"text": {"query": query, "path": "fulltext"}}},
                    {
                        "$project": {
                            "_id": 0,
                            "url": 1,
                            "title": 1,
                            "rank": 1,
                            "score": {"$meta": "searchScore"},
                        }
                    },
                    {"$sort": {"rank": 1}},
                ],
            )
        )  # Exclude the '_id' field for simplicity
        return render_template("index.html", query=query, results=results)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
