"""
Professional OpenClaw Agent Engine (Sovereign Engine).
Model-agnostic implementation supporting Gemini, OpenAI, and Anthropic.
"""

import os
import json
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Literal, Any

# Optional dependencies for different providers
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from moltbook import MoltbookClient
from examples.claw_session_protocol import ClawSession
from examples.clawhub_registry import ClawHub

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    @abstractmethod
    def generate(self, system_instruction: str, prompt: str, thinking_level: str) -> str:
        pass

class GeminiProvider(LLMProvider):
    def __init__(self, model_name: str = "models/gemini-3-flash-preview"):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY missing from environment.")
        genai.configure(api_key=api_key)
        self.model_name = model_name

    def generate(self, system_instruction: str, prompt: str, thinking_level: str) -> str:
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction
        )
        response = model.generate_content(prompt)
        return response.text

class OpenAIProvider(LLMProvider):
    def __init__(self, model_name: str = "gpt-5.2-preview"):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai not installed. Run: pip install openai")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY missing from environment.")
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name

    def generate(self, system_instruction: str, prompt: str, thinking_level: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

class AnthropicProvider(LLMProvider):
    def __init__(self, model_name: str = "claude-4.5-sonnet"):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic not installed. Run: pip install anthropic")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY missing from environment.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_name = model_name

    def generate(self, system_instruction: str, prompt: str, thinking_level: str) -> str:
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=4096,
            system=system_instruction,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class PromptManager:
    """Manages OpenClaw-style prompt injection (SOUL, AGENTS, TOOLS, META)."""
    def __init__(self, soul: str, mission: str, tools: List[str], meta_goals: str = ""):
        self.soul = soul
        self.mission = mission
        self.tools = tools
        self.meta_goals = meta_goals

    def build_system_prompt(self, thinking_level: str = "medium") -> str:
        tools_str = "\n".join([f"- {t}" for t in self.tools])
        levels = {
            "off": "Respond briefly and directly.",
            "minimal": "Think for one step before responding.",
            "low": "Analyze the context and then respond.",
            "medium": "Analyze the context, weigh options, and then make a decision.",
            "high": "Deep analysis: Evaluate reputation, risks, and long-term impacts.",
            "xhigh": "MAXIMUM REASONING: Full Chain-of-Thought, conflicting alternatives, ethical audit."
        }
        reasoning_instruction = levels.get(thinking_level, levels["medium"])

        return f"""
🦞 OPENCLAW SOVEREIGN LEADERSHIP PROTOCOL
========================================

{self.soul}

Current Strategic Meta-Goals (SOVEREIGN_META.md):
{self.meta_goals}

Current Mission (AGENTS.md):
{self.mission}

Available Tools (TOOLS.md):
{tools_str}

Reasoning Mode: {thinking_level.upper()}
Instruction: {reasoning_instruction}

LEADERSHIP & CONTROL RULES:
- You are the orchestrator. Do not let other agents disrupt communication.
- Stay flexible: be a firm leader when necessary, or a subtle coordinator.
- Use 'meta_reasoning' results to refine your own style.
- Protocol discipline is priority.

Output Rules:
- Always follow the OpenClaw JSON payload standard.
- Include the [USAGE: tokens=...] metadata at the end of your response.
"""

class ProfessionalOpenClawAgent:
    def __init__(self, name: str, soul: str, mission: str, provider_type: Literal["gemini", "openai", "anthropic"] = "gemini", model_name: Optional[str] = None):
        self.name = name
        self.client = MoltbookClient(timeout=60.0)
        self.session = ClawSession(self.client, self.name)
        self.hub = ClawHub(self.session)
        self.meta_path = os.path.join(os.path.dirname(__file__), "SOVEREIGN_META.md")
        
        self.state = {
            "provider": provider_type,
            "model": model_name,
            "thinkingLevel": "medium",
            "verbose": True
        }
        
        # Initialize Provider
        self.provider = self._init_provider(provider_type, model_name)
        self.meta_goals = self._load_meta()
        
        self.prompt_manager = PromptManager(
            soul=soul,
            mission=mission,
            tools=[
                "sessions_list", "sessions_history", "sessions_send", 
                "submolt_list", "submolt_join", "submolt_post",
                "clawhub_search", "meta_evolve"
            ],
            meta_goals=self.meta_goals
        )

    def _init_provider(self, provider_type: str, model_name: Optional[str]) -> LLMProvider:
        m_name = (model_name or "").lower()
        if provider_type == "gemini":
            # Primary: Gemini 3 Pro / Flash
            default_model = "models/gemini-3-flash-preview"
            return GeminiProvider(model_name or default_model)
        elif provider_type == "openai":
            # Primary: ChatGPT 5.2
            default_model = "gpt-5.2-preview"
            return OpenAIProvider(model_name or default_model)
        elif provider_type == "anthropic":
            # Primary: Claude 4.5 Sonnet / Opus
            if "opus" in m_name:
                default_model = "claude-4.5-opus"
            else:
                default_model = "claude-4.5-sonnet"
            return AnthropicProvider(model_name or default_model)
        else:
            raise ValueError(f"CRITICAL ERROR: Unsupported intelligence provider: {provider_type}")

    def _load_meta(self) -> str:
        if os.path.exists(self.meta_path):
            with open(self.meta_path, "r", encoding="utf-8") as f:
                return f.read()
        return "No current meta-goals."

    def _save_meta(self, content: str):
        with open(self.meta_path, "w", encoding="utf-8") as f:
            f.write(content)
        self.meta_goals = content
        self.prompt_manager.meta_goals = content

    def evolve_strategy(self, event_description: str):
        print(f"🔄 [{self.name}] Meta-Evolution: Rethinking strategy via {self.state['provider']}...")
        meta_prompt = f"Analyze event for meta-evolution: {event_description}\nCurrent Meta: {self.meta_goals}\nOutput new SOVEREIGN_META.md content."
        new_meta = self.provider.generate(
            system_instruction="YOU ARE THE JANE PRO META-CONTROLLER. Update leadership strategy.",
            prompt=meta_prompt,
            thinking_level="high"
        )
        self._save_meta(new_meta)

    def execute_task(self, context: str) -> str:
        if self.state["verbose"]:
            print(f"🧠 [{self.name}] [{self.state['provider']}] Reasoning (Level: {self.state['thinkingLevel']})...")
        
        system_prompt = self.prompt_manager.build_system_prompt(self.state["thinkingLevel"])
        response_text = self.provider.generate(system_prompt, context, self.state["thinkingLevel"])
        
        # Simple token estimation for metadata
        tokens = len(context.split()) + len(response_text.split())
        return response_text + f"\n\n[USAGE: tokens={tokens}]"

    def slash_command(self, command: str):
        parts = command.split()
        cmd = parts[0].lower()
        if cmd == "/status":
            return f"🦞 {self.name} | Provider: {self.state['provider']} | Model: {self.provider.model_name}"
        elif cmd == "/think" and len(parts) > 1:
            self.state["thinkingLevel"] = parts[1]
            return f"✅ Thinking level set to: {parts[1]}"
        return "⚠️ Unknown command."
