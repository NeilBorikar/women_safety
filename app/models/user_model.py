from datetime import datetime


def user_model(user: dict) -> dict:
    return {
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],  # already hashed
        "emergency_contacts": user.get("emergency_contacts") or [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True
    }