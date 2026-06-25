from pymongo import MongoClient

_client = MongoClient("mongodb://localhost:27017/",tz_aware = True)
_db = _client["study_pal_database"]

def get_collection(collection_name:str):
    return _db[collection_name]



