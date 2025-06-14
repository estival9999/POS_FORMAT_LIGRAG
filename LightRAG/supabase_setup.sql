-- Script de configuração do banco de dados Supabase para LightRAG
-- Execute este script no SQL Editor do Supabase

-- 1. Habilitar a extensão pgvector (se ainda não estiver habilitada)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Criar tabela para armazenamento KV (Key-Value)
CREATE TABLE IF NOT EXISTS lightrag_kv_storage (
    id TEXT PRIMARY KEY,
    data JSONB NOT NULL,
    namespace TEXT NOT NULL DEFAULT 'default',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índice para melhorar performance de busca por namespace
CREATE INDEX IF NOT EXISTS idx_kv_namespace ON lightrag_kv_storage(namespace);

-- 3. Criar tabela para armazenamento de vetores
CREATE TABLE IF NOT EXISTS lightrag_vectors (
    id TEXT PRIMARY KEY,
    embedding vector(768), -- Dimensão do nomic-embed-text
    metadata JSONB,
    namespace TEXT NOT NULL DEFAULT 'default',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índice para busca vetorial eficiente
CREATE INDEX IF NOT EXISTS idx_vectors_embedding ON lightrag_vectors 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Índice para namespace
CREATE INDEX IF NOT EXISTS idx_vectors_namespace ON lightrag_vectors(namespace);

-- 4. Criar tabela para status de documentos
CREATE TABLE IF NOT EXISTS lightrag_doc_status (
    doc_id TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK (status IN ('processed', 'processing', 'failed')),
    error_message TEXT,
    metadata JSONB,
    namespace TEXT NOT NULL DEFAULT 'default',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índice para busca por status e namespace
CREATE INDEX IF NOT EXISTS idx_doc_status ON lightrag_doc_status(status, namespace);

-- 5. Criar função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 6. Criar triggers para atualizar updated_at
CREATE TRIGGER update_kv_storage_updated_at BEFORE UPDATE
    ON lightrag_kv_storage FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_doc_status_updated_at BEFORE UPDATE
    ON lightrag_doc_status FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 7. Criar políticas RLS (Row Level Security) - opcional mas recomendado
ALTER TABLE lightrag_kv_storage ENABLE ROW LEVEL SECURITY;
ALTER TABLE lightrag_vectors ENABLE ROW LEVEL SECURITY;
ALTER TABLE lightrag_doc_status ENABLE ROW LEVEL SECURITY;

-- Política que permite acesso total (ajuste conforme necessário)
CREATE POLICY "Allow all operations" ON lightrag_kv_storage
    FOR ALL USING (true);

CREATE POLICY "Allow all operations" ON lightrag_vectors
    FOR ALL USING (true);

CREATE POLICY "Allow all operations" ON lightrag_doc_status
    FOR ALL USING (true);

-- 8. Comentários nas tabelas para documentação
COMMENT ON TABLE lightrag_kv_storage IS 'Armazenamento chave-valor para dados do LightRAG';
COMMENT ON TABLE lightrag_vectors IS 'Armazenamento de embeddings vetoriais para busca semântica';
COMMENT ON TABLE lightrag_doc_status IS 'Status de processamento de documentos';

COMMENT ON COLUMN lightrag_vectors.embedding IS 'Vetor de embedding com 768 dimensões (nomic-embed-text)';