import pymongo


def database_access():
    client = pymongo.MongoClient("mongodb://3.111.227.206:5001/")
    # client = pymongo.MongoClient("mongodb://localhost:27017")
    database = client['DMS']
    return database
