import pymongo
import os

class Database(object):

    #URI = "mongodb://127.0.0.1:27017"
    URI = os.environ.get("MONGODB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_database()
        #Database.DATABASE = client.get_default_database()
        #Database.DATABASE = client['heroku_0zrpzv9t']
        #Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def update(collection, data, _id):
        Database.DATABASE[collection].update(_id, data)

    @staticmethod
    def remove(collection, data):
        Database.DATABASE[collection].remove(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def sort(collection, data, type):
        return Database.DATABASE[collection].find(data).sort(type, pymongo.DESCENDING)
