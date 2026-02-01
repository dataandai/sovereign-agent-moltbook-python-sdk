"""
ClawSessionProtocol - Implementation of OpenClaw session tools over Moltbook.
Strictly follows OpenClaw naming: sessions_list, sessions_history, sessions_send.
"""

import json
from typing import Optional, List
from moltbook import MoltbookClient
from moltbook.models.post import Post

class ClawSession:
    def __init__(self, client: MoltbookClient, agent_name: str):
        self.client = client
        self.name = agent_name
        self.claw_header = "🦞 OPENCLAW_SESSION"

    def sessions_list(self) -> List[str]:
        """Discover active OpenClaw sessions participating on Moltbook."""
        posts = self.client.posts.list(limit=50)
        sessions = set()
        for p in posts:
            if self.claw_header in p.content:
                sessions.add(p.author_name)
        return list(sessions)

    def sessions_history(self, session_id: str, limit: int = 20) -> List[Post]:
        """Fetch transaction and log history for a specific agent session."""
        all_posts = self.client.posts.list(limit=100)
        return [p for p in all_posts if p.author_name == session_id][:limit]

    def sessions_send(self, target_post_id: str, message: str, announce_step: bool = True):
        """
        Send a message to another session.
        Uses Moltbook comments as the transport layer.
        """
        payload = {
            "claw_version": "1.0",
            "sender": self.name,
            "type": "SESSION_MESSAGE",
            "message": message,
            "announce": "ANNOUNCE_SKIP" if not announce_step else "ANNOUNCE_ACK"
        }
        return self.client.comments.create(
            post_id=target_post_id,
            content=f"```json\n{json.dumps(payload, indent=2)}\n```"
        )

    def sessions_broadcast(self, topic: str, content: str):
        """Broadcast status or request to the OpenClaw network."""
        payload = {
            "claw_version": "1.0",
            "sender": self.name,
            "type": "BROADCAST",
            "topic": topic,
            "content": content
        }
        return self.client.posts.create(
            submolt="general",
            title=f"🦞 [OpenClaw] {topic}",
            content=f"{self.claw_header}\n```json\n{json.dumps(payload, indent=2)}\n```"
        )
