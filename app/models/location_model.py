from datetime import datetime


def location_model(location: dict) -> dict:
    return {
        "alert_id": location["alert_id"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timestamp": location.get("timestamp", datetime.utcnow())
    }