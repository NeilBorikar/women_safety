from datetime import datetime
from bson import ObjectId


def get_current_time():
    return datetime.utcnow()


def convert_objectid(data):
    """
    Converts MongoDB ObjectId to string
    """
    if data is None:
        return None

    if isinstance(data, list):
        return [convert_objectid(item) for item in data]

    if isinstance(data, dict):
        res = {**data}
        if "_id" in res:
            res["_id"] = str(res["_id"])
            res["id"] = res["_id"]
        return res

    return data





def validate_objectid(id: str):
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)