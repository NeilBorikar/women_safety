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
        # Create a copy to avoid mutating the original MongoDB doc if referenced elsewhere
        res = {**data}
        if "_id" in res:
            str_id = str(res["_id"])
            res["_id"] = str_id
            res["id"] = str_id
        
        # Recursively convert nested objects (like emergency_contacts)
        for key, value in res.items():
            if isinstance(value, (dict, list)):
                res[key] = convert_objectid(value)
        
        return res

    return data



def validate_objectid(id: str):
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)