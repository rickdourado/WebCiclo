#!/bin/bash
# Script de inicialização do WebCiclo
# Ativa o ambiente virtual e inicia a aplicação Flask

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Porta padrão da aplicação
PORT=5001

echo -e "${BLUE}🚀 Iniciando WebCiclo...${NC}"

# Verificar se a porta está em uso
echo -e "${YELLOW}🔍 Verificando porta ${PORT}...${NC}"
PID=$(lsof -ti:${PORT})

if [ ! -z "$PID" ]; then
    echo -e "${YELLOW}⚠️  Porta ${PORT} em uso pelo processo ${PID}${NC}"
    echo -e "${YELLOW}🔪 Encerrando processo...${NC}"
    kill -9 $PID 2>/dev/null
    sleep 1
    
    # Verificar se o processo foi encerrado
    if lsof -ti:${PORT} > /dev/null 2>&1; then
        echo -e "${RED}❌ Erro: Não foi possível encerrar o processo na porta ${PORT}${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ Porta ${PORT} liberada${NC}"
    fi
else
    echo -e "${GREEN}✅ Porta ${PORT} disponível${NC}"
fi

# Ativar ambiente virtual
echo -e "${GREEN}📦 Ativando ambiente virtual...${NC}"
source .venv/bin/activate

# Navegar para o diretório do backend
cd backend/app

# Iniciar aplicação Flask
echo -e "${GREEN}🌐 Iniciando servidor Flask...${NC}"
python main.py
