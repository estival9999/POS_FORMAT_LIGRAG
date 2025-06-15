#!/usr/bin/env python3
"""
Chat LightRAG - Versão Funcionando
Testado e confirmado com o servidor
"""

import requests
import json

# Configuração
URL = "http://localhost:9621"
API_KEY = "sk-lightrag-estival-2024-secure-api-key-xyz789"

print("💬 Chat LightRAG")
print("-" * 50)

# Testar conexão
print("🔍 Verificando conexão...")
try:
    response = requests.get(
        f"{URL}/health",
        headers={"X-API-Key": API_KEY}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Conectado! Status: {data['status']}")
        print(f"   Modelo: {data['configuration']['llm_model']}")
    else:
        print(f"❌ Erro {response.status_code}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\nDigite 'sair' para encerrar")
print("-" * 50)

historico = []

while True:
    # Ler mensagem
    mensagem = input("\nVocê: ")
    
    if mensagem.lower() in ['sair', 'exit']:
        break
    
    if not mensagem.strip():
        continue
    
    # Preparar requisição
    payload = {
        "query": mensagem,
        "mode": "hybrid",
        "top_k": 30,
        "max_token_for_text_unit": 8000,
        "max_token_for_global_context": 8000,
        "max_token_for_local_context": 8000,
        "conversation_history": historico[-6:] if historico else None,
        "response_type": "Multiple Paragraphs",
        "history_turns": 3
    }
    
    # Enviar
    try:
        response = requests.post(
            f"{URL}/query",
            json=payload,
            headers={
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extrair resposta
            if isinstance(data, dict) and 'response' in data:
                resposta = data['response']
            elif isinstance(data, str):
                resposta = data
            else:
                resposta = json.dumps(data, ensure_ascii=False)
            
            print(f"\n🤖 LightRAG:\n{resposta}")
            
            # Atualizar histórico
            historico.append({"role": "user", "content": mensagem})
            historico.append({"role": "assistant", "content": resposta})
            
        else:
            print(f"\n❌ Erro {response.status_code}")
            print(f"Detalhes: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")

print("\n👋 Até logo!")