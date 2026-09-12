from dataclasses import dataclass
@dataclass(frozen=True)
class AppSettings:
    service_name: str = "sentinel-api"
    service_version: str = "0.1.0"
SETTINGS = AppSettings()
