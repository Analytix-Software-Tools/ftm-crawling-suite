import base64
import pymongo
import pydotenv

env = pydotenv.Environment()


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
            mongo_uri_encoded = env['MONGO_URI_PROD_ENCODED'] if env['ENVIRONMENT'] == 'production' else env[
                'MONGO_URI_DEV_ENCODED']
            # mongo_uri = base64.b64decode(mongo_uri_encoded)
            MongoDBSingleton.__instance = pymongo.MongoClient(mongo_uri_encoded)
