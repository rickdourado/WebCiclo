#!/bin/bash
# Script para ativar automaticamente o ambiente 'ciclo'

echo "🔄 Ativando ambiente conda 'ciclo'..."

# Verificar se conda está disponível
if ! command -v conda &> /dev/null; then
    echo "❌ Conda não encontrado. Instale o Anaconda/Miniconda primeiro."
    exit 1
fi

# Verificar se o ambiente 'ciclo' existe
if ! conda env list | grep -q "^ciclo "; then
    echo "❌ Ambiente 'ciclo' não encontrado."
    echo "📝 Criando ambiente 'ciclo'..."
    conda create -n ciclo python=3.13 -y
    echo "✅ Ambiente 'ciclo' criado com sucesso!"
fi

# Ativar o ambiente
echo "🚀 Ativando ambiente 'ciclo'..."
conda activate ciclo

# Verificar se as dependências estão instaladas
if [ -f "requirements.txt" ]; then
    echo "📦 Verificando dependências..."
    pip install -r requirements.txt
fi

echo "✅ Ambiente 'ciclo' ativado e pronto para uso!"
echo "🎯 Para executar o projeto: python app.py"