from datetime import datetime


def alert_model(alert: dict) -> dict:
    return {
        "user_id": alert["user_id"],
        "status": "active",
        "latitude": alert["latitude"],
        "longitude": alert["longitude"],
        "device_id": alert.get("device_id"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_resolved": False
    }