from datetime import datetime
from bson import ObjectId


def get_current_time():
    return datetime.utcnow()


def convert_objectid(data):
    """
    Converts MongoDB ObjectId to string
    """
    if isinstance(data, list):
        return [{**item, "_id": str(item["_id"])} for item in data]

    if isinstance(data, dict):
        data["_id"] = str(data["_id"])
        return data

    return data


def validate_objectid(id: str):
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)