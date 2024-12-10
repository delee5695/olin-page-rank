"""
Description: Write page rank index and website description to a mongoDB database
Name: Kenneth
Date: Discrete 2024
"""

import requests
from rank_pages import rank_pages
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def get_page_text(url):
    # Send a GET request to the URL
    print(f"Getting contents of {url}")
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.find_all("p")
            # Parse the HTML content of the page
            return [str(text), soup.title.text]

        else:
            return [url, url]
    except Exception as e:
        return [url, url]


def main():
    uri = "mongodb+srv://kxiong:aR8ArPDmKeeQLfdV@cluster0.j0ztq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi("1"))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # open  database on MongoDb
    collection = client["page_rank"]
    database = collection["webpages"]
    ranked_pages_list = rank_pages("./outlinks-dict.pickle", 0.15)
    for page, rank in ranked_pages_list:
        site_info = get_page_text(page)
        print(site_info)
        page_entry = {
            "url": page,
            "rank": rank + 1,
            "title": site_info[1],
            "fulltext": site_info[0],
        }
        print(f"Adding {page} to database\n")
        database.insert_one(page_entry)


main()
