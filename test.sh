#!/bin/bash
echo "🔍 Testing Flask app endpoints..."
curl -s http://localhost:5000/ | jq .
curl -s http://localhost:5000/users | jq .
