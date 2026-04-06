def notification_model(notification: dict) -> dict:
    return {
        "user_id": notification["user_id"],
        "alert_id": notification["alert_id"],
        "recipient_email": notification["recipient_email"],
        "message": notification["message"],
        "channel": notification.get("channel"),
        "status": notification.get("status", "sent"),
        "created_at": datetime.utcnow()
    }