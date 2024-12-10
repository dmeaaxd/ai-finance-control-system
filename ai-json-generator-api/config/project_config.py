from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    OPENAI_KEY: str
    OPENAI_MODEL: str


settings = Settings()
