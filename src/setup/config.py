from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, field_validator
from pydantic import PostgresDsn, SecretStr
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class JwtAuthConfig(BaseModel):
    secret_key: Path = BASE_DIR / "certificates" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certificates" / "jwt-public.pem"
    algorithm: str
    access_token_expire_minutes: int

    @field_validator("algorithm")
    def validate_algorithm(cls, value: str) -> str:
        allowed: list[str] = [
            "RS256",
            "RS2048",
        ]

        if value in allowed:
            return value
        else:
            raise ValueError(
                f"""Current algorithm "{value}" is not allowed. Allowed: f{", ".join(allowed)}"""
            )

    @field_validator("access_token_expire_minutes")
    def validate_access_expire(cls, value: int) -> int:
        expire_min_time: int = 5
        expire_max_time: int = 24 * 60
        if expire_min_time <= value <= expire_max_time:
            return value
        else:
            raise ValueError("Expire time must be between 5 minutes and 24 hours")


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env_app",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig
    auth: JwtAuthConfig


settings = Settings()
print(settings.auth)
