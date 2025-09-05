#!/usr/bin/python3.10

# Este arquivo é usado pelo PythonAnywhere para servir a aplicação Flask
# Arquivo flask_app.py no diretório raiz da conta PythonAnywhere

import sys
import os

# Adicione o caminho do projeto ao sys.path
path = '/home/rickdevarq/WebCiclo'
if path not in sys.path:
    sys.path.append(path)

# Configurações de ambiente para produção
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'ciclo_carioca_v4_pythonanywhere_production_2025'

# Importar a aplicação Flask
from app import app as application

# Para compatibilidade com PythonAnywhere
if __name__ == "__main__":
    application.run()