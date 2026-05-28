# ⚡ Week1 Alpha: Multi-Provider LLM Router

A high-performance, asynchronous FastAPI application that implements a robust failover routing mechanism across multiple LLM providers: **Groq**, **Gemini**, and **Ollama**. Built with modern Python tooling and optimized for speed and reliability.

---

## 🚀 Features

- **Asynchronous Routing**: Asynchronous endpoints built on top of FastAPI and `httpx`.
- **Intelligent Failover**: Automatically routes requests with a cascade strategy:
  $$\text{Groq} \longrightarrow \text{Gemini} \longrightarrow \text{Ollama (Local/Self-hosted)}$$
- **Resource Management**: Efficient connection pooling with HTTP/2 support via custom `httpx.AsyncClient` lifecycle management.
- **Robust Configuration**: Strictly validated environment settings utilizing `pydantic-settings`.
- **Modern Toolchain**: Fully managed and run with **Astral's `uv`**, the ultra-fast Python package manager.

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **HTTP Client**: [HTTPX](https://www.python-httpx.org/) (with HTTP/2 support)
- **Local LLM Client**: [Ollama Python SDK](https://github.com/ollama/ollama-python)
- **Settings & Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/) & [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Testing & Quality**: [pytest](https://docs.pytest.org/), [ruff](https://github.com/astral-sh/ruff), [mypy](https://mypy-lang.org/)

---

## 📦 Setup & Installation

This project is fully optimized to use [uv](https://github.com/astral-sh/uv) for lightning-fast environment setup and dependency management. No manual virtualenv creation or `pip` commands are required.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd week1_alpha
```

### 2. Project Bootstrapping

Install `uv` (if not already installed):

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Homebrew (macOS)
brew install uv
```

Sync and initialize the virtual environment and install all dependencies:

```bash
uv sync
```
*This command automatically creates a virtual environment (`.venv`), resolves all dependencies in `pyproject.toml`, and locks them into `uv.lock`.*

### 3. Environment Variables Configuration

Copy the example configuration to your local environment file:

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys and configuration parameters:

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OLLAMA_API_KEY=your_ollama_api_key_here
```

---

## 🏃 Running the Application

### Start the FastAPI Dev Server

Launch the server with live-reloading enabled using `uv run`:

```bash
uv run uvicorn src.main:app --reload
```

The application will start, and you can access:
- **API Endpoint**: `http://127.0.0.1:8000`
- **Interactive API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🤖 API Usage

### `/chat` Endpoint (POST)

Submit a prompt to be processed by the active/fallback LLM provider.

#### Request

- **URL**: `/chat`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Payload**:

```json
{
  "prompt": "Explain the concept of quantum computing in one simple sentence."
}
```

#### Curl Command

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain the concept of quantum computing in one simple sentence."}'
```

#### Response

```json
{
  "provider_response": {
    "provider": "groq",
    "response": "Quantum computing is a type of computing that uses quantum mechanics principles, such as superposition and entanglement, to perform calculations much faster than classical computers.",
    "latency_ms": 342.5
  }
}
```

---

## 🧪 Testing & Quality Assurance

All verification commands are executed within the sandbox environment managed by `uv`.

### Run Unit Tests

Execute the test suite (uses `pytest` and `pytest-asyncio`):

```bash
uv run pytest
```

### Code Quality (Linting & Formatting)

Check and automatically format files according to the project style guide:

```bash
# Check for lint violations using Ruff
uv run ruff check

# Format all source files
uv run ruff format

# Static Type Verification
uv run mypy src
```

---

## 📂 Project Structure

```text
├── .env.example             # Template for API credentials
├── pyproject.toml           # Project metadata and uv dependencies
├── uv.lock                  # Pinned dependency lockfile
├── src/
│   ├── main.py              # Application entry point & API routes
│   ├── clients/
│   │   └── httpx_client.py  # Shared, pooled Async HTTP client
│   ├── config/
│   │   └── settings.py      # Pydantic BaseSettings config
│   ├── schemas/
│   │   └── llm_schema.py    # LLM request/response Pydantic models
│   └── services/
│       ├── llm_router.py    # Priority & failover routing service
│       ├── groq_services.py # Groq API client service
│       ├── gemini_services.py# Gemini API client service
│       └── ollama_services.py# Ollama API/SDK client service
└── tests/
    └── test_ollama.py       # Async tests for LLM providers
```

---

## 🛡️ License

This project is licensed under the MIT License.
