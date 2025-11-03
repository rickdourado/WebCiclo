# services/auth_service.py
"""
Serviço de autenticação com hash de senhas e validação segura.
Implementa bcrypt para hash de senhas e validação de credenciais.
"""

import bcrypt
import logging
from typing import Tuple, Optional
from config import Config

logger = logging.getLogger(__name__)

class AuthService:
    """Serviço responsável pela autenticação e gerenciamento de senhas"""
    
    def __init__(self):
        """Inicializa o serviço de autenticação"""
        self.admin_username = Config.ADMIN_USERNAME
        # Hash da senha admin na inicialização se necessário
        self._ensure_password_hash()
    
    def _ensure_password_hash(self) -> None:
        """Garante que a senha do admin esteja em formato hash"""
        # Se a senha no config não estiver em formato hash, fazer o hash
        if Config.ADMIN_PASSWORD and not Config.ADMIN_PASSWORD.startswith('$2b$'):
            logger.warning("⚠️ Senha do admin não está em formato hash. Convertendo...")
            hashed = self.hash_password(Config.ADMIN_PASSWORD)
            logger.info("✅ Senha do admin convertida para hash bcrypt")
            # Nota: Em produção, você deve atualizar o .env com o hash gerado
            Config.ADMIN_PASSWORD = hashed
    
    def hash_password(self, password: str) -> str:
        """
        Gera hash bcrypt da senha
        
        Args:
            password: Senha em texto plano
            
        Returns:
            Hash bcrypt da senha
        """
        try:
            # Gerar salt e hash da senha
            salt = bcrypt.gensalt(rounds=12)  # 12 rounds é um bom equilíbrio
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"❌ Erro ao gerar hash da senha: {e}")
            raise
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verifica se a senha corresponde ao hash
        
        Args:
            password: Senha em texto plano
            hashed: Hash bcrypt para comparação
            
        Returns:
            True se a senha for válida, False caso contrário
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            logger.error(f"❌ Erro ao verificar senha: {e}")
            return False
    
    def authenticate_admin(self, username: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Autentica credenciais do administrador
        
        Args:
            username: Nome de usuário
            password: Senha em texto plano
            
        Returns:
            Tupla (sucesso, mensagem_erro)
        """
        try:
            # Validar entrada
            if not username or not password:
                return False, "Usuário e senha são obrigatórios"
            
            # Verificar username
            if username != self.admin_username:
                logger.warning(f"🔒 Tentativa de login com usuário inválido: {username}")
                return False, "Credenciais inválidas"
            
            # Verificar senha
            if not self.verify_password(password, Config.ADMIN_PASSWORD):
                logger.warning(f"🔒 Tentativa de login com senha inválida para usuário: {username}")
                return False, "Credenciais inválidas"
            
            logger.info(f"✅ Login bem-sucedido para usuário: {username}")
            return True, None
            
        except Exception as e:
            logger.error(f"❌ Erro na autenticação: {e}")
            return False, "Erro interno de autenticação"
    
    def generate_password_hash_for_config(self, password: str) -> str:
        """
        Gera hash de senha para ser usado no arquivo de configuração
        
        Args:
            password: Senha em texto plano
            
        Returns:
            Hash bcrypt formatado para uso em configuração
        """
        hashed = self.hash_password(password)
        logger.info("🔐 Hash gerado para configuração:")
        logger.info(f"ADMIN_PASSWORD={hashed}")
        return hashed