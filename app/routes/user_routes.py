from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserUpdate, AddEmergencyContact
from app.services.auth_service import AuthService
from app.repositories.user_repo import UserRepository
from app.core.security import verify_token
from app.utils.response import success_response

router = APIRouter()


@router.get("/me")
async def get_profile(user=Depends(verify_token)):
    user_data = await UserRepository.get_by_id(user["user_id"])
    return success_response(user_data)


@router.put("/update")
async def update_user(data: UserUpdate, user=Depends(verify_token)):
    updated = await UserRepository.update_user(user["user_id"], data.dict(exclude_none=True))
    return success_response(updated, "User updated")


@router.post("/add-contact")
async def add_contact(data: AddEmergencyContact, user=Depends(verify_token)):
    updated = await UserRepository.add_emergency_contact(
        user["user_id"],
        data.contact.dict()
    )
    return success_response(updated, "Contact added")


@router.delete("/contact/{contact_id}")
async def delete_contact(contact_id: str, user=Depends(verify_token)):
    updated = await UserRepository.delete_emergency_contact(
        user["user_id"],
        contact_id
    )
    return success_response(updated, "Contact deleted")