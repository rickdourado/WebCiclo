#!/bin/bash
# Script para parar o WebCiclo
# Encerra processos rodando na porta 5001

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Porta padrão da aplicação
PORT=5001

echo -e "${YELLOW}🛑 Parando WebCiclo...${NC}"

# Verificar se a porta está em uso
PID=$(lsof -ti:${PORT})

if [ ! -z "$PID" ]; then
    echo -e "${YELLOW}🔍 Encontrado processo ${PID} na porta ${PORT}${NC}"
    echo -e "${YELLOW}🔪 Encerrando processo...${NC}"
    kill -9 $PID 2>/dev/null
    sleep 1
    
    # Verificar se o processo foi encerrado
    if lsof -ti:${PORT} > /dev/null 2>&1; then
        echo -e "${RED}❌ Erro: Não foi possível encerrar o processo${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ WebCiclo parado com sucesso${NC}"
    fi
else
    echo -e "${GREEN}✅ Nenhum processo rodando na porta ${PORT}${NC}"
fi
