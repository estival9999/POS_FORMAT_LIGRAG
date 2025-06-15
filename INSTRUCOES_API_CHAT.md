# Instruções - Chat LightRAG via API

## 🔑 Informações de Acesso

- **URL do Servidor**: `https://7a05-168-194-80-252.ngrok-free.app`
- **API Key**: `sk-lightrag-estival-2024-secure-api-key-xyz789`

## 📋 Pré-requisitos

1. Python 3.6 ou superior
2. Biblioteca requests:
   ```bash
   pip install requests
   ```

## 🚀 Como Usar

### Opção 1: Usar o arquivo pronto

1. Abra o arquivo `chat_lightrag_api.py` 
2. Verifique se a URL e API Key estão corretas (linhas 93-94)
3. Execute:
   ```bash
   python chat_lightrag_api.py
   ```

### Opção 2: Código mínimo para integração

```python
import requests

# Configurações
URL = "https://7a05-168-194-80-252.ngrok-free.app"
API_KEY = "sk-lightrag-estival-2024-secure-api-key-xyz789"

# Função para enviar pergunta
def perguntar(texto):
    response = requests.post(
        f"{URL}/query",
        headers={"X-API-Key": API_KEY},
        json={
            "query": texto,
            "mode": "mix",
            "top_k": 30,
            "max_token_for_text_unit": 8000,
            "max_token_for_global_context": 8000,
            "max_token_for_local_context": 8000,
            "history_turns": 3,
            "response_type": "Multiple Paragraphs"
        }
    )
    return response.json()["response"]

# Exemplo de uso
resposta = perguntar("O que é inteligência artificial?")
print(resposta)
```

## 💬 Usando o Chat Interativo

Ao executar `chat_lightrag_api.py`, você verá:

```
============================================================
       💬 Chat LightRAG - Cliente Python
============================================================

🔍 Verificando conexão com o servidor...
✅ Conectado ao servidor LightRAG
   Status: healthy
   Modelo LLM: gpt-4o-mini

✅ Tudo pronto! Digite suas perguntas abaixo.
   Comandos especiais:
   - 'sair' ou 'exit' para encerrar
   - 'limpar' para limpar o histórico
   - 'ajuda' para ver este menu
------------------------------------------------------------

🤔 Você: O que é machine learning?

⏳ Processando...

🤖 LightRAG:
------------------------------------------------------------
Machine learning (aprendizado de máquina) é um subcampo da 
inteligência artificial que permite que sistemas aprendam e 
melhorem automaticamente a partir da experiência...
------------------------------------------------------------
```

## ⚙️ Configurações Automáticas

O sistema está configurado com:
- **Modo**: `mix` - Combina busca local e global para melhores resultados
- **Top K**: `30` - Recupera os 30 resultados mais relevantes
- **Max Tokens**: `8000` - Para cada tipo de contexto
- **History Turns**: `3` - Mantém as últimas 3 conversas para contexto
- **Response Type**: `Multiple Paragraphs` - Respostas detalhadas

## 🛠️ Solução de Problemas

### Erro de Conexão
- Verifique se a URL está correta
- Confirme que o servidor está online
- Teste a URL no navegador: https://xxx.ngrok-free.app/health

### Erro 403 - Forbidden
- A API Key está incorreta
- Verifique se copiou a chave completa

### Timeout
- Perguntas complexas podem demorar mais
- O timeout padrão é 60 segundos

## 📝 Exemplos de Uso Avançado

### Manter Contexto de Conversa
O chat mantém automaticamente o contexto das últimas 3 conversas.

### Integrar em Outro Sistema
```python
from chat_lightrag_api import ChatLightRAG

# Criar instância
chat = ChatLightRAG(
    "https://xxx.ngrok-free.app",
    "sk-lightrag-..."
)

# Enviar mensagem
resposta = chat.enviar_mensagem("Sua pergunta aqui")
print(resposta)
```

## ⚠️ Notas Importantes

1. **URL Temporária**: A URL do ngrok muda quando o servidor reinicia
2. **Segurança**: Não compartilhe a API Key
3. **Limite de Tokens**: Respostas muito longas podem ser truncadas
4. **Histórico**: O comando 'limpar' remove o contexto de conversa