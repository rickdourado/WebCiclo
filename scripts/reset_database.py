#!/usr/bin/env python3
"""
Script para resetar o banco de dados MySQL
Remove todos os dados das tabelas mantendo a estrutura
Autor: Sistema WebCiclo
Data: 2025-11-25
"""

import os
import sys
import pymysql
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'cursoscarioca'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


def get_db_connection():
    """Cria conexão com o banco de dados"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        logger.info("✅ Conexão com banco de dados estabelecida")
        return connection
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao banco: {e}")
        raise


def confirm_reset():
    """Solicita confirmação do usuário antes de resetar"""
    logger.warning("⚠️  ATENÇÃO: Esta ação irá DELETAR TODOS OS DADOS do banco de dados!")
    logger.warning("⚠️  As tabelas serão mantidas, mas todos os registros serão removidos.")
    logger.warning("")
    
    response = input("Digite 'CONFIRMAR' para prosseguir com o reset: ")
    
    return response.strip() == 'CONFIRMAR'


def get_table_stats(connection):
    """Obtém estatísticas das tabelas antes do reset"""
    stats = {}
    
    try:
        with connection.cursor() as cursor:
            # Lista de tabelas para verificar
            tables = ['cursos', 'turmas', 'turmas_dias_semana', 'plataformas_online', 'users']
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as total FROM {table}")
                result = cursor.fetchone()
                stats[table] = result['total']
        
        return stats
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {e}")
        return {}


def reset_database(connection, preserve_users=True):
    """
    Reseta o banco de dados removendo todos os dados
    
    Args:
        connection: Conexão com o banco de dados
        preserve_users: Se True, mantém os usuários admin
    """
    try:
        with connection.cursor() as cursor:
            logger.info("🔄 Desabilitando verificação de chaves estrangeiras...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Ordem de deleção respeitando as dependências
            tables_to_clear = [
                'turmas_dias_semana',
                'turmas',
                'plataformas_online',
                'cursos'
            ]
            
            if not preserve_users:
                tables_to_clear.append('users')
            
            logger.info("🗑️  Removendo dados das tabelas...")
            
            for table in tables_to_clear:
                cursor.execute(f"DELETE FROM {table}")
                affected = cursor.rowcount
                logger.info(f"   ✅ {table}: {affected} registros removidos")
            
            # Resetar AUTO_INCREMENT
            logger.info("🔄 Resetando contadores AUTO_INCREMENT...")
            
            reset_tables = {
                'cursos': 1,
                'turmas': 1,
                'turmas_dias_semana': 1,
                'plataformas_online': 1
            }
            
            if not preserve_users:
                reset_tables['users'] = 1
            
            for table, start_id in reset_tables.items():
                cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = {start_id}")
                logger.info(f"   ✅ {table}: AUTO_INCREMENT resetado para {start_id}")
            
            logger.info("🔄 Reabilitando verificação de chaves estrangeiras...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            connection.commit()
            logger.info("✅ Commit realizado com sucesso")
            
            return True
            
    except Exception as e:
        connection.rollback()
        logger.error(f"❌ Erro ao resetar banco de dados: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    logger.info("=" * 80)
    logger.info("🔄 RESET DO BANCO DE DADOS MySQL")
    logger.info("=" * 80)
    logger.info("")
    
    # Conectar ao banco
    connection = get_db_connection()
    
    try:
        # Obter estatísticas antes do reset
        logger.info("📊 Estatísticas atuais do banco de dados:")
        stats_before = get_table_stats(connection)
        
        for table, count in stats_before.items():
            logger.info(f"   • {table}: {count} registros")
        
        logger.info("")
        logger.info("-" * 80)
        logger.info("")
        
        # Solicitar confirmação
        if not confirm_reset():
            logger.info("❌ Reset cancelado pelo usuário")
            return 0
        
        logger.info("")
        logger.info("-" * 80)
        logger.info("")
        
        # Perguntar se deve preservar usuários
        preserve_users_input = input("Deseja manter os usuários admin? (s/N): ")
        preserve_users = preserve_users_input.strip().lower() in ['s', 'sim', 'y', 'yes']
        
        if preserve_users:
            logger.info("ℹ️  Usuários admin serão preservados")
        else:
            logger.info("⚠️  Todos os usuários serão removidos")
        
        logger.info("")
        logger.info("-" * 80)
        logger.info("")
        
        # Executar reset
        success = reset_database(connection, preserve_users)
        
        if success:
            logger.info("")
            logger.info("-" * 80)
            logger.info("")
            logger.info("📊 Estatísticas após o reset:")
            stats_after = get_table_stats(connection)
            
            for table, count in stats_after.items():
                logger.info(f"   • {table}: {count} registros")
            
            logger.info("")
            logger.info("=" * 80)
            logger.info("🎉 RESET CONCLUÍDO COM SUCESSO!")
            logger.info("=" * 80)
            logger.info("")
            logger.info("📝 Próximos passos:")
            logger.info("   1. Execute o script de migração para popular o banco:")
            logger.info("      python scripts/migrate_csv_to_mysql.py")
            logger.info("")
            
            if not preserve_users:
                logger.info("   2. Crie um novo usuário admin:")
                logger.info("      python scripts/create_admin_user.py")
                logger.info("")
            
            return 0
        else:
            logger.error("❌ Reset falhou!")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        connection.close()
        logger.info("🔌 Conexão com banco de dados fechada")


if __name__ == '__main__':
    exit(main())
