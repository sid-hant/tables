import pymongo
import os

class Database(object):

    URI= os.environ.get("MONGOLAB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

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
