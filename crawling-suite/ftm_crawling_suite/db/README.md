# Copyright FTM 2020

# This database class is a singleton which is intended to persist the connection with the MongoDB database
# between pipelines and throughout the lifecycle of the application. It is generally not the preferred
# method to create a MongoClient instance, and rather you should use the getInstance method on this Singleton.