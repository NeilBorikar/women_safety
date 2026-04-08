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
        # Create a clean shallow copy to avoid side effects
        res = {**data}
        if "_id" in res:
            obj_id_str = str(res["_id"])
            res["_id"] = obj_id_str
            res["id"] = obj_id_str
            
        # Specific handling for the emergency contacts list if it exists
        if "emergency_contacts" in res and isinstance(res["emergency_contacts"], list):
            res["emergency_contacts"] = [convert_objectid(c) for c in res["emergency_contacts"]]

        # Handle datetimes and other nested objects
        for key, value in res.items():
            if isinstance(value, datetime):
                res[key] = value.isoformat()
            elif isinstance(value, (dict, list)) and key != "emergency_contacts":
                res[key] = convert_objectid(value)
            
        return res

    return data






def validate_objectid(id: str):
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)