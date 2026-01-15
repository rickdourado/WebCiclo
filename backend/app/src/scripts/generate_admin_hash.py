#!/usr/bin/env python3
# scripts/generate_admin_hash.py
"""
Script para gerar hash bcrypt da senha do administrador.
Use este script para gerar um hash seguro da senha admin para o arquivo .env
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.auth_service import AuthService

def main():
    """Gera hash da senha do admin"""
    print("🔐 Gerador de Hash para Senha do Admin")
    print("=" * 50)
    
    # Solicitar senha
    password = input("Digite a nova senha do admin: ").strip()
    
    if not password:
        print("❌ Senha não pode estar vazia!")
        return
    
    if len(password) < 6:
        print("❌ Senha deve ter pelo menos 6 caracteres!")
        return
    
    # Confirmar senha
    confirm_password = input("Confirme a senha: ").strip()
    
    if password != confirm_password:
        print("❌ Senhas não coincidem!")
        return
    
    # Gerar hash
    auth_service = AuthService()
    hashed = auth_service.hash_password(password)
    
    print("\n✅ Hash gerado com sucesso!")
    print("=" * 50)
    print(f"ADMIN_PASSWORD={hashed}")
    print("=" * 50)
    print("\n📝 Instruções:")
    print("1. Copie o hash acima")
    print("2. Substitua o valor de ADMIN_PASSWORD no arquivo .env")
    print("3. Reinicie a aplicação")
    print("\n⚠️  IMPORTANTE: Mantenha este hash seguro e nunca o compartilhe!")

if __name__ == "__main__":
    main()