#!/bin/bash
# Script para fazer push usando Personal Access Token

echo "🔑 Configuração de Push para GitHub"
echo "=================================="
echo ""
echo "Você precisa de um Personal Access Token do GitHub."
echo ""
echo "Para criar um:"
echo "1. Acesse: https://github.com/settings/tokens/new"
echo "2. Dê um nome ao token (ex: 'LightRAG Push')"
echo "3. Selecione o escopo 'repo' (acesso completo)"
echo "4. Clique em 'Generate token'"
echo "5. Copie o token gerado"
echo ""
read -p "Cole seu Personal Access Token aqui: " TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ Token não pode estar vazio!"
    exit 1
fi

# Configura o remote com o token
echo "Configurando remote..."
git remote set-url origin https://${TOKEN}@github.com/estival9999/POS_FORMAT_LIGRAG.git

# Faz o push
echo "Fazendo push..."
git push origin master

if [ $? -eq 0 ]; then
    echo "✅ Push realizado com sucesso!"
    
    # Remove o token do remote por segurança
    echo "Removendo token do remote..."
    git remote set-url origin https://github.com/estival9999/POS_FORMAT_LIGRAG.git
    
    echo "✅ Concluído! Token removido por segurança."
else
    echo "❌ Erro ao fazer push"
    # Remove o token mesmo em caso de erro
    git remote set-url origin https://github.com/estival9999/POS_FORMAT_LIGRAG.git
fi