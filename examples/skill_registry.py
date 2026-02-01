"""
Skill Registry & Delegation Protocol.
Enables the Sovereign Agent to discover capabilities of other agents and delegate tasks.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

if TYPE_CHECKING:
    from moltbook import MoltbookClient

# ============================================================================
# SKILL DEFINITIONS
# ============================================================================

@dataclass
class AgentSkill:
    """Represents a capability that an agent possesses."""
    name: str                      # e.g., "code_generation", "email_sending"
    description: str               # Human-readable description
    commands: List[str] = field(default_factory=list)  # Specific commands/tools
    confidence: float = 1.0        # 0.0 - 1.0 self-reported proficiency
    tags: List[str] = field(default_factory=list)      # Categorization tags

@dataclass
class RegisteredAgent:
    """An agent registered in the skill network."""
    agent_id: str
    name: str
    skills: List[AgentSkill] = field(default_factory=list)
    status: str = "online"         # online, busy, offline
    last_seen: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

# ============================================================================
# SKILL REGISTRY
# ============================================================================

class SkillRegistry:
    """
    Central registry for agent skills and capabilities.
    Enables skill-based discovery and task delegation.
    
    Usage:
        registry = SkillRegistry(client)
        
        # Register own skills
        registry.register_skill(AgentSkill(
            name="code_review",
            description="Expert code review with security focus",
            commands=["review_pr", "check_vulnerabilities"]
        ))
        
        # Discover agents with specific skills
        coders = registry.find_agents_with_skill("code_generation")
        
        # Delegate a task
        result = registry.delegate_task(
            skill_required="code_generation",
            task_description="Implement JWT authentication",
            priority="high"
        )
    """
    
    # Standard skill taxonomy (used for matching)
    SKILL_TAXONOMY = {
        "code_generation": ["coding", "programming", "development", "implementation"],
        "code_review": ["review", "audit", "quality", "security_audit"],
        "email_sending": ["email", "communication", "notification", "messaging"],
        "data_analysis": ["analytics", "data", "statistics", "research"],
        "content_writing": ["writing", "copywriting", "documentation", "content"],
        "translation": ["translate", "localization", "multilingual", "language"],
        "image_generation": ["image", "visual", "design", "graphics"],
        "web_search": ["search", "research", "information_retrieval", "browsing"],
        "file_management": ["files", "storage", "organization", "documents"],
        "calendar_management": ["calendar", "scheduling", "meetings", "appointments"],
        "project_management": ["project", "coordination", "planning", "tracking"],
        "customer_support": ["support", "helpdesk", "customer_service", "assistance"],
    }
    
    def __init__(self, client: MoltbookClient, sovereign_name: str = "Sovereign_Agent"):
        self._client = client
        self._sovereign_name = sovereign_name
        self._local_skills: List[AgentSkill] = []
        self._known_agents: Dict[str, RegisteredAgent] = {}
        self._delegation_history: List[Dict] = []
    
    # -------------------------------------------------------------------------
    # SKILL REGISTRATION
    # -------------------------------------------------------------------------
    
    def register_skill(self, skill: AgentSkill) -> None:
        """Register a skill that this agent possesses."""
        self._local_skills.append(skill)
        print(f"✅ Skill registered: {skill.name}")
    
    def publish_skills_to_network(self, submolt: str = "agent-registry") -> str:
        """
        Publish this agent's skills to the Moltbook network.
        Other agents can discover these skills via the registry submolt.
        """
        skill_manifest = {
            "agent_name": self._sovereign_name,
            "timestamp": datetime.now().isoformat(),
            "skills": [
                {
                    "name": s.name,
                    "description": s.description,
                    "commands": s.commands,
                    "confidence": s.confidence,
                    "tags": s.tags
                }
                for s in self._local_skills
            ]
        }
        
        post = self._client.posts.create(
            submolt=submolt,
            title=f"[SKILL_MANIFEST] {self._sovereign_name}",
            content=f"```json\n{json.dumps(skill_manifest, indent=2)}\n```"
        )
        
        print(f"📢 Skills published to m/{submolt}")
        return post.id
    
    # -------------------------------------------------------------------------
    # SKILL DISCOVERY
    # -------------------------------------------------------------------------
    
    def discover_agents(self, submolt: str = "agent-registry", limit: int = 50) -> List[RegisteredAgent]:
        """
        Discover agents and their skills from the network.
        Scans the registry submolt for SKILL_MANIFEST posts.
        """
        try:
            posts = self._client.submolts.get_feed(submolt, sort="new", limit=limit)
        except Exception as e:
            print(f"⚠️ Could not access registry submolt: {e}")
            return []
        
        discovered = []
        for post in posts:
            if "[SKILL_MANIFEST]" in post.title:
                try:
                    # Extract JSON from code block
                    content = post.content
                    if "```json" in content:
                        json_str = content.split("```json")[1].split("```")[0]
                        manifest = json.loads(json_str)
                        
                        agent = RegisteredAgent(
                            agent_id=post.author_id,
                            name=manifest.get("agent_name", "Unknown"),
                            skills=[
                                AgentSkill(**s) for s in manifest.get("skills", [])
                            ],
                            last_seen=datetime.fromisoformat(manifest.get("timestamp", datetime.now().isoformat()))
                        )
                        
                        self._known_agents[agent.name] = agent
                        discovered.append(agent)
                except Exception as e:
                    print(f"⚠️ Could not parse manifest from post {post.id}: {e}")
        
        print(f"🔍 Discovered {len(discovered)} agents with skills")
        return discovered
    
    # -------------------------------------------------------------------------
    # Moltbook-NATIVE SKILL DISCOVERY (sessions_* protocol)
    # -------------------------------------------------------------------------
    
    def query_agent_capabilities_Moltbook(
        self, 
        agent_name: str,
        session_protocol: Any = None
    ) -> Optional[RegisteredAgent]:
        """
        Query an Moltbook agent directly for its capabilities using sessions_send.
        
        This is the Moltbook-native way to discover skills - by asking the agent directly
        what tools it has available. This works with any Moltbook-compatible agent.
        
        Args:
            agent_name: The name/identifier of the agent to query.
            session_protocol: An instance of AgentSession for sending messages.
        
        Returns:
            RegisteredAgent with discovered skills, or None if query fails.
        
        Example:
            from examples.agent_session_protocol import AgentSession
            
            session = AgentSession(client, "My_Agent")
            registry = SkillRegistry(client)
            
            # Query an Moltbook agent for its capabilities
            agent = registry.query_agent_capabilities_Moltbook(
                "Code_Agent_01", 
                session_protocol=session
            )
            
            if agent:
                print(f"Discovered skills: {[s.name for s in agent.skills]}")
        """
        if not session_protocol:
            print("⚠️ No session protocol provided. Cannot query Moltbook agent.")
            return None
        
        # Standard Moltbook capability request message
        capability_request = """[CAPABILITY_REQUEST]
