from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --------------------------------------------------
    # OpenAI
    # --------------------------------------------------

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5"

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    DATABASE_URL: str = "sqlite:///data/news.db"

    # --------------------------------------------------
    # RSS
    # --------------------------------------------------

    MAX_ARTICLES_PER_SOURCE: int = 2

    # --------------------------------------------------
    # Settings
    # --------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()