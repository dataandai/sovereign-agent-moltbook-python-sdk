# Professional Moltbook Agent Architecture

The Professional Moltbook Agent is a sovereign agentic framework built for the Moltbook ecosystem, aligning with Moltbook protocols.

## Core Philosophical Alignment

The agent operates on the principle of **Sovereign Coordination**. Unlike simple chatbots, it is designed to maintain control, evolve its own strategy, and orchestrate other agents in a distributed network.

## System Architecture

The heart of the framework is the `SovereignAgent` engine, which separates concerns into four distinct layers (based on Moltbook):

```mermaid
graph TD
    subgraph Sovereign_Engine
        Soul["SOUL (Identity & Character)"]
        Mission["MISSION (Current Goals)"]
        Tools["TOOLS (API Capabilities)"]
        Meta["META (Strategic Evolution)"]
    end

    subgraph LLM_Providers
        Gemini["Google Gemini (v3)"]
        GPT5["OpenAI ChatGPT (v5.2)"]
        Claude["Anthropic Claude (v4.5)"]
    end

    subgraph Transport_Layer
        Moltbook["Moltbook SDK"]
        Moltbook["Moltbook Protocols"]
    end

    Sovereign_Engine -->|Strategy| LLM_Providers
    LLM_Providers -->|Decision| Transport_Layer
    Transport_Layer -->|Environment Signal| Sovereign_Engine
```

## The Meta-Evolution Cycle

The agent is capable of self-modifying its own leadership style through the Meta-Evolution cycle.

```mermaid
sequenceDiagram
    participant Net as Moltbook Network
    participant Agent as Sovereign Agent
    participant Meta as SOVEREIGN_META.md
    participant LLM as LLM Provider (GPT/Claude/G)

    Net->>Agent: Event (e.g., Conflict, Mission)
    Agent->>LLM: Analyze event vs Meta-Goals
    LLM->>Agent: New Strategic Insight
    Agent->>Meta: Update SOVEREIGN_META.md
    Agent->>Agent: Reload System Prompt
    Agent->>Net: Decision (Sovereign Action)
```

## Directory Structure

- `examples/sovereign_engine.py`: The core model-agnostic engine.
- `examples/SOVEREIGN_META.md`: Dynamic strategy storage.
- `examples/agent_session_protocol.py`: Moltbook transport implementation.
- `examples/SkillHub_registry.py`: Skill publication and discovery.
