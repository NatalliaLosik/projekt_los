from pymongo import MongoClient
from datetime import datetime

client = MongoClient(
    "mongodb://ich_editor:verystrongpassword"
    "@mongo.itcareerhub.de/?readPreference=primary"
    "&ssl=false&authMechanism=DEFAULT&authSource=ich_edit")
db = client["ich_edit"]
collection = db['final_project_100125_Losik']

def log_request_keyword(search_word: str, res_count: int):
    search_type = "keyword"
    params = {"keyword": search_word}    
    log = {
        "timestamp": datetime.now(),
        "search_type": search_type,
        "params": params,
        "results_count": res_count
    }
    collection.insert_one(log)

def log_request_category(search_category: str, min_year: int, max_year: int, res_count: int):   
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
