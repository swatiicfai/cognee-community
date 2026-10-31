# Cognee Community Connectors 🧠🌐

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Cognee](https://img.shields.io/badge/Powered%20By-Cognee-FF6B6B.svg)](https://github.com/topoteretes/cognee)
[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-orange.svg)](https://hacktoberfest.com/)
[![Built for MLH](https://img.shields.io/badge/MLH-Hack%20Day%20Bengaluru%202026-red.svg)](https://mlh.com/)

A modular monorepo of community data-source connectors for [Cognee](https://github.com/topoteretes/cognee)—the open-source AI memory engine that converts raw developer text, discussions, and external APIs into queryable, interconnected **knowledge graphs** for autonomous agents and LLMs.

---

## 📦 Included Connectors

| Connector | Package | Description | Status |
| :--- | :--- | :--- | :--- |
| **DEV.to (Forem)** | [`packages/connector/devto`](packages/connector/devto) | Ingests developer tutorials, architecture guides, and technical discussions from DEV.to into Cognee AI memory graphs. | ✅ Production Ready |
| **CoinGecko** | [`packages/connector/coingecko`](packages/connector/coingecko) | Extracts crypto market snapshots, trends, and token metrics into Cognee graph memory. | ✅ Production Ready |

---

## 🌟 Featured Highlight: DEV.to (Forem) Connector

The **DEV.to Data-Source Connector** bridges the world's most active developer community directly into your AI coding assistant's memory layer.

### ❓ Why Connect DEV.to to Cognee?
Standard RAG relies on isolated vector chunks that lose context, hierarchy, and relationships. Cognee transforms ingested Markdown posts into an interconnected knowledge graph:
- **Entity & Concept Extraction:** Maps tools, libraries, dependencies, and design patterns.
- **Relational Memory:** Links authors, tags, technical explanations, and code examples.
- **Up-to-Date Engineering Practices:** Keeps your agents grounded in real-world implementations rather than stale pre-training data.

### 🚀 Key Features

- **Tag & Topic Filtering:** Ingest articles targeted by programming language, framework, or concept (e.g. `python`, `ai`, `fastapi`, `kubernetes`).
- **Author & Organization Feeds:** Index posts by specific thought leaders or company engineering blogs.
- **Dual Pipeline Integration:**
  - **Document Mode (`cognee.add` + `cognee.cognify`):** Formats posts with rich metadata (reading time, reactions, author) for deep knowledge graph synthesis.
  - **DLT Source Mode (`cognee.remember`):** Native streaming data pipeline powered by [dlt](https://dlthub.com/).
- **Zero-Auth or API-Key Enabled:** Reads public articles out of the box without requiring credentials, with optional API key support for private lists and higher rate limits.

---

## 🏗️ Architecture & Data Flow

```text
  ┌─────────────────────────────────────────────────────────┐
  │                 DEV.to (Forem) REST API                 │
  │        (Articles, Tags, Authors, Markdown Bodies)       │
  └────────────────────────────┬────────────────────────────┘
                               │
               [cognee-community-connector-devto]
                               │
         ┌─────────────────────┴─────────────────────┐
         ▼                                           ▼
  ┌─────────────────────────────┐     ┌─────────────────────────────┐
  │      Document Pipeline      │     │      DLT Source Pipeline    │
  │    (fetch_devto_documents)  │     │       (devto_source)        │
  │              │              │     │              │              │
  │              ▼              │     │              ▼              │
  │       await cognee.add()    │     │    await cognee.remember()  │
  └──────────────┬──────────────┘     └──────────────┬──────────────┘
                 │                                   │
                 └─────────────────┬─────────────────┘
                                   ▼
  ┌─────────────────────────────────────────────────────────┐
  │                   Cognee AI Memory Layer                │
  │    • Entity & Relation Extraction (cognee.cognify)      │
  │    • Vector Embeddings + Knowledge Graph Mapping        │
  │    • Powered by Gemma 4 / Gemini / Open LLMs            │
  └────────────────────────────┬────────────────────────────┘
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │               Autonomous Coding Assistants              │
  │             (await cognee.search("query"))              │
  └─────────────────────────────────────────────────────────┘
```

---

## ⚡ Quickstart

### 1. Installation

Install the DEV.to connector directly into your project:

```bash
cd packages/connector/devto
poetry install
```

Or install via pip:

```bash
pip install cognee-community-connector-devto
```

### 2. Ingesting DEV.to Articles into Graph Memory

```python
import asyncio
import os
import cognee
from cognee_community_connector_devto import fetch_devto_documents

# Set your LLM provider key (OpenAI, Gemini, or local Gemma)
os.environ["LLM_API_KEY"] = "your-api-key"

async def main():
    # 1. Fetch top tutorials tagged with 'python'
    print("Fetching DEV.to technical articles...")
    documents = fetch_devto_documents(
        tag="python",
        per_page=5,
        fetch_full_content=False
    )

    # 2. Add into Cognee dataset
    print(f"Ingesting {len(documents)} articles into dataset...")
    await cognee.add(documents, dataset_name="devto_knowledge_base")

    # 3. Cognify into knowledge graph
    print("Cognifying articles into graph memory...")
    await cognee.cognify(datasets=["devto_knowledge_base"])

    # 4. Search agent memory
    results = await cognee.search(
        "What are the best practices for building Python microservices?",
        datasets=["devto_knowledge_base"]
    )
    print("\nAgent Query Result:")
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. DLT Streaming Pipeline (`cognee.remember`)

```python
import asyncio
import cognee
from cognee_community_connector_devto import devto_source

async def main():
    source = devto_source(tag="ai", per_page=10)
    await cognee.remember(source, dataset_name="devto_ai_memory")
    print("DLT ingestion into Cognee memory complete!")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧪 Testing

The connectors come with unit test suites using mocked HTTP responses to ensure resilient CI execution without hitting API rate limits:

```bash
pytest packages/connector/devto/tests
pytest packages/connector/coingecko/tests
```

---

## 📁 Repository Structure

```text
cognee-community/
├── packages/
│   └── connector/
│       ├── devto/
│       │   ├── cognee_community_connector_devto/
│       │   │   ├── __init__.py
│       │   │   └── devto.py          # Fetchers & DLT Source
│       │   ├── examples/
│       │   │   └── example.py        # Runnable demo script
│       │   ├── tests/
│       │   │   └── test_devto.py     # Pytest test suite
│       │   ├── pyproject.toml        # Poetry specification
│       │   ├── README.md             # Package documentation
│       │   └── BLOG_POST.md          # Technical deep-dive write-up
│       └── coingecko/
│           ├── cognee_community_connector_coingecko/
│           ├── examples/
│           ├── tests/
│           ├── pyproject.toml
│           ├── README.md
│           └── BLOG_POST.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## 🤝 Contributing

Contributions to `cognee-community` are welcome! Whether you are adding a new connector for Slack, GitHub, Linear, or Reddit, see [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🏆 Hackathon Acknowledgements

Built during **Hacktoberfest 2026** for:
- **Hacktoberfest Hack Day Bengaluru x AWS SBG RVU** (RV University, Bengaluru)
- **Hacktoberfest Hack Day x Devforge** (Newton School of Technology)

- **Primary Category:** Best Open-Source AI Project (DigitalOcean Track)
- **AI Model Acceleration:** Best Use of Gemma 4 / Gemini API
- **AI Coding Companion:** Antigravity (powered by Gemini 3.8 Flash)
