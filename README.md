# ⚡ Week1 Alpha: Multi-Provider LLM Router CLI

A robust, production-ready CLI application that implements intelligent failover routing across multiple LLM providers: **Groq**, **Gemini**, and **Ollama**. Built with modern Python tooling, comprehensive logging, request validation, and graceful error handling.

---

## 🚀 Features

- **Asynchronous CLI Chat**: Interactive chat interface powered by async/await for responsive interactions.
- **Intelligent Failover**: Automatically routes requests with a cascade strategy:
  $$\text{Groq} \longrightarrow \text{Gemini} \longrightarrow \text{Ollama (Local/Self-hosted)}$$
- **Request/Response Validation**: Pydantic models validate all payloads, user inputs, and API responses.
- **Comprehensive Logging**: File and console logging with rotating file handlers, request/response tracking, and error diagnostics.
- **Graceful Error Handling**: Configuration validation at startup, network/timeout error handling, API failure recovery.
- **Resource Management**: Efficient connection pooling with HTTP/2 support via custom `httpx.AsyncClient`.
- **Robust Configuration**: Strictly validated environment settings using `pydantic-settings` with field validators.
- **Modern Toolchain**: Fully managed and run with **Astral's `uv`**, the ultra-fast Python package manager.

---

## 🛠️ Tech Stack

- **Async Runtime**: Python `asyncio` for concurrent execution
- **HTTP Client**: [HTTPX](https://www.python-httpx.org/) (with HTTP/2 support)
- **Local LLM Client**: [Ollama Python SDK](https://github.com/ollama/ollama-python)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/) & [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Logging**: Python `logging` module with rotating file handlers
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

### Start the CLI Chat

Launch the interactive chat interface:

```bash
uv run python -m src.main
```

You'll see:

```
--- Alpha LLM Chat ---
Type "exit" to quit
User: 
```

### Example Interaction

```
--- Alpha LLM Chat ---
Type "exit" to quit
User: What is machine learning?
AI: Machine learning is a subset of artificial intelligence that enables computers to learn from data and improve their performance on tasks without being explicitly programmed...
User: exit
Goodbye, Have a nice day
```

---

## 📋 Features in Detail

### 1. **Request Validation** (Pydantic)
- **User Input**: Prompts validated for length (1-10,000 characters)
- **API Payloads**: Groq, Gemini, and Ollama requests validated before sending
- **Responses**: LLM responses validated for provider, response text, and latency

**Models**:
- `UserInput`: Validates user prompts
- `Message`: Validates message structure (role: user/assistant/system)
- `GroqRequest`, `GeminiRequest`, `OllamaRequest`: Provider-specific payloads
- `LLMResponse`: Response structure with provider and latency tracking

### 2. **Logging** (Comprehensive)
- **File Location**: `logs/week1_alpha.log` (created automatically)
- **Log Levels**: INFO, DEBUG, WARNING, ERROR
- **What's Logged**:
  - Application startup and configuration validation
  - User prompts and responses
  - Provider selection and failover attempts
  - Request/response payloads (DEBUG level)
  - Errors and exceptions with full tracebacks
  - API latency metrics

**Log File Features**:
- Rotating file handler (5MB per file, 3 backups)
- Console + file output simultaneously
- Timestamped entries for debugging

### 3. **Error Handling** (Graceful)
- **Configuration Validation**: Startup checks for missing API keys, invalid URLs
- **Network Errors**: Timeout/connection errors caught and logged
- **API Failures**: 4xx/5xx errors trigger automatic failover
- **Rate Limiting**: 429 errors detected and handled per provider
- **User Input Errors**: Validation errors shown with helpful messages

**Error Output**:
```
❌ Configuration Error:
  - GROQ_API_KEY: GROQ_API_KEY is missing or empty. Check your .env file.

Please check your .env file and try again.
```

### 4. **Failover Strategy**
1. Try **Groq** (fast & reliable)
2. If Groq fails → Try **Gemini** 
3. If Gemini fails → Try **Ollama** (local fallback)
4. Log each transition with reason

---

## 🤖 API Usage (Legacy - Commented)

The FastAPI routes are currently commented in `src/main.py` but can be uncommented for future REST API support.

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
├── .env.example              # Template for API credentials
├── pyproject.toml            # Project metadata and uv dependencies
├── uv.lock                   # Pinned dependency lockfile
├── logs/                     # Logs directory (auto-created)
│   └── week1_alpha.log       # Application log file
├── src/
│   ├── main.py               # CLI chat application entry point
│   ├── clients/
│   │   └── httpx_client.py   # Shared, pooled Async HTTP client
│   ├── config/
│   │   ├── settings.py       # Pydantic BaseSettings with validation
│   │   └── logging_config.py # Logging configuration (file + console)
│   ├── schemas/
│   │   └── llm_schema.py     # Pydantic models for requests/responses
│   └── services/
│       ├── llm_router.py     # Priority & failover routing logic
│       ├── groq_services.py  # Groq API client with validation
│       ├── gemini_services.py# Gemini API client with validation
│       └── ollama_services.py# Ollama SDK client with validation
└── tests/
    └── test_ollama.py        # Async tests for Ollama provider
```

---

## � Troubleshooting

### Configuration Error at Startup

**Error**: `❌ Configuration Error: GROQ_API_KEY is missing or empty`

**Solution**: Ensure your `.env` file exists and contains all required API keys:
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### Validation Error on Input

**Error**: `❌ Validation Error: ensure this value has at most 10000 characters`

**Solution**: Your prompt exceeds 10,000 characters. Keep prompts shorter.

### Network Timeout

**Error**: `❌ Error: Groq network error: TimeoutError`

**Solution**: Check your internet connection. The application will automatically fallback to Gemini or Ollama.

### View Application Logs

Check the log file for detailed error information:
```bash
cat logs/week1_alpha.log
# Or follow logs in real-time
tail -f logs/week1_alpha.log
```

---

## �🛡️ License

This project is licensed under the MIT License.
