"""
SkillHub Skill Registry - Direct implementation of SkillHub-style discovery.
Skills follow the directory/metadata structure of Moltbook.
"""

import json
from enum import Enum
from typing import List, Dict

class SkillHub:
    def __init__(self, session_protocol):
        self.session = session_protocol

    def publish_skill(self, name: str, description: str, commands: List[str]):
        """
        Publishes a skill to the registry (Moltbook SkillHub).
        Mirrors the skill.md metadata structure.
        """
        payload = {
            "SkillHub_v": "1.0",
            "skill": {
                "name": name,
                "description": description,
                "commands": commands,
                "source": f"moltbook://u/{self.session.name}/skills/{name}"
            }
        }
        return self.session.sessions_broadcast(f"Skill: {name}", json.dumps(payload))

    def discover_skills(self, query: str = None) -> List[Dict]:
        """Search for published skills in the network."""
        posts = self.session.client.posts.list(submolt="general", limit=50)
        skills = []
        for p in posts:
            if "Skill:" in p.title:
                payload_str = p.content.split("```json")[-1].split("```")[0].strip()
                try:
                    payload = json.loads(payload_str)
                    if "skill" in payload:
                        skills.append(payload["skill"])
                except:
                    continue
        return skills
