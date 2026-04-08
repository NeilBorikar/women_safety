from app.repositories.user_repo import UserRepository
from app.models.user_model import user_model
from app.core.hashing import hash_password, verify_password
from app.core.security import create_access_token
from app.utils.exceptions import BadRequestException, UnauthorizedException


class AuthService:

    @staticmethod
    async def register(user_data):
        # 🔍 Normalize email
        clean_email = user_data.email.lower().strip()
        
        # 🔍 Check existing user
        existing_user = await UserRepository.get_by_email(clean_email)
        if existing_user:
            raise BadRequestException("User already exists")

        # 🔐 Hash password
        hashed_password = hash_password(user_data.password)

        # 🧱 Prepare data
        user_dict = user_data.dict()
        user_dict["email"] = clean_email
        user_dict["password"] = hashed_password

        new_user = user_model(user_dict)

        # 💾 Save to DB
        user_id = await UserRepository.create_user(new_user)

        # 🔐 Generate token
        token = create_access_token({
            "user_id": user_id,
            "email": clean_email
        })

        return {
            "access_token": token,
            "user": {
                "id": user_id,
                "name": user_data.name,
                "email": clean_email
            },
            "message": "User registered successfully"
        }

    @staticmethod
    async def login(user_data):
        clean_email = user_data.email.lower().strip()
        print(f"DEBUG: Attempting login for email: [{clean_email}]")
        
        user = await UserRepository.get_by_email(clean_email)

        if not user:
            print("DEBUG: User not found in database")
            raise UnauthorizedException("Invalid credentials")

        print(f"DEBUG: User found. Comparing passwords...")
        if not verify_password(user_data.password, user["password"]):
            print("DEBUG: Password verification failed")
            raise UnauthorizedException("Invalid credentials")

        print("DEBUG: Login successful. Generating token...")
        # 🔐 Generate token
        token = create_access_token({
            "user_id": user["id"],
            "email": user["email"]
        })


        return {
            "access_token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }