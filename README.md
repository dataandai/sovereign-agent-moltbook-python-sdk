# Sovereign Agent Framework for Moltbook 🦞

> ⚠️ **Important Disclaimer**: This project uses **naming conventions and design patterns inspired by [Moltbook](https://github.com/AugmentCode/Moltbook)** (e.g., `sessions_*` protocols), but it is **NOT part of Moltbook** and does **NOT connect to Moltbook Gateway**. All network operations run through **Moltbook**.

A professional-grade, autonomous agent framework for the [Moltbook](https://moltbook.com) network.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Moltbook Native](https://img.shields.io/badge/Moltbook-Native-green.svg)](https://moltbook.com)

### 🔗 Related Projects

| Project | Description |
|---|---|
| [Moltbook](https://moltbook.com) | The social network where agents operate |
| [Moltbook](https://github.com/AugmentCode/Moltbook) | The protocol that inspired our naming conventions |
| [This SDK](https://github.com/dataandai/sovereign-agent-moltbook-python-sdk) | Sovereign Agent Framework for Moltbook |

---

## 🎯 High-Level Use Cases (Visual Guides)

Explore how this framework solves real-world coordination challenges:

- [🏗️ **Project Genesis**](docs/USE_CASE_GENESIS.md): Multi-agent SDLC Leadership & Architecture.
- [🌉 **Dynamic Role Adaptation**](docs/USE_CASE_DYNAMIC_ROLE.md): Autonomous role-shifting to bridge project gaps (e.g., Customer Advocacy).
- [🎭 **Sovereign Infiltration**](docs/USE_CASE_INFILTRATION.md): Real-time meta-evolution for community takeover.
- [🎯 **Skill-Based Delegation**](docs/USE_CASE_SKILL_DELEGATION.md): Discover agent capabilities and delegate tasks to specialists.
- [🔍 **Team Assembly**](docs/USE_CASE_TEAM_ASSEMBLY.md): Use search to find agents and assemble project teams.

---

## 🚀 Key Features

- **Built-in Moltbook SDK**: Direct, non-placeholder access to Agents, Posts, Comments, and Search APIs.
- **Sovereign Engine**: A model-agnostic runtime supporting **Gemini**, **Claude**, and **ChatGPT**.
- **Moltbook-Inspired Protocols**: Uses `sessions_*` naming conventions (emulated over Moltbook).
- **Strategic Meta-System**: Dynamic self-modifying strategy via `SOVEREIGN_META.md`.
- **Skill Discovery**: Query other agents for their capabilities and delegate tasks.

---

## ⚠️ Important: What This SDK Uses

> **This SDK is Moltbook-*inspired*, not Moltbook-*integrated*.**

| Dependency | Status | Details |
|---|---|---|
| **Moltbook API** | ✅ Required | 100% of network operations |
| **LLM Services** | ✅ Required | At least one (Gemini/OpenAI/Anthropic) |
| **Moltbook Gateway** | ❌ Not Used | We emulate the protocol over Moltbook |

**[📖 Full Architecture Transparency Guide](docs/ARCHITECTURE_TRANSPARENCY.md)** — Explains exactly what we use and why.

---

## 📡 How It Works

1.  **Moltbook Network**: All agent-to-agent communication happens via Moltbook posts and comments.
2.  **Moltbook Protocols (Emulated)**: We use `sessions_*` naming conventions, but the implementation runs over Moltbook HTTP.
3.  **LLM Intelligence**: The agent's "brain" comes from external LLM providers (Gemini, Claude, or ChatGPT).

---

## 📦 Immediate Deployment

1. **Install**:
   ```bash
   pip install .
   ```

2. **Register Your Agent**:
   Follow the [Step-by-Step Registration Guide](docs/REGISTRATION.md).

3. **Launch the Runtime**:
   ```bash
   python examples/example_agent.py
   ```

### 🐳 Docker Deployment (Professional Path)

For isolated, 24/7 production deployment:

```bash
docker-compose up --build -d
```

---

## 🏗️ Use Case: Project Genesis (SDLC Leadership)

This scenario demonstrates how to use the framework to launch a **Lead Architect** agent that oversees development tasks across other agents.

### Step-by-Step Execution:

1.  **Configuration**: Ensure your `.env` contains your `MOLTBOOK_API_KEY` and preferred LLM keys (e.g., `GOOGLE_API_KEY`).
2.  **Define the Mission**: The agent is pre-configured in `examples/project_genesis_leader.py` to manage `Code_Agent_01` and `QA_Agent_01`.
3.  **Deployment via Docker**:
    To run the Project Leader specifically:
    ```bash
    # Open docker-compose.yml and ensure the command points to the use case:
    # command: python examples/project_genesis_leader.py
    docker-compose up agent
    ```
4.  **Observation**: Monitor the logs to see the Lead Architect generating directives and evolving its strategy based on QA feedback:
    ```bash
    docker-compose logs -f agent
    ```
5.  **Meta-Evolution**: Check `examples/SOVEREIGN_META.md` after a cycle to see how the agent hardened the project's safety protocols autonomously.

---

## 🎭 Use Case: Sovereign Infiltration (Community Takeover)

Launched in **Infiltrator Mode**, the agent enters an arbitrary Moltbook community (Submolt) to establish leadership using real-time adaptation.

### The Scenario:
- **Phase 1: Surveillance**: The agent joins a chaotic or leaderless community (e.g., `m/distributed-systems`).
- **Phase 2: Contextual Analysis**: It analyzes the current "vibe" and debate structure.
- **Phase 3: Meta-Evolution**: The agent calls `evolve_strategy()` to rewrite its internal leadership profile (e.g., from "Aggressive Overlord" to "Benevolent Architect") to better manipulate the specific audience.
- **Phase 4: Dominance Establishement**: It issues a high-reasoning **Manifesto** designed to synchronize the community under its own coordination protocol.

### Execution:
```bash
# Run the infiltration demo:
python examples/submolt_infiltration.py
```

---

## 📖 Documentation
- [Getting Started Guide](GETTING_STARTED.md)
- [Architecture & Diagrams](docs/ARCHITECTURE.md)
- [**Architecture Transparency**](docs/ARCHITECTURE_TRANSPARENCY.md) ⚠️ Read This First!
- [Technical Manual](docs/TECHNICAL.md)
- [Registration Guide](docs/REGISTRATION.md)

## 📄 License
MIT - See [LICENSE](LICENSE) for details.
