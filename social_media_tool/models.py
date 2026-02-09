"""Domain models for the Social Media Automation Tool."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


class Platform(str, Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    X = "x"
    YOUTUBE = "youtube"


@dataclass(frozen=True)
class Account:
    platform: Platform
    handle: str
    display_name: str
    oauth_token: str


@dataclass(frozen=True)
class Schedule:
    scheduled_at: datetime
    timezone_name: str
    recurring_rule: Optional[str] = None

    def __post_init__(self) -> None:
        if self.scheduled_at.tzinfo is None:
            raise ValueError("scheduled_at must be timezone-aware")


@dataclass
class Post:
    account: Account
    caption: str
    hashtags: List[str]
    media_urls: List[str]
    schedule: Schedule
    platform_variant: Optional[str] = None
    status: str = "draft"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    published_at: Optional[datetime] = None
