#!/bin/bash

echo "🚀 Deploying Token Manager..."

cd "$(dirname "$0")/.."

# Ensure build exists
if ! docker image ls tokenmanager/backend:latest | grep -q tokenmanager; then
    echo "⚠️  Build not found, running build first..."
    ./scripts/build.sh
fi

# Stop and remove existing containers
docker-compose down || true

# Start new containers
docker-compose up -d

echo "✅ Deployment complete!"
echo "📱 Frontend: http://localhost:7777"
echo "🔧 Backend: http://localhost:7776"
