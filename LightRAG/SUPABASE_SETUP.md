# Configuração do LightRAG com Supabase

Este guia explica como configurar o LightRAG para usar o Supabase como armazenamento na nuvem, mantendo uma arquitetura híbrida para melhor performance.

## 🏗️ Arquitetura Híbrida

A solução implementada usa:
- **Grafos locais** (NetworkXStorage): Mantidos localmente para performance
- **Vetores** (PGVectorStorage): Armazenados no Supabase
- **Key-Value** (PGKVStorage): Armazenados no Supabase  
- **Status de docs** (PGDocStatusStorage): Armazenados no Supabase

## 📋 Pré-requisitos

1. Conta no [Supabase](https://supabase.com)
2. Ollama instalado com os modelos:
   - `llama3.2:latest`
   - `nomic-embed-text:latest`

## 🚀 Passos de Configuração

### 1. Criar Projeto no Supabase

1. Acesse [app.supabase.com](https://app.supabase.com)
2. Crie um novo projeto
3. Anote as credenciais:
   - Host: `seu-projeto.supabase.co`
   - Database: `postgres`
   - User: `postgres`
   - Password: sua senha do projeto
   - Port: `5432`

### 2. Configurar Banco de Dados

1. No painel do Supabase, vá para **SQL Editor**
2. Execute o script `supabase_setup.sql`:
   ```sql
   -- Cole e execute todo o conteúdo do arquivo supabase_setup.sql
   ```

3. Verifique se as tabelas foram criadas:
   - `lightrag_kv_storage`
   - `lightrag_vectors`
   - `lightrag_doc_status`

### 3. Configurar Variáveis de Ambiente

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.supabase.example .env
   ```

2. Edite o `.env` com suas credenciais:
   ```env
   # Configurações do Supabase
   POSTGRES_HOST=seu-projeto.supabase.co
   POSTGRES_PORT=5432
   POSTGRES_DATABASE=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=sua-senha-aqui
   ```

### 4. Testar a Configuração

Execute o script de teste:
```bash
python setup_supabase_lightrag.py
```

O script irá:
1. Verificar as variáveis de ambiente
2. Criar uma instância do LightRAG
3. Oferecer opções para testar inserção e consulta

## 📊 Monitoramento

No painel do Supabase você pode:
- Ver os dados nas tabelas (Table Editor)
- Monitorar queries (Database → Logs)
- Verificar uso de storage

## 🔧 Personalização

### Mudar Dimensão dos Embeddings

Se usar outro modelo de embedding, ajuste:
1. No `.env`: `EMBEDDING_DIM=nova_dimensao`
2. No SQL: `embedding vector(nova_dimensao)`

### Usar Connection String

Ao invés de variáveis separadas, você pode usar:
```env
DATABASE_URL=postgresql://postgres:senha@projeto.supabase.co:5432/postgres
```

## ⚠️ Considerações de Segurança

1. **Nunca commite o arquivo .env**
2. Use Row Level Security (RLS) no Supabase
3. Crie políticas de acesso específicas
4. Considere usar Service Role Key para produção

## 🐛 Troubleshooting

### Erro: "relation does not exist"
- Execute o script SQL de setup

### Erro: "connection refused"
- Verifique as credenciais no .env
- Confirme que o projeto Supabase está ativo

### Erro: "dimension mismatch"
- Verifique EMBEDDING_DIM no .env
- Confirme a dimensão do modelo de embedding

## 📈 Próximos Passos

1. **Otimização de Performance**:
   - Ajustar índices conforme volume de dados
   - Configurar connection pooling

2. **Backup e Recuperação**:
   - Configurar backups automáticos no Supabase
   - Exportar grafos locais periodicamente

3. **Monitoramento**:
   - Configurar alertas de uso
   - Monitorar performance de queries