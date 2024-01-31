from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017")

db = client["db"]

db.test2.insert_one({"test": "test_col"})


data = db.test2.find()
for item in data:
    print(item['test'])