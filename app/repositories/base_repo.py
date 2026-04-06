from bson import ObjectId
from app.utils.helpers import convert_objectid, validate_objectid


class BaseRepository:

    @staticmethod
    def to_objectid(id: str) -> ObjectId:
        return validate_objectid(id)

    @staticmethod
    def serialize(data):
        return convert_objectid(data)