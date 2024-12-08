"""
    Name; Kenneth
    Date: Whack 23
    Purpose: Write data to the mongodb database that is in the cloud.
"""
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from generateCulture import getCulture
from getRecipes import *
import requests
from bs4 import BeautifulSoup
from random import randrange
from time import sleep

def createEntry(dishNum: int) -> (str,dict):
    """Creates a tuple with (collection, entry) for database """
    URL = f"https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/{dishNum}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    image = getImage(soup)
    ingredients = getIngredients(soup)
    steps = getSteps(soup)
    cuisine, prepTime, source = getCuisinePrepSource(soup)
    dish = getName(soup)
    culture = getCulture(dish)


    collection = cuisine[0]
    entry = {
        "name": dish,
        "image": image,
        "originalRecipe": source,
        'ingredients': ingredients,
        "instructions":steps,
        'cuisine':cuisine[1],
        'cookTime':prepTime,
        'culture':culture,
    }

    return (collection, entry)




def main():

    uri = "mongodb+srv://kxiong:aR8ArPDmKeeQLfdV@recipes.yzed4bm.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api = ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client["World_Recipes"]
    naCol = db["North American"]
    laCol = db["Latin American"]
    asCol = db["Asian"]
    afCol = db["African"]
    euCol = db["European"]
    ocCol = db["Australasian"]

    for i in range(0, 250):
        random = randrange(2675, 100000)
        sleep(20)
        try:
            recipe = createEntry(random)
        except AttributeError:
            continue
        print(f"current run {i}, recipe #{random}")
        if recipe[0] == "North American":
            naCol.insert_one(recipe[1])
        elif recipe[0] == "Latin American":
            laCol.insert_one(recipe[1])
        elif recipe[0] == "Asian":
            asCol.insert_one(recipe[1])
        elif recipe[0] == "African":
            afCol.insert_one(recipe[1])
        elif recipe[0] == "European":
            euCol.insert_one(recipe[1])
        elif recipe[0] == "Australasian":
            ocCol.insert_one(recipe[1])
        else:
            print("missing a region")
            print(recipe[0])
main()
