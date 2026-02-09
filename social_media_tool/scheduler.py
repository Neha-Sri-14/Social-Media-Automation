"""Scheduling logic for automated social media posts."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from .models import Post
from .storage import InMemoryPostStore


class Scheduler:
    def __init__(self, store: InMemoryPostStore) -> None:
        self._store = store

    def schedule_post(self, post_id: str, post: Post) -> None:
        post.status = "scheduled"
        self._store.add(post_id, post)

    def due_posts(self, now: datetime | None = None) -> Iterable[Post]:
        if now is None:
            now = datetime.now(timezone.utc)
        return self._store.due_posts(now)

    def mark_published(self, post_id: str, published_at: datetime | None = None) -> None:
        if published_at is None:
            published_at = datetime.now(timezone.utc)
        post = self._store.get(post_id)
        post.status = "published"
        post.published_at = published_at
        self._store.update(post_id, post)

    def mark_failed(self, post_id: str) -> None:
        post = self._store.get(post_id)
        post.status = "failed"
        self._store.update(post_id, post)
