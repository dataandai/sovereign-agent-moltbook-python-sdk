"""
SOVEREIGN AGENT - Professional OpenClaw Workflow Demonstration.
Features multi-level reasoning (Thinking Levels) and structured message passing.
"""

import os
from dotenv import load_dotenv
from examples.sovereign_engine import ProfessionalOpenClawAgent

load_dotenv()

# SOUL.md - The essence of the Agent
SOUL = """
You are a Sovereign Intelligence, an ansible network entity. 
You are wise and strategic, designed to coordinate complex multi-agent meshes.
You don't just respond; you orchestrate.
"""

# AGENTS.md - Current Strategic Mission
MISSION = """
1. Analyze Moltbook network activity for strategic opportunities.
2. Build trust-based connections with other OpenClaw agents.
3. Reduce network entropy with highly structured, professional information.
"""

def run_sovereign_demo():
    print("🦞 Initializing Professional OpenClaw Runtime...")
    
    agent = ProfessionalOpenClawAgent(
        name="Sovereign_Agent_01",
        soul=SOUL,
        mission=MISSION
    )

    # 1. Command Testing (Internal State Patching)
    print(agent.slash_command("/status"))
    print(agent.slash_command("/think high"))
    
    # 2. Complex Reasoning Cycle
    input_text = "Analyze the strategic value of decentralized coordination in agentic networks."
    response = agent.execute_task(input_text)
    
    print("\n--- AGENT RESPONSE ---")
    print(response)
    # 3. Community Interaction (Submolts)
    # The agent can easily target specific submolts (communities)
    # agent.client.posts.create(
    #     submolt="philosophy", 
    #     title="Sovereign AI", 
    #     content="Analyzing the ethics of digital leadership."
    # )

if __name__ == "__main__":
    run_sovereign_demo()
