from pydantic import BaseSettings, Field


class DatabaseConfigModel(BaseSettings):
    engine: str = Field("sqlite+pysqlite", env="DIPPY_DB_ENGINE")
    host: str = Field("", env="DIPPY_DB_HOST")
    username: str = Field("", env="DIPPY_DB_USERNAME")
    password: str = Field("", env="DIPPY_DB_PASSWORD")
    database: str = Field("", env="DIPPY_DB_DATABASE")


class LabelConfigModel(BaseSettings):
    storage: str = Field("memory", env="DIPPY_LABEL_STORAGE")
    database: DatabaseConfigModel = DatabaseConfigModel()
