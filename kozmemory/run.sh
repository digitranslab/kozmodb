#!/bin/bash

set -e

echo "🚀 Starting KozMemory installation..."

# Set environment variables
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
USER="${USER:-$(whoami)}"
NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8765}"

if [ -z "$OPENAI_API_KEY" ]; then
  echo "❌ OPENAI_API_KEY not set. Please run with: curl -sL https://raw.githubusercontent.com/digitranslab/kozmodb/main/kozmemory/run.sh | OPENAI_API_KEY=your_api_key bash"
  echo "❌ OPENAI_API_KEY not set. You can also set it as global environment variable: export OPENAI_API_KEY=your_api_key"
  exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "❌ Docker not found. Please install Docker first."
  exit 1
fi

# Check if docker compose is available
if ! docker compose version &> /dev/null; then
  echo "❌ Docker Compose not found. Please install Docker Compose V2."
  exit 1
fi

# Check if the container "kozmodb_ui" already exists and remove it if necessary
if [ $(docker ps -aq -f name=kozmodb_ui) ]; then
  echo "⚠️ Found existing container 'kozmodb_ui'. Removing it..."
  docker rm -f kozmodb_ui
fi

# Find an available port starting from 3000
echo "🔍 Looking for available port for frontend..."
for port in {3000..3010}; do
  if ! lsof -i:$port >/dev/null 2>&1; then
    FRONTEND_PORT=$port
    break
  fi
done

if [ -z "$FRONTEND_PORT" ]; then
  echo "❌ Could not find an available port between 3000 and 3010"
  exit 1
fi

# Export required variables for Compose and frontend
export OPENAI_API_KEY
export USER
export NEXT_PUBLIC_API_URL
export NEXT_PUBLIC_USER_ID="$USER"
export FRONTEND_PORT

# Create docker-compose.yml file
echo "📝 Creating docker-compose.yml..."
cat > docker-compose.yml <<EOF
services:
  kozmodb_store:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - kozmodb_storage:/kozmodb/storage
  kozmemory-mcp:
    image: kozmodb/kozmemory-mcp:latest
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - USER=${USER}
      - QDRANT_HOST=kozmodb_store
      - QDRANT_PORT=6333
    depends_on:
      - kozmodb_store
    ports:
      - "8765:8765"

volumes:
  kozmodb_storage:
EOF

# Start services
echo "🚀 Starting backend services..."
docker compose up -d

# Start the frontend
echo "🚀 Starting frontend on port $FRONTEND_PORT..."
docker run -d \
  --name kozmodb_ui \
  -p ${FRONTEND_PORT}:3000 \
  -e NEXT_PUBLIC_API_URL="$NEXT_PUBLIC_API_URL" \
  -e NEXT_PUBLIC_USER_ID="$USER" \
  kozmodb/kozmemory-ui:latest

echo "✅ Backend:  http://localhost:8765"
echo "✅ Frontend: http://localhost:$FRONTEND_PORT"

# Open the frontend URL in the default web browser
echo "🌐 Opening frontend in the default browser..."
URL="http://localhost:$FRONTEND_PORT"

if command -v xdg-open > /dev/null; then
  xdg-open "$URL"        # Linux
elif command -v open > /dev/null; then
  open "$URL"            # macOS
elif command -v start > /dev/null; then
  start "$URL"           # Windows (if run via Git Bash or similar)
else
  echo "⚠️ Could not detect a method to open the browser. Please open $URL manually."
fi
