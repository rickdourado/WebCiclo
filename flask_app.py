#!/usr/bin/python3.10

# Este arquivo é usado pelo PythonAnywhere para servir a aplicação Flask
# Renomeie este arquivo para 'flask_app.py' no diretório raiz da sua conta PythonAnywhere

import sys
import os

# Adicione o caminho do seu projeto ao sys.path
# Substitua 'seuusuario' pelo seu nome de usuário no PythonAnywhere
# path = '/home/seuusuario/ciclo-carioca-v4'
# if path not in sys.path:
#     sys.path.append(path)

# Configurações de ambiente para produção
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'ciclo_carioca_v4_pythonanywhere_production_2025'

# Importar a aplicação Flask
from app import application

# Para compatibilidade com PythonAnywhere
if __name__ == "__main__":
    application.run()