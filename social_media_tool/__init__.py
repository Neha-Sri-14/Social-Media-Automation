"""Social Media Automation Tool core package."""

from .analytics import EngagementMetrics, engagement_rate
from .models import Account, Platform, Post, Schedule
from .scheduler import Scheduler
from .storage import InMemoryPostStore

__all__ = [
    "Account",
    "EngagementMetrics",
    "InMemoryPostStore",
    "Platform",
    "Post",
    "Schedule",
    "Scheduler",
    "engagement_rate",
]
