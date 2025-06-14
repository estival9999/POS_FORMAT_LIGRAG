"""
Script de configuração do LightRAG com Supabase
Modo híbrido: grafos locais, resto na nuvem
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from lightrag import LightRAG, QueryParam

# Carrega variáveis de ambiente
load_dotenv()

def verificar_configuracao():
    """Verifica se todas as variáveis necessárias estão configuradas"""
    variaveis_necessarias = [
        "POSTGRES_HOST",
        "POSTGRES_PORT", 
        "POSTGRES_DATABASE",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD"
    ]
    
    faltando = []
    for var in variaveis_necessarias:
        if not os.getenv(var):
            faltando.append(var)
    
    if faltando:
        print("❌ Variáveis de ambiente faltando:")
        for var in faltando:
            print(f"   - {var}")
        print("\n📝 Configure estas variáveis no arquivo .env")
        print("   Use .env.supabase.example como referência")
        return False
    
    print("✅ Todas as variáveis de ambiente configuradas!")
    return True

def criar_instancia_lightrag():
    """Cria uma instância do LightRAG com configuração híbrida"""
    
    # Diretório para grafos locais
    local_dir = "./rag_storage_hibrido"
    Path(local_dir).mkdir(exist_ok=True)
    
    # Inicializa LightRAG com storages específicos
    rag = LightRAG(
        working_dir=local_dir,
        llm_binding="ollama",
        llm_model="llama3.2:latest",
        llm_binding_host="http://localhost:11434",
        embedding_binding="ollama",
        embedding_model="nomic-embed-text:latest",
        embedding_dim=768,
        embedding_binding_host="http://localhost:11434",
        # Configuração de armazenamento híbrido
        kv_storage="PGKVStorage",           # Supabase
        vector_storage="PGVectorStorage",   # Supabase  
        graph_storage="NetworkXStorage",    # Local
        doc_status_storage="PGDocStatusStorage"  # Supabase
    )
    
    print("✅ LightRAG configurado com sucesso!")
    print(f"📁 Grafos locais em: {local_dir}")
    print("☁️  KV, vetores e status no Supabase")
    
    return rag

def testar_insercao(rag: LightRAG):
    """Testa inserção de um documento pequeno"""
    
    texto_teste = """
    Manual de Teste do Sistema Híbrido
    
    Este é um documento de teste para verificar a integração do LightRAG
    com o Supabase. O sistema utiliza uma arquitetura híbrida onde:
    
    1. Os grafos de conhecimento são armazenados localmente
    2. Os vetores de embedding são armazenados no Supabase
    3. O armazenamento chave-valor está no Supabase
    4. O status dos documentos é rastreado no Supabase
    
    Esta configuração permite escalabilidade e compartilhamento de dados
    entre múltiplas instâncias, mantendo a performance dos grafos locais.
    """
    
    print("\n📄 Inserindo documento de teste...")
    try:
        rag.insert(texto_teste)
        print("✅ Documento inserido com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inserir documento: {e}")
        return False

def testar_consulta(rag: LightRAG):
    """Testa diferentes modos de consulta"""
    
    pergunta = "O que é armazenado no Supabase?"
    
    print(f"\n🔍 Testando consulta: '{pergunta}'")
    print("-" * 50)
    
    modos = ["local", "global", "hybrid"]
    
    for modo in modos:
        print(f"\n📊 Modo {modo.upper()}:")
        try:
            resultado = rag.query(
                pergunta,
                param=QueryParam(mode=modo)
            )
            print(resultado[:200] + "..." if len(resultado) > 200 else resultado)
        except Exception as e:
            print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    
    print("🚀 Configuração do LightRAG com Supabase")
    print("=" * 50)
    
    # Verifica configuração
    if not verificar_configuracao():
        sys.exit(1)
    
    # Cria instância
    try:
        rag = criar_instancia_lightrag()
    except Exception as e:
        print(f"❌ Erro ao criar instância: {e}")
        print("\n💡 Dicas:")
        print("   1. Verifique se o Supabase está acessível")
        print("   2. Execute o script SQL de setup no Supabase")
        print("   3. Confirme as credenciais no arquivo .env")
        sys.exit(1)
    
    # Menu de opções
    while True:
        print("\n" + "=" * 50)
        print("📋 MENU:")
        print("1. Testar inserção de documento")
        print("2. Testar consultas")
        print("3. Inserir arquivo personalizado")
        print("4. Sair")
        
        escolha = input("\nEscolha uma opção: ")
        
        if escolha == "1":
            testar_insercao(rag)
        elif escolha == "2":
            if testar_insercao(rag):  # Garante que há dados
                testar_consulta(rag)
        elif escolha == "3":
            arquivo = input("Caminho do arquivo: ")
            if Path(arquivo).exists():
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                try:
                    rag.insert(conteudo)
                    print("✅ Arquivo inserido com sucesso!")
                except Exception as e:
                    print(f"❌ Erro: {e}")
            else:
                print("❌ Arquivo não encontrado")
        elif escolha == "4":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    main()