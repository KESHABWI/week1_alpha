# Week1 Alpha: Multi-Provider LLM Router CLI

A command-line interface (CLI) chat application that implements failover routing across multiple LLM providers: **Groq**, **Gemini**, and **Ollama**. Built with modern Python tooling, structured logging, request validation, real-time token streaming, and graceful error handling.

---

## Features

- **Asynchronous CLI Chat with Token Streaming**: Real-time token streaming for a responsive chat loop across all supported providers.
- **Intelligent Failover**: Automatically routes requests using a cascade strategy:
  $$\text{Groq} \longrightarrow \text{Gemini} \longrightarrow \text{Ollama (Local/Self-hosted)}$$
- **Request/Response Validation**: Pydantic models validate all payloads, user inputs, and API responses.
- **Session Chat History**: Tracks chat history during the active session to provide context for subsequent messages.
- **Structured Logging**: Automatic dual console and file logging with rotating file handlers, request/response tracking, and diagnostics.
- **Startup Configuration Validation**: Strictly validates environment settings using `pydantic-settings` with field validators before starting.
- **Connection Management**: Efficient connection pooling using a custom `httpx.AsyncClient`.
- **Modern Toolchain**: Fully managed and run with **Astral's `uv`**, the high-performance Python package manager.

---

## Tech Stack

- **Async Runtime**: Python `asyncio` for concurrent execution.
- **HTTP Client**: [HTTPX](https://www.python-httpx.org/) (with HTTP/2 support).
- **Local LLM Client**: [Ollama Python SDK](https://github.com/ollama/ollama-python).
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/) & [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).
- **Logging**: Python standard `logging` with rotating file handlers.
- **Package Manager**: [uv](https://github.com/astral-sh/uv).
- **Testing & Quality**: [pytest](https://docs.pytest.org/), [ruff](https://github.com/astral-sh/ruff), [mypy](https://mypy-lang.org/).

---

## Setup & Installation

This project uses [uv](https://github.com/astral-sh/uv) for environment setup and dependency management. No manual virtual environment creation or `pip` commands are required.

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
*This command automatically creates a local virtual environment (`.venv`), resolves all dependencies in `pyproject.toml`, and locks them into `uv.lock`.*

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

## Running the Application

### Start the CLI Chat

Launch the interactive chat interface using the following command:

```bash
uv run python -m src.chatbot.main
```

You will see:

```
--- Alpha LLM Chat ---
Type "exit" to quit
User: 
```

### Example Interaction

```
--- Alpha LLM Chat ---
Type "exit" to quit
User: Hello
AI: Hello! How can I help you today?
User: exit
Goodbye, Have a nice day
```

---

## Features in Detail

### 1. Request/Response Validation (Pydantic)
- **User Input**: Prompts validated for length (1–10,000 characters).
- **API Payloads**: Groq, Gemini, and Ollama requests validated before execution.
- **Responses**: Standardized `LLMResponse` payload containing the selected provider, text content, and connection/response latency metrics.

**Key Models (`src/chatbot/schemas/llm_schema.py`)**:
- `UserInput`: Validates user prompt constraints.
- `Message`: Validates prompt/message roles (e.g. `user`, `assistant`).
- `GroqRequest`, `GeminiRequest`, `OllamaRequest`: Provider-specific validated payloads.
- `LLMResponse`: Unified output schema with provider and latency tracking.

### 2. Logging & Monitoring
- **File Location**: `logs/week1_alpha.log` (created automatically).
- **Log Levels**: Standard INFO, DEBUG, WARNING, ERROR.
- **Capabilities**:
  - Application startup and configuration validation tracking.
  - Interactive user prompts and returned response text.
  - Failover attempts and provider transitions.
  - Raw JSON request/response payloads (at DEBUG level).
  - Exceptions and tracebacks.
  - Response latency measurements.

### 3. Graceful Error Handling & Resiliency
- **Configuration Verification**: Validates missing environment variables or malformed URLs at startup.
- **Network Failures**: Catches network/timeout exceptions, logs details, and triggers fallbacks.
- **HTTP/API Failures**: Handles 4xx/5xx responses from downstream services.
- **Rate Limiting**: Custom error classes detect 429 status codes and immediately bubble up or transition.

### 4. Failover Routing Logic
The application automatically cascades down the list of providers in the event of an error:
1. Try **Groq** (primary).
2. If Groq fails (network timeout, rate-limited, bad key) $\rightarrow$ Try **Gemini**.
3. If Gemini fails $\rightarrow$ Try **Ollama** (local/self-hosted fallback).
4. Returns the validated response once successful, logging the selected provider and total round-trip time.

---

## Testing & Quality Assurance

All verification commands are executed within the virtual environment managed by `uv`.

### Run Unit Tests

Execute the automated test suite (uses `pytest` and `pytest-asyncio`):

```bash
uv run pytest
```

### Code Quality (Linting & Formatting)

```bash
# Check for lint violations using Ruff
uv run ruff check

# Format source files using Ruff
uv run ruff format

# Static type verification
uv run mypy src
```

---

## Project Structure

```text
├── .env.example              # Template for API credentials
├── pyproject.toml            # Project metadata and uv dependencies
├── uv.lock                   # Pinned dependency lockfile
├── logs/                     # Logs directory (auto-created)
│   └── week1_alpha.log       # Application log file
├── src/
│   └── chatbot/              # Main application package
│       ├── __init__.py
│       ├── main.py           # CLI chat application entry point
│       ├── clients/
│       │   ├── __init__.py
│       │   └── httpx_client.py   # Shared, pooled Async HTTP client
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py       # Pydantic BaseSettings with validation
│       │   └── logging_config.py # Logging configuration (file + console)
│       ├── memory/
│       │   └── short_term.py     # Session history / short-term storage
│       ├── router/
│       │   └── llm_router.py     # Priority & failover routing logic
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── llm_schema.py     # Pydantic models for requests/responses
│       └── services/
│           ├── __init__.py
│           ├── groq_services.py  # Groq client with real-time streaming
│           ├── gemini_services.py# Gemini client with real-time streaming
│           └── ollama_services.py# Ollama client with real-time streaming
└── tests/
    ├── conftest.py           # Shared test fixtures & config
    ├── test_gemini.py        # Gemini client unit tests
    ├── test_groq.py          # Groq client unit tests
    └── test_ollama.py        # Ollama client unit tests
```

---

## Troubleshooting

### Configuration Error at Startup

> [!WARNING]
> If required environment settings are missing, the application will exit immediately on launch.

**Error**:
```
❌ Configuration Error:
  - GROQ_API_KEY: GROQ_API_KEY is missing or empty. Check your .env file.
```

**Solution**:
1. Check that `.env` is present in the project root.
2. Verify all API keys are populated.

### Input Validation Failures

**Error**:
```
❌ Validation Error: Invalid prompt: 1 validation error for UserInput ...
```

**Solution**: Ensure prompts are not empty and do not exceed the 10,000 character maximum limit.

### Monitoring Logs in Real-time

You can read or follow the diagnostic log file in your terminal:

```bash
# Follow logs in real-time
tail -f logs/week1_alpha.log
```

---

## �🛡️ License

This project is licensed under the MIT License.
