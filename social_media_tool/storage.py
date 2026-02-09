"""In-memory storage for scheduled posts."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List

from .models import Post


class InMemoryPostStore:
    def __init__(self) -> None:
        self._posts: Dict[str, Post] = {}

    def add(self, post_id: str, post: Post) -> None:
        if post_id in self._posts:
            raise ValueError(f"post_id {post_id!r} already exists")
        self._posts[post_id] = post

    def get(self, post_id: str) -> Post:
        try:
            return self._posts[post_id]
        except KeyError as exc:
            raise KeyError(f"post_id {post_id!r} not found") from exc

    def update(self, post_id: str, post: Post) -> None:
        if post_id not in self._posts:
            raise KeyError(f"post_id {post_id!r} not found")
        self._posts[post_id] = post

    def list_all(self) -> List[Post]:
        return list(self._posts.values())

    def due_posts(self, now: datetime) -> Iterable[Post]:
        return (
            post
            for post in self._posts.values()
            if post.schedule.scheduled_at <= now and post.status == "scheduled"
        )
