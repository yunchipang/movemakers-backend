from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    TEST_POSTGRES_DB: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")
