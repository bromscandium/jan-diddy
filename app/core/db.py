from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    DATABASE_URL: str

    @property
    def url(self) -> str:
        return self.DATABASE_URL.replace("postgresql://", "postgres://")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_nested_delimiter="__")


db_settings = DBSettings()  # type: ignore
