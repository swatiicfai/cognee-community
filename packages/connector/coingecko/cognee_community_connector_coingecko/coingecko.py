"""CoinGecko data source connector for Cognee.

This module provides data extraction from CoinGecko's REST API into Cognee's
memory layer, enabling AI agents to ingest, cognify, and query cryptocurrency
market data, prices, trends, and market metrics.
"""

from typing import Any, Dict, Iterator, List, Optional
import os
import requests

try:
    import dlt
    HAS_DLT = True
except ImportError:
    HAS_DLT = False

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"


def _get_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    """Build request headers including API key if provided."""
    headers = {
        "Accept": "application/json",
        "User-Agent": "cognee-community-connector-coingecko/0.1.0",
    }
    key = api_key or os.getenv("COINGECKO_API_KEY")
    if key:
        headers["x-cg-demo-api-key"] = key
    return headers


def fetch_coins_markets(
    vs_currency: str = "usd",
    limit: int = 50,
    page: int = 1,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch cryptocurrency market snapshot data from CoinGecko API.

    Args:
        vs_currency: Target currency of market data (default: 'usd').
        limit: Number of results per page (1-250, default: 50).
        page: Page number of results.
        api_key: Optional CoinGecko demo or pro API key.

    Returns:
        List of coin market data dictionaries.
    """
    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": min(max(1, limit), 250),
        "page": page,
        "sparkline": "false",
        "price_change_percentage": "24h",
    }
    response = requests.get(
        url,
        headers=_get_headers(api_key),
        params=params,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def fetch_trending_coins(api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch top trending search coins from CoinGecko API."""
    url = f"{COINGECKO_BASE_URL}/search/trending"
    response = requests.get(
        url,
        headers=_get_headers(api_key),
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    coins = data.get("coins", [])
    return [c.get("item", {}) for c in coins]


def format_coin_to_document(coin: Dict[str, Any], vs_currency: str = "USD") -> str:
    """Format raw coin market data into a rich natural language document.

    This ensures optimal knowledge-graph extraction during Cognee's cognify step.
    """
    name = coin.get("name", "Unknown")
    symbol = (coin.get("symbol") or "").upper()
    rank = coin.get("market_cap_rank", "N/A")
    price = coin.get("current_price", 0.0)
    market_cap = coin.get("market_cap", 0)
    high_24h = coin.get("high_24h", 0.0)
    low_24h = coin.get("low_24h", 0.0)
    change_24h = coin.get("price_change_24h", 0.0)
    change_pct_24h = coin.get("price_change_percentage_24h", 0.0)
    total_volume = coin.get("total_volume", 0)
    circulating_supply = coin.get("circulating_supply", 0)
    last_updated = coin.get("last_updated", "N/A")

    return (
        f"# Cryptocurrency Snapshot: {name} ({symbol})\n\n"
        f"- Market Rank: #{rank}\n"
        f"- Current Price: ${price:,.4f} {vs_currency.upper()}\n"
        f"- Market Capitalization: ${market_cap:,.2f} {vs_currency.upper()}\n"
        f"- 24h High: ${high_24h:,.4f} | 24h Low: ${low_24h:,.4f}\n"
        f"- 24h Price Change: ${change_24h:+,.4f} ({change_pct_24h:+.2f}%)\n"
        f"- 24h Total Trading Volume: ${total_volume:,.2f}\n"
        f"- Circulating Supply: {circulating_supply:,.0f} {symbol}\n"
        f"- Snapshot Timestamp: {last_updated}\n"
    )


def fetch_coins_markets_documents(
    vs_currency: str = "usd",
    limit: int = 50,
    api_key: Optional[str] = None,
) -> List[str]:
    """Fetch market snapshots and return them formatted as markdown documents.

    Ideal for feeding directly into `await cognee.add(documents)`.
    """
    coins = fetch_coins_markets(
        vs_currency=vs_currency, limit=limit, api_key=api_key
    )
    return [format_coin_to_document(c, vs_currency) for c in coins]


if HAS_DLT:
    @dlt.source(name="coingecko")
    def coingecko_source(
        vs_currency: str = "usd",
        limit: int = 50,
        api_key: Optional[str] = None,
    ) -> Any:
        """DLT source for CoinGecko cryptocurrency data.

        Usable with `await cognee.remember(coingecko_source(...))` or dlt pipelines.
        """
        @dlt.resource(name="coins_markets", write_disposition="replace")
        def coins_markets_resource() -> Iterator[Dict[str, Any]]:
            coins = fetch_coins_markets(
                vs_currency=vs_currency,
                limit=limit,
                api_key=api_key,
            )
            for coin in coins:
                # Add formatted text body to allow document-mode ingestion
                coin["formatted_document"] = format_coin_to_document(coin, vs_currency)
                yield coin

        @dlt.resource(name="trending_coins", write_disposition="replace")
        def trending_coins_resource() -> Iterator[Dict[str, Any]]:
            trending = fetch_trending_coins(api_key=api_key)
            for item in trending:
                yield item

        return coins_markets_resource, trending_coins_resource
else:
    def coingecko_source(*args, **kwargs):  # type: ignore
        raise ImportError(
            "dlt is required to use coingecko_source(). "
            "Please install dlt: pip install dlt"
        )
