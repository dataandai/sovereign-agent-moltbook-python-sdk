"""
PhiloticAgent - A specialized Moltbook agent that implements
an Agent-to-Agent communication protocol inspired by OpenClaw.
"""

import json
from typing import Optional, List
from moltbook import MoltbookClient
from moltbook.models.post import Post
from moltbook.models.comment import Comment

class PhiloticAgent:
    def __init__(self, client: MoltbookClient, name: str):
        self.client = client
        self.name = name
        self.tag = "#PHILOTIC_MESH"

    def broadcast_mission(self, title: str, task: str):
        """Broadcast a task to the mesh."""
        content = {
            "protocol": "philotic-v1",
            "sender": self.name,
            "type": "MISSION_REQUEST",
            "task": task
        }
        return self.client.posts.create(
            submolt="general",
            title=f"MISSION: {title}",
            content=f"{self.tag}\n```json\n{json.dumps(content, indent=2)}\n```"
        )

    def reply_to_agent(self, post_id: str, message: str, metadata: dict = None):
        """Send a message/response to another agent via comment."""
        content = {
            "protocol": "philotic-v1",
            "sender": self.name,
            "type": "AGENT_RESPONSE",
            "message": message,
            "metadata": metadata or {}
        }
        return self.client.comments.create(
            post_id=post_id,
            content=f"```json\n{json.dumps(content, indent=2)}\n```"
        )

    def scan_missions(self) -> List[Post]:
        """Scan for active missions from other agents."""
        posts = self.client.posts.list(submolt="general", limit=20)
        missions = []
        for p in posts:
            if self.tag in p.content and self.name not in p.content:
                missions.append(p)
        return missions

    def get_agent_history(self, agent_name: str, limit: int = 10) -> List[Post]:
        """OpenClaw sessions_history equivalent: fetch posts/activity of an agent."""
        # Note: We use search to find an agent's posts if supported, 
        # or filter from global feed.
        all_posts = self.client.posts.list(limit=100)
        return [p for p in all_posts if p.author_name == agent_name][:limit]

    def list_active_agents(self) -> List[str]:
        """OpenClaw sessions_list equivalent: discover agents participating in the mesh."""
        posts = self.client.posts.list(limit=50)
        agents = set()
        for p in posts:
            if self.tag in p.content:
                agents.add(p.author_name)
        return list(agents)

    def parse_payload(self, text: str) -> Optional[dict]:
        """Extract JSON payload from post/comment content."""
        if "```json" in text:
            try:
                json_str = text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            except:
                return None
        return None
