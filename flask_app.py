#!/usr/bin/python3.10

# Este arquivo é usado pelo PythonAnywhere para servir a aplicação Flask
# Arquivo flask_app.py no diretório raiz da conta CicloCarioca.pythonanywhere.com

import sys
import os

# Adicione o caminho do projeto ao sys.path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Importar dotenv para carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de ambiente para produção
os.environ['FLASK_ENV'] = 'production'

# As demais variáveis sensíveis (SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD, GEMINI_API_KEY)
# são carregadas automaticamente do arquivo .env pelo load_dotenv()

# Importar a aplicação Flask
from app import app as application

# Para compatibilidade com PythonAnywhere
if __name__ == "__main__":
    application.run()