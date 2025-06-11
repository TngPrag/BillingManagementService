from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Print for debug
#print("Current working directory:", os.getcwd())

# Load .env file
env_path = os.path.join(os.getcwd(), ".env")
#print("Loading .env from:", env_path)
load_dotenv(env_path)

class Settings(BaseSettings):
    ENV: str
    APP_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SMTP_USER: str
    SMTP_PASS: str

    class Config:
        env_file = "../.env"

settings = Settings()

# Debug print
#print("ENV =", settings.ENV)
#print("APP_PORT =", settings.APP_PORT)
