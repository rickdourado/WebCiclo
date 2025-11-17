#!/usr/bin/env python3
"""
Script de teste de conexão com o banco de dados MySQL.
Verifica a conectividade e lista todas as tabelas existentes.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar config
sys.path.insert(0, str(Path(__file__).parent.parent))

import pymysql
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


def test_database_connection():
    """Testa a conexão com o banco de dados e lista as tabelas."""
    
    print("=" * 70)
    print("🔍 TESTE DE CONEXÃO COM BANCO DE DADOS MYSQL")
    print("=" * 70)
    print()
    
    # Configurações do banco
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'cursoscarioca'),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4')
    }
    
    print("📋 Configurações carregadas:")
    print(f"   Host: {config['host']}")
    print(f"   Porta: {config['port']}")
    print(f"   Usuário: {config['user']}")
    print(f"   Banco: {config['database']}")
    print(f"   Charset: {config['charset']}")
    print()
    
    connection = None
    
    try:
        # Tenta conectar ao banco
        print("🔌 Tentando conectar ao banco de dados...")
        connection = pymysql.connect(**config)
        print("✅ Conexão estabelecida com sucesso!")
        print()
        
        # Obtém informações do servidor
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"📊 Versão do MySQL: {version}")
            print()
            
            # Lista todas as tabelas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"📁 Tabelas encontradas no banco '{config['database']}':")
                print("-" * 70)
                for idx, table in enumerate(tables, 1):
                    table_name = table[0]
                    print(f"\n   {idx}. {table_name}")
                    
                    # Obtém informações sobre cada tabela
                    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    count = cursor.fetchone()[0]
                    print(f"      └─ Registros: {count}")
                    
                    # Mostra estrutura da tabela
                    cursor.execute(f"DESCRIBE `{table_name}`")
                    columns = cursor.fetchall()
                    print(f"      └─ Colunas:")
                    for col in columns:
                        col_name = col[0]
                        col_type = col[1]
                        col_null = "NULL" if col[2] == "YES" else "NOT NULL"
                        col_key = f" [{col[3]}]" if col[3] else ""
                        print(f"         • {col_name}: {col_type} {col_null}{col_key}")
                    
                print("\n" + "-" * 70)
                print(f"\n✅ Total de tabelas: {len(tables)}")
            else:
                print(f"⚠️  Nenhuma tabela encontrada no banco '{config['database']}'")
                print("   O banco existe mas está vazio.")
        
        print()
        print("=" * 70)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"❌ Erro de conexão: {e}")
        print()
        print("💡 Possíveis causas:")
        print("   - MySQL não está rodando")
        print("   - Credenciais incorretas no arquivo .env")
        print("   - Host ou porta incorretos")
        print("   - Banco de dados não existe")
        return False
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
        
    finally:
        if connection:
            connection.close()
            print("\n🔌 Conexão fechada.")


if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
