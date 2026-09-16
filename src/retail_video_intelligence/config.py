"""Safe, side-effect-free, and verifiable configuration."""

import os
from dataclasses import dataclass
from urllib.parse import urlparse

DEFAULT_DATABASE_URL = "postgresql://retail_video:change-me@localhost:5432/retail_video"
DEFAULT_FRIGATE_BASE_URL = "http://localhost:5000"


@dataclass(frozen=True, slots=True)
class Settings:
    database_url: str = DEFAULT_DATABASE_URL
    frigate_base_url: str = DEFAULT_FRIGATE_BASE_URL
    retention_days: int = 30

    @classmethod
    def from_env(cls) -> "Settings":
        raw_retention = os.getenv("RVI_RETENTION_DAYS", "30")
        try:
            retention_days = int(raw_retention)
        except ValueError as exc:
            raise ValueError("RVI_RETENTION_DAYS must be an integer") from exc
        settings = cls(
            database_url=os.getenv("RVI_DATABASE_URL", DEFAULT_DATABASE_URL),
            frigate_base_url=os.getenv("RVI_FRIGATE_BASE_URL", DEFAULT_FRIGATE_BASE_URL),
            retention_days=retention_days,
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if urlparse(self.database_url).scheme not in {"postgresql", "postgres"}:
            raise ValueError("RVI_DATABASE_URL must use postgresql://")
        frigate = urlparse(self.frigate_base_url)
        if frigate.scheme not in {"http", "https"} or not frigate.netloc:
            raise ValueError("RVI_FRIGATE_BASE_URL must be a valid HTTP(S) URL")
        if not 1 <= self.retention_days <= 365:
            raise ValueError("RVI_RETENTION_DAYS must be between 1 and 365")
