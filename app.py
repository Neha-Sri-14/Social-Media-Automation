"""Streamlit UI preview for the Social Media Automation Tool."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import streamlit as st

from social_media_tool import (
    Account,
    EngagementMetrics,
    InMemoryPostStore,
    Platform,
    Post,
    Schedule,
    Scheduler,
    engagement_rate,
)


st.set_page_config(page_title="Social Media Automation Tool", page_icon="📣", layout="wide")

st.title("📣 Social Media Automation Tool")
st.caption(
    "Plan, schedule, and analyze content across your social channels from one place."
)

store = InMemoryPostStore()
scheduler = Scheduler(store)


def build_sample_posts() -> None:
    base_time = datetime.now(timezone.utc) + timedelta(hours=2)
    account = Account(
        platform=Platform.INSTAGRAM,
        handle="@creator",
        display_name="Creator",
        oauth_token="secure-token",
    )
    for offset, caption in enumerate(
        ["Launch teaser", "Product highlights", "Behind the scenes"], start=1
    ):
        schedule = Schedule(
            scheduled_at=base_time + timedelta(hours=offset),
            timezone_name="UTC",
        )
        post = Post(
            account=account,
            caption=caption,
            hashtags=["#launch", "#creator"],
            media_urls=["https://example.com/asset.jpg"],
            schedule=schedule,
        )
        scheduler.schedule_post(f"post-{offset}", post)


build_sample_posts()

with st.sidebar:
    st.header("Queue Controls")
    preview_time = st.slider("Preview time (hours from now)", 0, 6, 2)
    preview_timestamp = datetime.now(timezone.utc) + timedelta(hours=preview_time)
    st.write("Preview timestamp:")
    st.code(preview_timestamp.isoformat())

    if st.button("Mark first due post as published"):
        due_posts = list(scheduler.due_posts(preview_timestamp))
        if due_posts:
            scheduler.mark_published("post-1")
            st.success("Marked post-1 as published.")
        else:
            st.info("No posts are due yet.")

st.subheader("Scheduled Queue")

queue_rows = []
for post in store.list_all():
    queue_rows.append(
        {
            "Post ID": post.caption.lower().replace(" ", "-")[:10],
            "Platform": post.account.platform.value,
            "Handle": post.account.handle,
            "Caption": post.caption,
            "Scheduled (UTC)": post.schedule.scheduled_at.strftime("%Y-%m-%d %H:%M"),
            "Status": post.status,
        }
    )

st.dataframe(queue_rows, use_container_width=True)

st.subheader("Next Posts Preview")

for post in scheduler.due_posts(preview_timestamp):
    with st.container():
        st.markdown(f"**{post.caption}**")
        st.write(f"Scheduled for {post.schedule.scheduled_at.strftime('%Y-%m-%d %H:%M UTC')}")
        st.write(f"Status: {post.status}")
        st.divider()

st.subheader("Engagement Snapshot")

col1, col2, col3 = st.columns(3)
metrics = EngagementMetrics(impressions=12500, reach=9800, likes=860, shares=140)

col1.metric("Impressions", f"{metrics.impressions:,}")
col2.metric("Reach", f"{metrics.reach:,}")
col3.metric("Engagement Rate", f"{engagement_rate(metrics) * 100:.2f}%")

st.subheader("Publishing Timeline")

st.write(
    "Posts move from draft to scheduled, then publishing, with retries and analytics capture."
)

st.markdown(
    \"\"\"\n1. **Draft** — Post created and saved.\n2. **Scheduled** — Queued with timezone-aware timestamp.\n3. **Publishing** — Background worker pushes to platform.\n4. **Success/Retry** — Status updated and retries handled.\n5. **Reported** — Engagement metrics collected.\n\"\"\"\n)
