#!/bin/bash

# =============================================================================
# SCRIPT DE INICIALIZAÇÃO - WEBCICLO CARIOCA
# =============================================================================
# Este script automatiza o processo de:
# 1. Subir o banco de dados via Docker (se necessário)
# 2. Executar as migrações do Alembic
# 3. Iniciar a aplicação Flask via UV
# =============================================================================

# Cores para o output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando ambiente WebCiclo Carioca...${NC}"

# 1. Verificar arquivo .env
if [ ! -f .env ]; then
    echo -e "${RED}❌ Erro: Arquivo .env não encontrado!${NC}"
    echo "Crie um arquivo .env baseado nas configurações do seu banco de dados."
    exit 1
fi

# 2. Iniciar Docker (Banco de Dados)
if command -v docker-compose &> /dev/null; then
    echo -e "${BLUE}📦 Verificando container do banco de dados (MariaDB)...${NC}"
    docker-compose up -d mariadb
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Banco de dados pronto ou iniciando.${NC}"
        # Pequena pausa para garantir que o MySQL aceite conexões
        echo -e "${YELLOW}⏳ Aguardando inicialização do banco (5s)...${NC}"
        sleep 5
    else
        echo -e "${YELLOW}⚠️ Falha ao iniciar containers via docker-compose. Verifique as permissões.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ docker-compose não encontrado. Certifique-se de que o banco de dados está rodando.${NC}"
fi

# 3. Executar Migrações do Alembic
echo -e "${BLUE}🔄 Sincronizando esquema do banco de dados (Alembic)...${NC}"
uv run alembic upgrade head
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migrações aplicadas com sucesso.${NC}"
else
    echo -e "${RED}❌ Erro ao aplicar migrações. Verifique a conexão com o banco.${NC}"
    exit 1
fi

# 4. Iniciar Aplicação Flask
echo -e "${BLUE}🌐 Iniciando servidor Flask (app.py) na porta 5001...${NC}"
echo -e "${YELLOW}Acesse: http://localhost:5001${NC}"
echo "-----------------------------------------------------------------------------"

uv run python app.py
