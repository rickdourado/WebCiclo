#!/usr/bin/env python3
"""
Script para criar usuário administrador no banco de dados.
Usa as credenciais do arquivo .env como base para criar o primeiro usuário.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.auth_service import AuthService
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


def create_admin_user():
    """Cria o usuário administrador no banco de dados"""
    
    print("=" * 70)
    print("🔐 CRIAÇÃO DE USUÁRIO ADMINISTRADOR")
    print("=" * 70)
    print()
    
    # Obter credenciais do .env
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password_env = os.getenv('ADMIN_PASSWORD', '')
    
    # Solicitar email válido
    print("💡 O sistema agora usa email para autenticação.")
    print()
    
    default_email = f"{admin_username}@cicloscarioca.rio" if '@' not in admin_username else admin_username
    email_input = input(f"Digite o email do administrador [{default_email}]: ").strip()
    admin_email = email_input if email_input else default_email
    
    # Se a senha no .env for um hash, pedir nova senha
    if admin_password_env.startswith('$2b$'):
        print()
        print("⚠️  A senha no .env está em formato hash.")
        print("    Por favor, digite a senha em texto plano para criar o usuário.")
        print()
        admin_password = input("Digite a senha do administrador: ").strip()
        
        if not admin_password:
            print("❌ Senha não pode ser vazia!")
            return False
    else:
        print()
        password_input = input(f"Digite a senha [{admin_password_env}]: ").strip()
        admin_password = password_input if password_input else admin_password_env
    
    print()
    print(f"📧 Email: {admin_email}")
    print(f"🔑 Senha: {'*' * len(admin_password)}")
    print()
    
    # Confirmar criação
    print("Deseja criar este usuário? (s/n): ", end='')
    confirm = input().strip().lower()
    
    if confirm != 's':
        print("❌ Operação cancelada.")
        return False
    
    print()
    print("🔄 Criando usuário...")
    
    # Criar usuário usando o serviço
    auth_service = AuthService()
    success, error_message, user_id = auth_service.create_user(admin_email, admin_password)
    
    if success:
        print()
        print("=" * 70)
        print("✅ USUÁRIO CRIADO COM SUCESSO!")
        print("=" * 70)
        print(f"   ID: {user_id}")
        print(f"   Email: {admin_email}")
        print()
        print("💡 Você já pode fazer login no sistema com estas credenciais.")
        print("=" * 70)
        return True
    else:
        print()
        print("=" * 70)
        print("❌ ERRO AO CRIAR USUÁRIO")
        print("=" * 70)
        print(f"   {error_message}")
        print()
        print("💡 Possíveis causas:")
        print("   - Email já cadastrado no banco de dados")
        print("   - Erro de conexão com o banco de dados")
        print("   - Senha muito curta (mínimo 6 caracteres)")
        print("=" * 70)
        return False


def main():
    """Função principal"""
    try:
        success = create_admin_user()
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
