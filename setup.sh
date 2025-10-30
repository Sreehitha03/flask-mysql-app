#!/bin/bash
echo "🚀 Starting Flask + MySQL containers..."
docker-compose down -v
docker-compose build
docker-compose up -d
echo "✅ Containers are running! Visit: http://localhost:5000/"
