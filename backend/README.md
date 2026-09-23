# Bayan Backend

FastAPI backend service for Bayan.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/)

## Development Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```

3. **Run development server:**
   ```bash
   uv run uvicorn app.main:app --reload --port 4356
   ```

4. **Access endpoints:**
   - Health check: `http://127.0.0.1:4356/health`
   - API Docs: `http://127.0.0.1:4356/api/v1/openapi.json` (when `DEBUG=true`)

## Quality & Testing

- **Linting:**
  ```bash
  uv run ruff check .
  ```
- **Formatting:**
  ```bash
  uv run ruff format --check .
  ```
- **Type Checking:**
  ```bash
  uv run pyright
  ```
- **Tests:**
  ```bash
  uv run pytest
  ```
