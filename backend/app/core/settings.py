from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class DBSettings(BaseModel):
    url: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/pact"
    echo: bool = False


class Settings(BaseModel):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        case_sensitive=False,
    )

    db: DBSettings = DBSettings()


settings = Settings()
