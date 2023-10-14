from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    jwt_secret_key: str
    app_name: str

    model_config = SettingsConfigDict(env_file=".env")
