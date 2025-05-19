# PharmaCare Stage 1 Chatbot

A local, containerized customer support chatbot demo for a pretend online pharmacy (PharmaCare). This project demonstrates a progression from a simple LLM-based chatbot to a flexible, API-configurable support assistant. The chatbot UI is embedded in a modern, responsive pharmacy website.

## Features
- **Frontend**: Modern Bootstrap-based pharmacy site with a chat widget (bottom right or in the last column on desktop)
- **Backend**: Python FastAPI server with support for multiple LLM providers:
  - Ollama (local, default)
  - OpenAI API
  - OpenRouter API
  - Gemini API
  - Anthropic API
- **Model selection**: Choose model and provider via environment variables
- **Error handling**: User-friendly error dialogs for backend/model errors
- **Containerized**: All services run via Docker Compose
- **Makefile**: Helper commands for common tasks (start, stop, logs, model management)

## Project Structure
```
stage1-chatbot/
  docker-compose.yml         # Orchestrates all services
  launch.sh                  # (Legacy) Bash script for launching the stack
  Makefile                   # Helper commands for dev workflow
  ollama.Dockerfile          # Custom Ollama image config
  backend/
    app.py                   # FastAPI backend (configurable for multiple LLM APIs)
    Dockerfile               # Backend container
    requirements.txt         # Python dependencies
  frontend/
    index.html               # Main pharmacy site + chatbot widget
    style.css                # Custom and Bootstrap styles
    app.js                   # Chatbot UI logic and error handling
    Dockerfile               # Frontend container (Nginx)
```

## Quick Start
1. **Build and start all services in the background:**
   ```sh
   make start
   ```
   Or, to restart and rebuild everything:
   ```sh
   make restart
   ```

2. **Access the site:**
   - Open [http://localhost](http://localhost) in your browser.

3. **View logs:**
   - All services: `make logs`
   - Specific service: `make logs SERVICE=backend`

4. **Stop all services:**
   ```sh
   make down
   ```

## Model Management (Ollama)
- **Download a new model:**
  ```sh
  make pull MODEL=tinyllama:1.1b
  make pull MODEL=llama3:8b-q4_K_M
  ```
- **List available models:**
  ```sh
  make list
  ```

## Configuration
All major settings are controlled via environment variables in `docker-compose.yml` (backend service):
- `API_PROVIDER`: `ollama` (default), `openai`, `openrouter`, `gemini`, `anthropic`
- `OLLAMA_MODEL`: Model name for Ollama/OpenAI/etc (e.g. `tinyllama:1.1b`, `gpt-3.5-turbo`)
- `OLLAMA_HOST`, `OLLAMA_PORT`: Ollama service connection (default: `ollama:11434`)
- `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`: API keys for cloud providers
- `DEBUG`: Set to `True` for verbose backend error logging

## Error Handling
- If the backend or model returns an error (e.g., out of memory, invalid API key), the chatbot UI will display a clear error dialog with the backend's error message.

## Customization
- **Switch LLM provider:** Edit `API_PROVIDER` in `docker-compose.yml` and provide the relevant API key.
- **Change model:** Edit `OLLAMA_MODEL` (or equivalent for your provider).
- **UI tweaks:** Edit `frontend/index.html` and `frontend/style.css`.

## Requirements
- Docker and Docker Compose (v2 syntax)
- (Optional) Make (for Makefile commands)

## Development Notes
- The backend supports easy extension for new LLM APIs.
- The frontend is designed for easy integration into any modern web app.
- For local LLMs, ensure your system has enough RAM for the selected model (see Ollama error messages).

---

**PharmaCare Stage 1 Chatbot** is a foundation for building more advanced, production-ready customer support bots with RAG, tools, and multi-agent orchestration.
