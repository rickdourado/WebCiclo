# config.py
# Módulo de configuração centralizada para o WebCiclo

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Configurações centralizadas da aplicação"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ciclo_carioca_v4_pythonanywhere_2025')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configurações de upload
    UPLOAD_FOLDER = os.path.join('static', 'images', 'uploads')
    LOGO_PARCEIROS_FOLDER = os.path.join('static', 'images', 'LOGOPARCEIROS')
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
    
    # Configurações de diretórios
    CSV_DIR = 'CSV'
    PDF_DIR = 'PDF'
    ID_FILE = 'last_id.json'
    
    # Configurações de API
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    # Configurações de autenticação
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    
    # Configurações de validação
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 2000
    MAX_PARTNER_NAME_LENGTH = 100
    
    @classmethod
    def validate_required_config(cls):
        """Valida se todas as configurações obrigatórias estão definidas"""
        required_configs = [
            ('ADMIN_USERNAME', cls.ADMIN_USERNAME),
            ('ADMIN_PASSWORD', cls.ADMIN_PASSWORD),
        ]
        
        missing_configs = []
        for config_name, config_value in required_configs:
            if not config_value:
                missing_configs.append(config_name)
        
        if missing_configs:
            raise ValueError(f'Configurações obrigatórias não definidas: {", ".join(missing_configs)}')
        
        return True

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configurações para testes"""
    DEBUG = True
    TESTING = True
    CSV_DIR = 'test_csv'
    PDF_DIR = 'test_pdf'

# Configuração padrão baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
