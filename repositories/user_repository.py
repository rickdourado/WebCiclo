"""
Repositório para gerenciamento de usuários no banco de dados MySQL.
Responsável por todas as operações de persistência relacionadas a usuários.
"""

import pymysql
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class UserRepository:
    """Repositório para operações de usuários no banco de dados"""
    
    def __init__(self):
        """Inicializa o repositório com configurações do banco"""
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'cursoscarioca'),
            'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
            'cursorclass': pymysql.cursors.DictCursor
        }
    
    def _get_connection(self):
        """Cria e retorna uma conexão com o banco de dados"""
        try:
            connection = pymysql.connect(**self.db_config)
            return connection
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao banco de dados: {e}")
            raise
    
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca um usuário pelo email
        
        Args:
            email: Email do usuário
            
        Returns:
            Dicionário com dados do usuário ou None se não encontrado
        """
        connection = None
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                sql = """
                    SELECT id, email, senha, ativo, ultimo_acesso, created_at, updated_at
                    FROM users
                    WHERE email = %s AND ativo = 'sim'
                """
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                
                if user:
                    logger.info(f"✅ Usuário encontrado: {email}")
                else:
                    logger.warning(f"⚠️ Usuário não encontrado: {email}")
                
                return user
                
        except Exception as e:
            logger.error(f"❌ Erro ao buscar usuário por email: {e}")
            return None
        finally:
            if connection:
                connection.close()
    
    def update_last_access(self, user_id: int) -> bool:
        """
        Atualiza o último acesso do usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se atualizado com sucesso, False caso contrário
        """
        connection = None
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                sql = """
                    UPDATE users
                    SET ultimo_acesso = NOW()
                    WHERE id = %s
                """
                cursor.execute(sql, (user_id,))
                connection.commit()
                
                logger.info(f"✅ Último acesso atualizado para usuário ID: {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar último acesso: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection:
                connection.close()
    
    def create_user(self, email: str, senha_hash: str) -> Optional[int]:
        """
        Cria um novo usuário no banco de dados
        
        Args:
            email: Email do usuário
            senha_hash: Hash bcrypt da senha
            
        Returns:
            ID do usuário criado ou None em caso de erro
        """
        connection = None
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO users (email, senha, ativo, created_at, updated_at)
                    VALUES (%s, %s, 'sim', NOW(), NOW())
                """
                cursor.execute(sql, (email, senha_hash))
                connection.commit()
                
                user_id = cursor.lastrowid
                logger.info(f"✅ Usuário criado com sucesso: {email} (ID: {user_id})")
                return user_id
                
        except pymysql.err.IntegrityError as e:
            logger.warning(f"⚠️ Email já existe: {email}")
            if connection:
                connection.rollback()
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao criar usuário: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if connection:
                connection.close()
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Desativa um usuário (soft delete)
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se desativado com sucesso, False caso contrário
        """
        connection = None
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                sql = """
                    UPDATE users
                    SET ativo = 'nao', updated_at = NOW()
                    WHERE id = %s
                """
                cursor.execute(sql, (user_id,))
                connection.commit()
                
                logger.info(f"✅ Usuário desativado: ID {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro ao desativar usuário: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection:
                connection.close()
