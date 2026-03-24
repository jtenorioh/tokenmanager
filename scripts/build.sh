#!/bin/bash

echo "🔧 Building Token Manager containers..."

cd "$(dirname "$0")/.."

# Build backend
docker build -t tokenmanager/backend:latest \
  --file docker/Dockerfile \
  .

# Build frontend
docker build -t tokenmanager/frontend:latest \
  --file docker/Dockerfile.frontend \
  ./frontend

echo "✅ Build complete!"
