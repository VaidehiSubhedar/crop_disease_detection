import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["NewDataBase"] 
    collection = db['SampleCollection']
    print("Database connected:", db.name)
    dictionary = {'name' : 'Pranav','marks' :98}
    collection.insert_one(dictionary)