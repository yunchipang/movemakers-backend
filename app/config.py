from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # database_url: str
    # postgres_db: str
    # postgres_user: str
    # postgres_password: str
    # postgres_host: str
    # postgres_port: str
    # jwt_secret_key: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DATABASE_URL: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")
