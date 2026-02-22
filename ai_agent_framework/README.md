# Minimal AI Agent Framework

A lightweight, asynchronous AI agent framework for information gathering tasks.

## Features

- Modular architecture with pluggable modules
- Async support using asyncio and httpx
- Configuration management
- Persistent storage with SQLite
- CLI interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from ai_agent_framework.core import InformationGatheringAgent
from ai_agent_framework.modules import WhoisModule, DNSModule

async def main():
    agent = InformationGatheringAgent()
    agent.register_module("whois", WhoisModule())
    agent.register_module("dns", DNSModule())
    
    task = {"target": "example.com"}
    results = await agent.execute(task)
    print(results)

asyncio.run(main())
```

Or via CLI:
```bash
python -m ai_agent_framework.cli --target example.com
```

## Core Components

1. **Agent**: Main orchestrator for executing tasks
2. **Modules**: Pluggable components for specific tasks
3. **HTTP Client**: Async HTTP client using httpx
4. **Storage**: SQLite-based result storage
5. **Config**: YAML configuration management
