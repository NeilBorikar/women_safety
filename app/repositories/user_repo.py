from app.db.mongodb import user_collection
from app.repositories.base_repo import BaseRepository
from app.utils.exceptions import NotFoundException, BadRequestException


class UserRepository(BaseRepository):

    @staticmethod
    async def create_user(user_data: dict):
        try:
            result = await user_collection.insert_one(user_data)
            return str(result.inserted_id)
        except Exception as e:
            raise BadRequestException(f"Failed to create user: {str(e)}")

    @staticmethod
    async def get_by_email(email: str):
        user = await user_collection.find_one({"email": email})
        return BaseRepository.serialize(user) if user else None

    @staticmethod
    async def get_by_id(user_id: str):
        user = await user_collection.find_one({
            "_id": BaseRepository.to_objectid(user_id)
        })

        if not user:
            raise NotFoundException("User not found")

        return BaseRepository.serialize(user)

    @staticmethod
    async def update_user(user_id: str, update_data: dict):
        result = await user_collection.update_one(
            {"_id": BaseRepository.to_objectid(user_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise NotFoundException("User not found")

        return await UserRepository.get_by_id(user_id)

    @staticmethod
    async def add_emergency_contact(user_id: str, contact: dict):
        if "phone" not in contact:
            raise BadRequestException("Contact must include phone number")

        result = await user_collection.update_one(
            {"_id": BaseRepository.to_objectid(user_id)},
            {"$push": {"emergency_contacts": contact}}
        )

        if result.matched_count == 0:
            raise NotFoundException("User not found")

        return await UserRepository.get_by_id(user_id)