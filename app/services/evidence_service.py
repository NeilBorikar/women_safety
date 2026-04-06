from app.repositories.evidence_repo import EvidenceRepository
from app.models.evidence_model import evidence_model


class EvidenceService:

    @staticmethod
    async def upload_evidence(evidence_data):
        evidence_dict = evidence_data.dict()

        new_evidence = evidence_model(evidence_dict)

        evidence_id = await EvidenceRepository.add_evidence(new_evidence)

        return {
            "evidence_id": evidence_id
        }

    @staticmethod
    async def get_evidence(alert_id: str):
        return await EvidenceRepository.get_by_alert(alert_id)