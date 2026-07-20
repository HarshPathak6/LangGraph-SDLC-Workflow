from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str
    DATABASE_URL: str
    # GEMINI_API_KEY: str
    # GEMINI_MODEL: str
    # GROQ_MODEL: str
    # GROQ_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()