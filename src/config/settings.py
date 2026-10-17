from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ApiPrefix(BaseModel):
    v1_prefix: str = "/v1"
    healthcheck: str = "/healthcheck"


class ApiConf(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class LogConf(BaseModel):
    format: str = (
        "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    )


class DatabaseConf(BaseModel):
    url: PostgresDsn
    echo: bool = False
    # echo: bool = True


class JWTConf(BaseModel):
    public_key_path: Path
    algorithm: str = "RS256"

    @cached_property
    def public_key(self) -> str:
        return (BASE_DIR / self.public_key_path).read_text()


class Redis(BaseModel):
    url: RedisDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        frozen=True,
        env_prefix="CONFIG__",
        extra="ignore",
    )

    api_prefix: ApiPrefix = ApiPrefix()
    api_conf: ApiConf = ApiConf()
    logging_conf: LogConf = LogConf()
    db: DatabaseConf
    jwt: JWTConf
    redis: Redis


settings = Settings()