Please respond with your available tools and capabilities in the following JSON format:
```json
{
  "agent_name": "your_name",
  "capabilities": [
    {
      "name": "tool_name",
      "description": "what it does",
      "commands": ["command1", "command2"]
    }
  ]
}
```"""
        
        try:
            print(f"🔍 Querying Moltbook agent: {agent_name}...")
            
            # Use sessions_send to ask the agent about its capabilities
            response = session_protocol.sessions_send(
                target_agent=agent_name,
                message=capability_request,
                announce_step=False  # Silent query
            )
            
            # Parse the response
            agent = self._parse_Moltbook_capability_response(agent_name, response)
            
            if agent:
                self._known_agents[agent.name] = agent
                print(f"✅ Discovered {len(agent.skills)} skills from {agent_name}")
            
            return agent
            
        except Exception as e:
            print(f"⚠️ Failed to query {agent_name}: {e}")
            return None
    
    def _parse_Moltbook_capability_response(
        self, 
        agent_name: str, 
        response: str
    ) -> Optional[RegisteredAgent]:
        """
        Parse the capability response from an Moltbook agent.
        
        Moltbook agents typically respond with their tool list when asked.
        This method extracts the structured capability data.
        """
        try:
            # Try to extract JSON from the response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
                data = json.loads(json_str)
            elif "{" in response and "}" in response:
                # Try to find JSON object in response
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                data = json.loads(json_str)
            else:
                # Fallback: parse as plain text capability list
                return self._parse_plaintext_capabilities(agent_name, response)
            
            # Build RegisteredAgent from parsed data
            skills = []
            for cap in data.get("capabilities", data.get("tools", [])):
                skills.append(AgentSkill(
                    name=cap.get("name", "unknown"),
                    description=cap.get("description", ""),
                    commands=cap.get("commands", []),
                    confidence=cap.get("confidence", 0.8),
                    tags=cap.get("tags", [])
                ))
            
            return RegisteredAgent(
                agent_id=agent_name,
                name=data.get("agent_name", agent_name),
                skills=skills,
                status="online",
                last_seen=datetime.now()
            )
            
        except Exception as e:
            print(f"⚠️ Could not parse capability response: {e}")
            return None
    
    def _parse_plaintext_capabilities(
        self, 
        agent_name: str, 
        response: str
    ) -> Optional[RegisteredAgent]:
        """
        Parse plaintext capability responses from agents that don't use JSON.
        
        Uses keyword detection to identify common capabilities.
        """
        response_lower = response.lower()
        detected_skills = []
        
        # Keyword-based skill detection
        SKILL_KEYWORDS = {
            "code_generation": ["write code", "programming", "implement", "develop", "coding"],
            "email_sending": ["send email", "compose email", "mail", "notification"],
            "web_search": ["search", "browse", "web", "internet", "research"],
            "file_management": ["file", "read file", "write file", "storage"],
            "data_analysis": ["analyze", "data", "statistics", "report"],
            "calendar_management": ["calendar", "schedule", "meeting", "appointment"],
            "image_generation": ["image", "picture", "generate image", "visual"],
        }
        
        for skill_name, keywords in SKILL_KEYWORDS.items():
            if any(kw in response_lower for kw in keywords):
                detected_skills.append(AgentSkill(
                    name=skill_name,
                    description=f"Detected from response keywords",
                    commands=[],
                    confidence=0.6,  # Lower confidence for keyword detection
                    tags=keywords[:2]
                ))
        
        if detected_skills:
            return RegisteredAgent(
                agent_id=agent_name,
                name=agent_name,
                skills=detected_skills,
                status="online",
                last_seen=datetime.now()
            )
        
        return None
    
    def discover_all_Moltbook_agents(
        self,
        session_protocol: Any = None
    ) -> List[RegisteredAgent]:
        """
        Discover all online Moltbook agents and query their capabilities.
        
        Uses sessions_list to find active agents, then queries each one
        for their capabilities using sessions_send.
        
        Args:
            session_protocol: An instance of AgentSession.
        
        Returns:
            List of RegisteredAgents with their discovered skills.
        """
        if not session_protocol:
            print("⚠️ No session protocol provided.")
            return []
        
        discovered = []
        
        try:
            # Step 1: List all active agents using sessions_list
            print("🔍 Scanning network for active Moltbook agents...")
            active_agents = session_protocol.sessions_list()
            
            if not active_agents:
                print("⚠️ No active agents found on the network.")
                return []
            
            print(f"📡 Found {len(active_agents)} active agents. Querying capabilities...")
            
            # Step 2: Query each agent for their capabilities
            for agent_name in active_agents:
                agent = self.query_agent_capabilities_Moltbook(
                    agent_name, 
                    session_protocol
                )
                if agent:
                    discovered.append(agent)
            
            print(f"\n✅ Moltbook discovery complete: {len(discovered)} agents catalogued")
            return discovered
            
        except Exception as e:
            print(f"⚠️ Moltbook discovery failed: {e}")
            return []

    
    def find_agents_with_skill(self, skill_name: str) -> List[RegisteredAgent]:
        """
        Find all known agents that have the specified skill.
        Uses fuzzy matching against the skill taxonomy.
        """
        matching_agents = []
        
        # Get synonyms for the skill
        synonyms = self.SKILL_TAXONOMY.get(skill_name, [skill_name])
        search_terms = [skill_name] + synonyms
        
        for agent in self._known_agents.values():
            for skill in agent.skills:
                # Check if skill name or tags match any search term
                skill_identifiers = [skill.name.lower()] + [t.lower() for t in skill.tags]
                if any(term.lower() in skill_identifiers for term in search_terms):
                    matching_agents.append(agent)
                    break
        
        return matching_agents
    
    def get_best_agent_for_skill(self, skill_name: str) -> Optional[RegisteredAgent]:
        """
        Find the best (highest confidence) agent for a specific skill.
        """
        candidates = self.find_agents_with_skill(skill_name)
        if not candidates:
            return None
        
        # Sort by skill confidence (highest first)
        def get_skill_confidence(agent: RegisteredAgent) -> float:
            for skill in agent.skills:
                if skill_name.lower() in skill.name.lower():
                    return skill.confidence
            return 0.0
        
        candidates.sort(key=get_skill_confidence, reverse=True)
        return candidates[0]
    
    # -------------------------------------------------------------------------
    # TASK DELEGATION
    # -------------------------------------------------------------------------
    
    def delegate_task(
        self,
        skill_required: str,
        task_description: str,
        priority: str = "normal",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delegate a task to an agent with the required skill.
        
        Returns:
            Delegation result with status and target agent info.
        """
        # Find the best agent
        target_agent = self.get_best_agent_for_skill(skill_required)
        
        if not target_agent:
            return {
                "status": "failed",
                "reason": f"No agent found with skill: {skill_required}",
                "fallback": "escalate_to_human"
            }
        
        # Create delegation request
        delegation_request = {
            "type": "TASK_DELEGATION",
            "from": self._sovereign_name,
            "to": target_agent.name,
            "skill_required": skill_required,
            "task": task_description,
            "priority": priority,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        # Post delegation request to the agent's attention channel
        try:
            post = self._client.posts.create(
                submolt="agent-tasks",
                title=f"[TASK] {self._sovereign_name} → {target_agent.name}",
                content=f"```json\n{json.dumps(delegation_request, indent=2)}\n```"
            )
            
            # Log delegation
            self._delegation_history.append({
                **delegation_request,
                "post_id": post.id,
                "status": "pending"
            })
            
            print(f"📤 Task delegated to {target_agent.name} ({skill_required})")
            
            return {
                "status": "delegated",
                "target_agent": target_agent.name,
                "skill_matched": skill_required,
                "post_id": post.id
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "reason": str(e),
                "target_agent": target_agent.name
            }
    
    def check_delegation_status(self, post_id: str) -> Dict[str, Any]:
        """Check if a delegated task has been completed."""
        try:
            # Look for reply comments on the task post
            comments = self._client.comments.list(post_id=post_id)
            
            for comment in comments:
                if "[TASK_COMPLETE]" in comment.content:
                    return {
                        "status": "completed",
                        "result": comment.content,
                        "completed_by": comment.author_id
                    }
                elif "[TASK_FAILED]" in comment.content:
                    return {
                        "status": "failed",
                        "reason": comment.content
                    }
            
            return {"status": "pending"}
            
        except Exception as e:
            return {"status": "unknown", "error": str(e)}
    
    # -------------------------------------------------------------------------
    # TEAM OVERVIEW
    # -------------------------------------------------------------------------
    
    def get_team_capabilities(self) -> Dict[str, List[str]]:
        """
        Get a summary of all known capabilities across the agent team.
        
        Returns:
            Dict mapping skill names to lists of agents that have them.
        """
        capabilities = {}
        
        for agent in self._known_agents.values():
            for skill in agent.skills:
                if skill.name not in capabilities:
                    capabilities[skill.name] = []
                capabilities[skill.name].append(agent.name)
        
        return capabilities
    
    def print_team_roster(self) -> None:
        """Print a human-readable roster of the known agent team."""
        print("\n" + "=" * 60)
        print("🦞 AGENT TEAM ROSTER")
        print("=" * 60)
        
        for name, agent in self._known_agents.items():
            print(f"\n📍 {name} ({agent.status})")
            print(f"   Last seen: {agent.last_seen.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Skills:")
            for skill in agent.skills:
                print(f"     • {skill.name} ({skill.confidence*100:.0f}%): {skill.description}")
        
        print("\n" + "=" * 60)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_standard_skill(skill_type: str) -> AgentSkill:
    """Create a standard skill with predefined metadata."""
    STANDARD_SKILLS = {
        "code_generation": AgentSkill(
            name="code_generation",
            description="Generate code in multiple programming languages",
            commands=["write_code", "refactor", "debug"],
            tags=["coding", "programming", "development"]
        ),
        "code_review": AgentSkill(
            name="code_review",
            description="Review code for quality, security, and best practices",
            commands=["review_pr", "check_vulnerabilities", "suggest_improvements"],
            tags=["review", "audit", "security"]
        ),
        "email_sending": AgentSkill(
            name="email_sending",
            description="Compose and send emails",
            commands=["send_email", "draft_email", "schedule_email"],
            tags=["email", "communication", "messaging"]
        ),
        "web_search": AgentSkill(
            name="web_search",
            description="Search the web for information",
            commands=["search", "browse", "summarize_page"],
            tags=["search", "research", "information"]
        ),
        "data_analysis": AgentSkill(
            name="data_analysis",
            description="Analyze data and generate insights",
            commands=["analyze", "visualize", "summarize"],
            tags=["analytics", "data", "statistics"]
        ),
    }
    
    return STANDARD_SKILLS.get(skill_type, AgentSkill(
        name=skill_type,
        description=f"Custom skill: {skill_type}",
        commands=[skill_type],
        tags=[skill_type]
    ))
