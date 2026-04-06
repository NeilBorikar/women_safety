from datetime import datetime


def evidence_model(evidence: dict) -> dict:
    return {
        "alert_id": evidence["alert_id"],
        "file_type": evidence["file_type"],
        "file_url": evidence["file_url"],
        "timestamp": evidence.get("timestamp", datetime.utcnow())
    }