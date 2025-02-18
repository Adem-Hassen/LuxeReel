import json

from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")
  
db = client["movies"]                        
collection = db["movies_listings"]                     


with open("../Recommendation_System/dataset/movies.json", "r") as file:
    data = json.load(file)


if isinstance(data, list):
    collection.insert_many(data)  
else:
    collection.insert_one(data)   


 
