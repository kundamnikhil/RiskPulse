from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Keep this aligned with .env.example
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/riskpulse"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
