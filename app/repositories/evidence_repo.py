from app.db.mongodb import database
from app.repositories.base_repo import BaseRepository

evidence_collection = database["evidence"]


class EvidenceRepository(BaseRepository):

    @staticmethod
    async def add_evidence(evidence_data: dict):
        result = await evidence_collection.insert_one(evidence_data)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_alert(alert_id: str):
        evidence = evidence_collection.find({"alert_id": alert_id})
        return BaseRepository.serialize([e async for e in evidence])