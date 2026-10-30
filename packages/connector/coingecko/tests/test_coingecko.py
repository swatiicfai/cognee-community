"""Unit tests for the Cognee CoinGecko connector."""

from unittest.mock import MagicMock, patch
import pytest
from cognee_community_connector_coingecko.coingecko import (
    _get_headers,
    coingecko_source,
    fetch_coins_markets,
    fetch_coins_markets_documents,
    fetch_trending_coins,
    format_coin_to_document,
)

SAMPLE_COIN_DATA = [
    {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 65000.0,
        "market_cap": 1280000000000,
        "market_cap_rank": 1,
        "total_volume": 25000000000,
        "high_24h": 66000.0,
        "low_24h": 64500.0,
        "price_change_24h": 500.0,
        "price_change_percentage_24h": 0.77,
        "circulating_supply": 19700000,
        "last_updated": "2026-10-30T12:00:00Z",
    },
    {
        "id": "ethereum",
        "symbol": "eth",
        "name": "Ethereum",
        "current_price": 2600.0,
        "market_cap": 310000000000,
        "market_cap_rank": 2,
        "total_volume": 12000000000,
        "high_24h": 2650.0,
        "low_24h": 2580.0,
        "price_change_24h": -20.0,
        "price_change_percentage_24h": -0.76,
        "circulating_supply": 120000000,
        "last_updated": "2026-10-30T12:00:00Z",
    },
]

SAMPLE_TRENDING_DATA = {
    "coins": [
        {
            "item": {
                "id": "solana",
                "coin_id": 4128,
                "name": "Solana",
                "symbol": "SOL",
                "market_cap_rank": 5,
            }
        }
    ]
}


def test_get_headers_without_key():
    headers = _get_headers(None)
    assert "Accept" in headers
    assert "x-cg-demo-api-key" not in headers


def test_get_headers_with_key():
    headers = _get_headers("test-demo-key-123")
    assert headers.get("x-cg-demo-api-key") == "test-demo-key-123"


def test_format_coin_to_document():
    doc = format_coin_to_document(SAMPLE_COIN_DATA[0], vs_currency="USD")
    assert "Cryptocurrency Snapshot: Bitcoin (BTC)" in doc
    assert "Market Rank: #1" in doc
    assert "$65,000.0000 USD" in doc
    assert "+0.77%" in doc


@patch("requests.get")
def test_fetch_coins_markets(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = SAMPLE_COIN_DATA
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    results = fetch_coins_markets(vs_currency="usd", limit=2)
    assert len(results) == 2
    assert results[0]["name"] == "Bitcoin"
    assert results[1]["name"] == "Ethereum"
    mock_get.assert_called_once()


@patch("requests.get")
def test_fetch_trending_coins(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = SAMPLE_TRENDING_DATA
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    results = fetch_trending_coins()
    assert len(results) == 1
    assert results[0]["name"] == "Solana"


@patch("requests.get")
def test_fetch_coins_markets_documents(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = SAMPLE_COIN_DATA
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    docs = fetch_coins_markets_documents(vs_currency="usd", limit=2)
    assert len(docs) == 2
    assert "Bitcoin" in docs[0]
    assert "Ethereum" in docs[1]


@patch("requests.get")
def test_coingecko_source_generator(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = SAMPLE_COIN_DATA
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    try:
        source_resources = coingecko_source(vs_currency="usd", limit=2)
        markets_res, trending_res = source_resources
        data = list(markets_res())
        assert len(data) == 2
        assert "formatted_document" in data[0]
    except ImportError:
        pytest.skip("dlt is not installed, skipping DLT resource test.")
