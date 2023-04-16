import base64
import pymongo
import os


class MongoDBSingleton:
    """
    Singleton class which persists the MongoClient connection throughout the lifecycle
    of the application.
    """
    __instance = None

    @staticmethod
    def get_instance():
        if MongoDBSingleton.__instance is None:
            MongoDBSingleton()
        return MongoDBSingleton.__instance

    def __init__(self):
        if MongoDBSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            mongo_uri_encoded = os.environ.get('MONGO_URI_PROD_ENCODED', 'bW9uZ29kYjovL2xvY2FsaG9zdDoyNzAxOQ==')
            mongo_uri = base64.b64decode(mongo_uri_encoded).decode('utf-8')
            MongoDBSingleton.__instance = pymongo.MongoClient(mongo_uri_encoded)
