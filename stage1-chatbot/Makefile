# Makefile for stage1-chatbot

# Start all containers (build if needed)
start:
	docker compose up -d --build

# Stop all containers
down:
	docker compose down

# Download a new model for Ollama (usage: make pull MODEL=tinyllama:1.1b)
pull:
	docker compose exec ollama sh -c 'ollama pull "$(MODEL)"'

# List all models available in Ollama
list:
	docker compose exec ollama ollama list

# Show available commands and usage
help:
	@echo "Available commands:"
	@echo "  make start         Start all containers (build if needed)"
	@echo "  make down          Stop all containers"
	@echo "  make pull MODEL=   Download a new model for Ollama (usage: make pull MODEL=tinyllama:1.1b)"
	@echo "  make list          List all models available in Ollama"
	@echo "  make help          Show this help message"

# Show logs for all services or a specific service (usage: make logs or make logs SERVICE=backend)
logs:
ifdef SERVICE
	docker compose logs -f $(SERVICE)
else
	docker compose logs -f
endif

# Restart all containers with rebuild (stop, rebuild, and start)
restart:
	docker compose down
	docker compose build --no-cache
	docker compose up -d
