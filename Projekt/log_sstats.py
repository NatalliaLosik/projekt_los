from datetime import datetime
from typing import List, Dict, Any
from pymongo.collection import Collection


def getFrequencyTop5(collection: Collection) -> List[Dict[str, Any]]:
    query_frequency5 = [
        {
            "$group": {
                "_id": [
                    "$search_type",
                    "$params.keyword",
                    "$params.category",
                    "$params.min_year",
                    "$params.max_year"
                ],
                "count": { "$sum": 1 }
            }
        },
        { "$sort": { "count": -1 } },
        { "$limit": 5 }
    ]
    query_results = list(collection.aggregate(query_frequency5))
    results = []
    for i, res in enumerate(query_results, 1):
        results += [{
            "num": i,
            "search_type": res["_id"][0],
            "keyword": res["_id"][1],
            "category": res["_id"][2],
            "min_year": res["_id"][3],
            "max_year": res["_id"][4],
            "count": res["count"]
        }]
    return results

def getLatestTop5(collection: Collection) -> List[Dict[str, Any]]:
    query_last5 = [
        {
            "$project": {
                "search_type": 1,
                "timestamp": 1,
                "params": 1
            }
        },
        { "$sort": { "timestamp": -1 } },
        { "$limit": 5 }
    ]
    query_results = list(collection.aggregate(query_last5))
    results = []
    for i, res in enumerate(query_results, 1):
        results += [{
            "num": i,
            "search_type": res["search_type"],
            "timestamp": res["timestamp"],
            "keyword": res["params"].get("keyword"),
            "category": res["params"].get("category"),
            "min_year": res["params"].get("min_year"),
            "max_year": res["params"].get("max_year")
        }]
    return results