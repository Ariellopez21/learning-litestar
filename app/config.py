from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    database_url: str = "sqlite:///db.sqlite3"
    secret_key: SecretStr = SecretStr("secret123")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()