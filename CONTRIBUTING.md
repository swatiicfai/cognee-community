# Contributing to Cognee Community Connectors

Thank you for your interest in expanding the Cognee ecosystem! We welcome contributions for new connectors, bug fixes, documentation improvements, and tests.

## Adding a New Connector

To add a new data-source connector (e.g. for Slack, Linear, Notion, GitHub):

1. **Create Package Directory:**
   ```text
   packages/connector/<connector_name>/
   ├── cognee_community_connector_<connector_name>/
   │   ├── __init__.py
   │   └── <connector_name>.py
   ├── examples/
   │   └── example.py
   ├── tests/
   │   └── test_<connector_name>.py
   ├── pyproject.toml
   └── README.md
   ```

2. **Implement Both Ingestion Paradigms:**
   - **Document Mode:** Return structured Markdown text or Cognee document objects for `cognee.add()` and `cognee.cognify()`.
   - **DLT Source Mode:** Provide a `dlt` source generator function for streaming via `cognee.remember()`.

3. **Add Tests:**
   Use `pytest` with mocked HTTP responses (e.g. using `responses` or `unittest.mock`) to test endpoints without requiring live API keys.

4. **Document:**
   Include a clear `README.md` and runnable `examples/example.py`.

## Pull Requests

1. Fork the repository.
2. Create your feature branch (`git checkout -b feat/my-connector`).
3. Commit your changes (`git commit -m 'feat: add <name> connector'`).
4. Push to your branch (`git push origin feat/my-connector`).
5. Open a Pull Request!
