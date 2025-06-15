#!/usr/bin/env python3
"""
Cliente de Chat para LightRAG via API
Configurado com parâmetros fixos para melhor performance
"""

import requests
import sys

class ChatLightRAG:
    def __init__(self, base_url: str, api_key: str):
        """
        Inicializa o cliente de chat
        
        Args:
            base_url: URL do servidor LightRAG (ex: https://xxx.ngrok-free.app)
            api_key: Chave de API para autenticação
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        self.historico = []
    
    def verificar_conexao(self) -> bool:
        """Verifica se o servidor está acessível"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                headers=self.headers,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Conectado ao servidor LightRAG")
                print(f"   Status: {data.get('status')}")
                print(f"   Modelo LLM: {data.get('configuration', {}).get('llm_model')}")
                return True
            else:
                print(f"❌ Erro ao conectar: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
    
    def enviar_mensagem(self, mensagem: str) -> str:
        """
        Envia uma mensagem para o chat e retorna a resposta
        
        Args:
            mensagem: Texto da pergunta/mensagem
            
        Returns:
            Resposta do sistema ou None em caso de erro
        """
        # Configurações FIXAS conforme solicitado
        payload = {
            "query": mensagem,
            "mode": "mix",
            "top_k": 30,
            "max_token_for_text_unit": 8000,
            "max_token_for_global_context": 8000,
            "max_token_for_local_context": 8000,
            "history_turns": 3,
            "response_type": "Multiple Paragraphs",
            "conversation_history": self.historico[-6:] if self.historico else None
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/query",
                json=payload,
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code == 200:
                resposta_texto = response.json().get("response", "")
                
                # Atualizar histórico
                self.historico.append({"role": "user", "content": mensagem})
                self.historico.append({"role": "assistant", "content": resposta_texto})
                
                # Manter apenas últimas 3 conversas (6 mensagens)
                if len(self.historico) > 6:
                    self.historico = self.historico[-6:]
                
                return resposta_texto
            else:
                print(f"❌ Erro na API: {response.status_code}")
                print(f"   Detalhes: {response.text}")
                return None
                
        except requests.Timeout:
            print("⏱️  Timeout - a resposta está demorando muito")
            return None
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return None
    
    def limpar_historico(self):
        """Limpa o histórico de conversas"""
        self.historico = []
        print("🧹 Histórico limpo!")


def main():
    """Função principal do chat"""
    # Configurações de conexão
    # IMPORTANTE: Substitua estes valores!
    SERVIDOR_URL = "https://7a05-168-194-80-252.ngrok-free.app"  # URL do ngrok
    API_KEY = "sk-lightrag-estival-2024-secure-api-key-xyz789"   # Chave API
    
    print("=" * 60)
    print("       💬 Chat LightRAG - Cliente Python")
    print("=" * 60)
    print()
    
    # Criar cliente
    chat = ChatLightRAG(SERVIDOR_URL, API_KEY)
    
    # Verificar conexão
    print("🔍 Verificando conexão com o servidor...")
    if not chat.verificar_conexao():
        print("\n❌ Não foi possível conectar ao servidor.")
        print("   Verifique a URL e a chave API.")
        sys.exit(1)
    
    print("\n✅ Tudo pronto! Digite suas perguntas abaixo.")
    print("   Comandos especiais:")
    print("   - 'sair' ou 'exit' para encerrar")
    print("   - 'limpar' para limpar o histórico")
    print("   - 'ajuda' para ver este menu")
    print("-" * 60)
    
    # Loop principal do chat
    while True:
        try:
            # Ler entrada do usuário
            pergunta = input("\n🤔 Você: ").strip()
            
            # Comandos especiais
            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Até logo!")
                break
            elif pergunta.lower() == 'limpar':
                chat.limpar_historico()
                continue
            elif pergunta.lower() == 'ajuda':
                print("\n📋 Comandos disponíveis:")
                print("   - Digite qualquer pergunta para conversar")
                print("   - 'limpar' - limpa o histórico de conversa")
                print("   - 'sair' - encerra o programa")
                continue
            elif not pergunta:
                continue
            
            # Enviar mensagem
            print("\n⏳ Processando...")
            resposta = chat.enviar_mensagem(pergunta)
            
            if resposta:
                print("\n🤖 LightRAG:")
                print("-" * 60)
                print(resposta)
                print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrompido. Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")


if __name__ == "__main__":
    main()