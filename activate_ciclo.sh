#!/bin/bash
# Ativação automática do ambiente 'ciclo' para WebCiclo
if command -v conda &> /dev/null; then
    conda activate ciclo
    echo "✅ Ambiente 'ciclo' ativado para WebCiclo"
else
    echo "❌ Conda não encontrado"
fi
