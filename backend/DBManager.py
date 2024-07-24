from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDB:
    def __init__(self):
        self.CLIENT = None
        self.DB = None 
        self.COLLECTION = ''

    def connect(self, uri, dbName, collection):
        try:
            self.CLIENT = MongoClient(uri)
            self.DB = self.CLIENT[dbName]
            self.COLLECTION = self.DB[collection]
            print("CONNECTED TO MONGO_DB ATLAS")
        except ConnectionFailure as e:
            print(f"COULD NOT CONNECTED TO MONGO_DB ATLAS: {e}")

    def disconnect(self):
        if self.CLIENT:
            self.CLIENT.close()
            print("DISCONNECTED FROM MONGO_DB ATLAS")

    def retrieveData(self, plateNo, password):
        for DATA in self.COLLECTION.find({"plateNo" : plateNo, "password" : password}): # type: ignore
            return DATA
        
    def updateData(self, plateNo, password, newValues):
        self.COLLECTION.update_one({"plateNo" : plateNo, "password" : password}, {"$set": newValues})
    