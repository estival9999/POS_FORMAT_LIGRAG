#!/bin/bash
# Teste com curl no WSL

echo "🔍 Teste de API com curl"
echo "========================"

API_KEY="sk-lightrag-estival-2024-secure-api-key-xyz789"

echo -e "\n1. Teste /health sem API Key:"
curl -s http://localhost:9621/health | jq . || echo "Falhou"

echo -e "\n2. Teste /health com API Key:"
curl -s -H "X-API-Key: $API_KEY" http://localhost:9621/health | jq . || echo "Falhou"

echo -e "\n3. Teste /query com API Key:"
curl -s -X POST http://localhost:9621/query \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "teste",
    "mode": "hybrid",
    "top_k": 30
  }' | jq . || echo "Falhou"

echo -e "\n4. Teste auth-status:"
curl -s http://localhost:9621/auth-status | jq . || echo "Falhou"