"""Analytics helpers for engagement metrics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngagementMetrics:
    impressions: int
    reach: int
    likes: int
    shares: int

    @property
    def total_engagements(self) -> int:
        return self.likes + self.shares


def engagement_rate(metrics: EngagementMetrics) -> float:
    if metrics.impressions <= 0:
        return 0.0
    return metrics.total_engagements / metrics.impressions
