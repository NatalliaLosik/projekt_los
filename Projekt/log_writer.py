from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime
from urllib.parse import quote_plus

def collection(config) -> Collection:
    args = '&'.join([config["args"], f'authSource={config["authSource"]}']).strip('&')
    uri = "mongodb://%s:%s@%s/?%s" % (
        quote_plus(config["user"]),
        quote_plus(config["password"]),
        config["host"],
        args)
    client = MongoClient(uri)
    db = client[config["db"]]
    collection = db['final_project_100125_Losik']
    return collection

def logRequestKeyword(collection, search_word: str, res_count: int):
    search_type = "keyword"
    params = {"keyword": search_word}    
    log = {
        "timestamp": datetime.now(),
        "search_type": search_type,
        "params": params,
        "results_count": res_count
    }
    collection.insert_one(log)

def logRequestCategory(collection, search_category: str, min_year: int, max_year: int, res_count: int):   
    search_type = "category"
    params = {
        "category": search_category,
        "min_year": min_year,
        "max_year": max_year
    }    
    log = {
        "timestamp": datetime.now(),
        "search_type": search_type,
        "params": params,
        "results_count": res_count
    }
    collection.insert_one(log)
