# services/auth_service.py
"""
Serviço de autenticação com hash de senhas e validação segura.
Implementa bcrypt para hash de senhas e validação de credenciais.
Migrado para usar banco de dados MySQL ao invés de variáveis de ambiente.
"""

import bcrypt
import logging
from typing import Tuple, Optional, Dict, Any
from src.models.user_repository import UserRepository

logger = logging.getLogger(__name__)

class AuthService:
    """Serviço responsável pela autenticação e gerenciamento de senhas"""
    
    def __init__(self):
        """Inicializa o serviço de autenticação"""
        self.user_repository = UserRepository()
    
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
    
    def authenticate_admin(self, email: str, password: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Autentica credenciais do administrador usando banco de dados
        
        Args:
            email: Email do usuário (usado como username)
            password: Senha em texto plano
            
        Returns:
            Tupla (sucesso, mensagem_erro, dados_usuario)
        """
        try:
            # Validar entrada
            if not email or not password:
                return False, "Email e senha são obrigatórios", None
            
            # Buscar usuário no banco de dados
            user = self.user_repository.find_by_email(email)
            
            if not user:
                logger.warning(f"🔒 Tentativa de login com email não cadastrado: {email}")
                return False, "Credenciais inválidas", None
            
            # Verificar se usuário está ativo
            if user.get('ativo') != 'sim':
                logger.warning(f"🔒 Tentativa de login com usuário inativo: {email}")
                return False, "Usuário inativo", None
            
            # Verificar senha
            senha_hash = user.get('senha')
            if not senha_hash or not self.verify_password(password, senha_hash):
                logger.warning(f"🔒 Tentativa de login com senha inválida para: {email}")
                return False, "Credenciais inválidas", None
            
            # Atualizar último acesso
            self.user_repository.update_last_access(user['id'])
            
            logger.info(f"✅ Login bem-sucedido para usuário: {email}")
            
            # Retornar dados do usuário (sem a senha)
            user_data = {
                'id': user['id'],
                'email': user['email'],
                'ultimo_acesso': user.get('ultimo_acesso')
            }
            
            return True, None, user_data
            
        except Exception as e:
            logger.error(f"❌ Erro na autenticação: {e}")
            return False, "Erro interno de autenticação", None
    
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
    
    def create_user(self, email: str, password: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        Cria um novo usuário no sistema
        
        Args:
            email: Email do usuário
            password: Senha em texto plano
            
        Returns:
            Tupla (sucesso, mensagem_erro, user_id)
        """
        try:
            # Validar entrada
            if not email or not password:
                return False, "Email e senha são obrigatórios", None
            
            # Validar formato de email básico
            if '@' not in email or '.' not in email:
                return False, "Email inválido", None
            
            # Validar força da senha
            if len(password) < 6:
                return False, "Senha deve ter no mínimo 6 caracteres", None
            
            # Gerar hash da senha
            senha_hash = self.hash_password(password)
            
            # Criar usuário no banco
            user_id = self.user_repository.create_user(email, senha_hash)
            
            if not user_id:
                return False, "Email já cadastrado", None
            
            logger.info(f"✅ Usuário criado com sucesso: {email}")
            return True, None, user_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar usuário: {e}")
            return False, "Erro interno ao criar usuário", None