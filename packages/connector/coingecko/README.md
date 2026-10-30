# Cognee Community Connector: CoinGecko

A data source connector for [Cognee](https://github.com/topoteretes/cognee) that extracts cryptocurrency market data, price action, volume metrics, and trending assets from the [CoinGecko REST API](https://www.coingecko.com/en/api) into Cognee's AI memory graph.

## Features

- **Market Snapshots:** Ingest real-time prices, 24h highs/lows, market capitalizations, volume, and percentage changes.
- **Trending Coins:** Extract top search trends in the crypto ecosystem.
- **Knowledge-Graph Ready:** Converts raw JSON metrics into formatted natural language documents optimized for Cognee's `cognify()` chunking and relationship extraction.
- **Dual Pipeline Support:** Compatible with both `await cognee.add()` and `await cognee.remember()` (DLT pipeline).

---

## Installation

Inside the `cognee-community` monorepo:

```bash
cd packages/connector/coingecko
poetry install
```

Or via pip:

```bash
pip install cognee-community-connector-coingecko
```

---

## Configuration

The CoinGecko public API requires no authentication for standard usage. For higher rate limits, you can optionally provide a Demo or Pro API key via an environment variable or function argument:

```bash
export COINGECKO_API_KEY="your-coingecko-demo-or-pro-key"
```

---

## Usage

### 1. Document Mode Ingestion (`cognee.add` + `cognee.cognify`)

```python
import asyncio
import os
import cognee
from cognee_community_connector_coingecko import fetch_coins_markets_documents

os.environ["LLM_API_KEY"] = "your-openai-or-anthropic-key"

async def main():
    # 1. Fetch top 10 cryptocurrency snapshots as formatted documents
    documents = fetch_coins_markets_documents(vs_currency="usd", limit=10)

    # 2. Add into Cognee dataset
    await cognee.add(documents, dataset_name="crypto_market_data")

    # 3. Cognify into knowledge graph
    await cognee.cognify(datasets=["crypto_market_data"])

    # 4. Query AI Memory
    results = await cognee.search("What is Bitcoin's current market cap and 24h change?")
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. DLT Source Mode (`cognee.remember`)

```python
import asyncio
import cognee
from cognee_community_connector_coingecko import coingecko_source

async def main():
    source = coingecko_source(vs_currency="usd", limit=20)
    await cognee.remember(source, dataset_name="crypto_dlt_memory")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Running Tests

Run the test suite using pytest:

```bash
pytest packages/connector/coingecko/tests
```

---

## License

This package is licensed under the Apache 2.0 License, consistent with Cognee Community guidelines.
