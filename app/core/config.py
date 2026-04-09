from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 🔐 JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # 📧 SMTP
    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL: str
    EMAIL_PASSWORD: str

    # 🗄️ DB
    MONGO_URL: str

    # 🔒 Security
    BCRYPT_ROUNDS: int = 12

    #sms
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()