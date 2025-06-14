# Configurando Ollama para modelos grandes

## 1. Aumentar memória virtual (swap) no WSL

```bash
# Verificar swap atual
free -h

# Criar arquivo swap de 50GB
sudo fallocate -l 50G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Tornar permanente
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 2. Configurar Ollama para usar offloading

```bash
# Definir variáveis de ambiente
export OLLAMA_NUM_GPU=0  # Força uso de CPU
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_MODELS_DIR=/mnt/c/ollama_models  # Use disco do Windows

# Ou configure no systemd (se aplicável)
sudo systemctl edit ollama
```

## 3. Usar modelos quantizados

```bash
# Q2_K - Menor qualidade, menos memória (~26GB)
ollama pull llama3.3:70b-instruct-q2_K

# Q4_K_M - Melhor equilíbrio (~39GB)
ollama pull llama3.3:70b-instruct-q4_K_M
```

## 4. Configurar WSL para mais memória

Crie/edite `C:\Users\[seu-usuario]\.wslconfig`:

```ini
[wsl2]
memory=16GB  # Aumente se tiver mais RAM
swap=50GB
localhostForwarding=true
```

Depois reinicie o WSL:
```bash
wsl --shutdown
wsl
```

## Performance

⚠️ **Importante**: Usar swap tornará o modelo MUITO mais lento, mas funcionará.

### Tempos estimados:
- RAM pura: ~2-5 segundos por resposta
- Com swap: ~30-60 segundos por resposta

### Recomendação:
Para melhor experiência com 18GB RAM, use:
- **llama3.1:8b** - Excelente qualidade
- **mixtral:8x7b** - Muito bom (se tiver ~32GB com swap)
- **qwen2.5:14b** - Ótimo para português