#db_connection.py
from pymongo import MongoClient

def get_db_collection():
    """
    Establishes a connection to the MongoDB database and returns the collection object.
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['avani_test']
    collection = db['test']
    return collection
def get_backup_db_collection():
    """
    Establishes a connection to the MongoDB database and returns the collection object.
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['avani_backup']
    collection = db['backup']
    return collection