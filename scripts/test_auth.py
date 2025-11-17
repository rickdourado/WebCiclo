#!/usr/bin/env python3
"""
Script para testar a autenticação com o banco de dados.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.auth_service import AuthService
from repositories.user_repository import UserRepository


def test_authentication():
    """Testa a autenticação de usuários"""
    
    print("=" * 70)
    print("🔐 TESTE DE AUTENTICAÇÃO")
    print("=" * 70)
    print()
    
    # Solicitar credenciais
    email = input("Email: ").strip()
    password = input("Senha: ").strip()
    
    if not email or not password:
        print("❌ Email e senha são obrigatórios!")
        return False
    
    print()
    print("🔄 Testando autenticação...")
    print()
    
    # Testar autenticação
    auth_service = AuthService()
    success, error_message, user_data = auth_service.authenticate_admin(email, password)
    
    if success and user_data:
        print("=" * 70)
        print("✅ AUTENTICAÇÃO BEM-SUCEDIDA!")
        print("=" * 70)
        print(f"   ID: {user_data['id']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Último acesso: {user_data.get('ultimo_acesso', 'Nunca')}")
        print("=" * 70)
        return True
    else:
        print("=" * 70)
        print("❌ FALHA NA AUTENTICAÇÃO")
        print("=" * 70)
        print(f"   Motivo: {error_message}")
        print("=" * 70)
        return False


def list_users():
    """Lista todos os usuários cadastrados"""
    
    print("=" * 70)
    print("👥 USUÁRIOS CADASTRADOS")
    print("=" * 70)
    print()
    
    try:
        import pymysql
        from dotenv import load_dotenv
        
        load_dotenv()
        
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'cursoscarioca'),
            charset=os.getenv('DB_CHARSET', 'utf8mb4'),
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, email, ativo, ultimo_acesso, created_at
                FROM users
                ORDER BY id
            """)
            users = cursor.fetchall()
            
            if users:
                for user in users:
                    status = "✅ Ativo" if user['ativo'] == 'sim' else "❌ Inativo"
                    print(f"ID: {user['id']}")
                    print(f"   Email: {user['email']}")
                    print(f"   Status: {status}")
                    print(f"   Último acesso: {user.get('ultimo_acesso', 'Nunca')}")
                    print(f"   Criado em: {user.get('created_at', 'N/A')}")
                    print()
                
                print(f"Total: {len(users)} usuário(s)")
            else:
                print("⚠️  Nenhum usuário cadastrado no banco de dados.")
                print()
                print("💡 Execute o script create_admin_user.py para criar o primeiro usuário.")
        
        connection.close()
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao listar usuários: {e}")
        print("=" * 70)
        return False


def main():
    """Função principal"""
    print()
    print("Escolha uma opção:")
    print("1. Testar autenticação")
    print("2. Listar usuários cadastrados")
    print()
    
    choice = input("Opção (1 ou 2): ").strip()
    print()
    
    try:
        if choice == '1':
            success = test_authentication()
        elif choice == '2':
            success = list_users()
        else:
            print("❌ Opção inválida!")
            success = False
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
