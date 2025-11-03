#!/usr/bin/env python3
# scripts/test_security.py
"""
Script para testar as implementações de segurança do WebCiclo.
Testa CSRF protection, hash de senhas e headers de segurança.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from services.auth_service import AuthService
from config import Config

def test_password_hashing():
    """Testa o sistema de hash de senhas"""
    print("🔐 Testando sistema de hash de senhas...")
    
    auth_service = AuthService()
    
    # Teste 1: Gerar hash
    password = "teste123"
    hashed = auth_service.hash_password(password)
    print(f"✅ Hash gerado: {hashed[:20]}...")
    
    # Teste 2: Verificar senha correta
    if auth_service.verify_password(password, hashed):
        print("✅ Verificação de senha correta: OK")
    else:
        print("❌ Verificação de senha correta: FALHOU")
    
    # Teste 3: Verificar senha incorreta
    if not auth_service.verify_password("senha_errada", hashed):
        print("✅ Rejeição de senha incorreta: OK")
    else:
        print("❌ Rejeição de senha incorreta: FALHOU")
    
    # Teste 4: Autenticação admin
    success, error = auth_service.authenticate_admin("admin", "GPCE#2025#")
    if success:
        print("✅ Autenticação admin: OK")
    else:
        print(f"❌ Autenticação admin: FALHOU - {error}")

def test_csrf_protection():
    """Testa a proteção CSRF (requer servidor rodando)"""
    print("\n🛡️ Testando proteção CSRF...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Teste 1: Acessar página de login
        response = requests.get(f"{base_url}/admin/login")
        if response.status_code == 200:
            print("✅ Página de login acessível")
            
            # Verificar se há token CSRF na página
            if 'csrf_token' in response.text:
                print("✅ Token CSRF presente na página")
            else:
                print("⚠️ Token CSRF não encontrado na página")
        else:
            print(f"❌ Erro ao acessar página de login: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("⚠️ Servidor não está rodando. Inicie com 'python app.py' para testar CSRF")

def test_security_headers():
    """Testa os headers de segurança (requer servidor rodando)"""
    print("\n🔒 Testando headers de segurança...")
    
    base_url = "http://localhost:5000"
    
    try:
        response = requests.get(base_url)
        
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options', 
            'X-XSS-Protection',
            'Content-Security-Policy',
            'Referrer-Policy'
        ]
        
        for header in security_headers:
            if header in response.headers:
                print(f"✅ {header}: {response.headers[header]}")
            else:
                print(f"❌ {header}: Não encontrado")
                
    except requests.exceptions.ConnectionError:
        print("⚠️ Servidor não está rodando. Inicie com 'python app.py' para testar headers")

def test_config_validation():
    """Testa a validação de configurações"""
    print("\n⚙️ Testando validação de configurações...")
    
    try:
        Config.validate_required_config()
        print("✅ Configurações obrigatórias: OK")
    except ValueError as e:
        print(f"❌ Configurações obrigatórias: {e}")

def main():
    """Executa todos os testes de segurança"""
    print("🔍 TESTE DE SEGURANÇA - WEBCICLO CARIOCA")
    print("=" * 50)
    
    test_config_validation()
    test_password_hashing()
    test_csrf_protection()
    test_security_headers()
    
    print("\n" + "=" * 50)
    print("✅ Testes de segurança concluídos!")
    print("\n📝 Próximos passos:")
    print("1. Inicie o servidor: python app.py")
    print("2. Execute novamente para testar CSRF e headers")
    print("3. Teste o login com as novas credenciais")

if __name__ == "__main__":
    main()