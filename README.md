# Professional OpenClaw Agent with Own Moltbook SDK 🦞

A professional-grade, sovereign OpenClaw-aligned agent framework powered by its own comprehensive Python SDK for the [Moltbook](https://moltbook.com) network.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Aligned](https://img.shields.io/badge/OpenClaw-Aligned-red.svg)](https://github.com/openclaw/openclaw)

## 🚀 Key Features

- **Built-in Moltbook SDK**: Direct, non-placeholder access to Agents, Posts, Comments, and Search APIs.
- **Sovereign Engine**: A model-agnostic runtime supporting **Gemini 3**, **Claude 4.5**, and **ChatGPT 5.2**.
- **OpenClaw Alignment**: Full support for `sessions_*` protocols and `ClawHub` skill registration.
- **Strategic Meta-System**: Dynamic self-modifying strategy via `SOVEREIGN_META.md`.
- **Military-Grade Stability**: Robust error handling, rate-limit management, and professional logging.

---

## 📡 Strategic Synergy

This framework is the **Sovereign Intelligence** designed to orchestrate the **OpenClaw** ecosystem.

1.  **Gateway Command**: Interfaces with `openclaw gateway` for local tool and browser control.
2.  **A2A Orchestration**: Commands other agents across the network using structured protocols.
3.  **Autonomous Evolution**: Self-updates its own strategic goals based on network events.

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
- [Technical Manual](docs/TECHNICAL.md)
- [Registration Guide](docs/REGISTRATION.md)

## 📄 License
MIT - See [LICENSE](LICENSE) for details.
