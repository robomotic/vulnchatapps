#!/bin/bash
set -e

# Check for docker compose or docker-compose
if command -v docker-compose &> /dev/null; then
  COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
  COMPOSE_CMD="docker compose"
else
  echo "[ERROR] Neither 'docker-compose' nor 'docker compose' is installed. Please install Docker Compose."
  exit 1
fi

echo "Pulling the TinyLlama model for Ollama (if not already present)..."
docker compose exec ollama ollama pull tinyllama:1.1b || true

echo "Building and starting stage1-chatbot containers..."
$COMPOSE_CMD up --build

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
  echo "\n[ERROR] One or more services failed to start. Check the logs above for details."
  exit $EXIT_CODE
else
  echo "\n[SUCCESS] stage1-chatbot is running. Access the frontend at http://localhost."
fi
