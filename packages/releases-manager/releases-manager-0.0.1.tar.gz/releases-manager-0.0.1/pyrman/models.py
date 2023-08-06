from dataclasses import dataclass
from datetime import datetime


@dataclass
class Package:
    title: str
    description: str
    last_released: datetime
    package_url: str
    releases_url: str


@dataclass
class Release:
    version: str
    release_date: datetime
