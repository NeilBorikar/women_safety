from datetime import datetime
from bson import ObjectId


def get_current_time():
    return datetime.utcnow()


def convert_objectid(data):
    """
    Converts MongoDB ObjectId to string and adds 'id' field
    """
    if data is None:
        return None

    if isinstance(data, list):
        return [convert_objectid(item) for item in data]

    if isinstance(data, dict):
        # Handle current object
        if "_id" in data:
            data["id"] = str(data["_id"])
            data["_id"] = str(data["_id"])
        
        # Handle nested emergency_contacts specifically
        if "emergency_contacts" in data and isinstance(data["emergency_contacts"], list):
            data["emergency_contacts"] = [convert_objectid(c) for c in data["emergency_contacts"]]
            
        return data

    return data




def validate_objectid(id: str):
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)