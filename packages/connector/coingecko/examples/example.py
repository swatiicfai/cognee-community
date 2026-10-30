"""Example: Ingesting CoinGecko Crypto Market Data into Cognee AI Memory."""

import asyncio
import os
from cognee_community_connector_coingecko import (
    coingecko_source,
    fetch_coins_markets_documents,
)

# Set up your LLM key if not already set in environment
os.environ.setdefault("LLM_API_KEY", "your-llm-api-key")


async def run_document_ingestion_example():
    """Method A: Ingest formatted crypto market snapshots via cognee.add()."""
    import cognee

    print("[1/3] Fetching top 5 cryptocurrency snapshots from CoinGecko...")
    documents = fetch_coins_markets_documents(vs_currency="usd", limit=5)
    print(f"Fetched {len(documents)} coin documents.")

    print("\nSample Formatted Document:")
    print("------------------------------------------")
    print(documents[0])
    print("------------------------------------------")

    print("[2/3] Adding documents into Cognee dataset...")
    await cognee.add(documents, dataset_name="crypto_market_knowledge")

    print("[3/3] Cognifying data into knowledge graph memory...")
    await cognee.cognify(datasets=["crypto_market_knowledge"])

    print("\nQuerying Cognee AI memory:")
    queries = [
        "What is the current price and market capitalization of Bitcoin?",
        "Which coin had the highest 24h price percentage change?",
    ]
    for q in queries:
        print(f"\nQuestion: {q}")
        search_results = await cognee.search(q, datasets=["crypto_market_knowledge"])
        print(f"Answer / Results: {search_results}")


async def run_dlt_source_example():
    """Method B: Ingest structured data via dlt source with cognee.remember()."""
    import cognee

    print("\nRunning Cognee remember pipeline with CoinGecko DLT source...")
    source = coingecko_source(vs_currency="usd", limit=10)
    await cognee.remember(source, dataset_name="crypto_dlt_dataset")
    print("DLT ingestion completed.")


async def main():
    print("=== Cognee CoinGecko Connector Demo ===")
    await run_document_ingestion_example()


if __name__ == "__main__":
    asyncio.run(main())
