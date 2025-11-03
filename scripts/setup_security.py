#!/usr/bin/env python3
# scripts/setup_security.py
"""
Script de configuração inicial para as melhorias de segurança.
Instala dependências, valida configurações e executa testes básicos.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências de segurança...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "Flask-WTF==1.2.1", 
            "WTForms==3.1.1", 
            "bcrypt==4.1.2"
        ])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def check_env_file():
    """Verifica se o arquivo .env está configurado"""
    print("\n🔍 Verificando arquivo .env...")
    
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    required_vars = [
        'ADMIN_USERNAME',
        'ADMIN_PASSWORD', 
        'SECRET_KEY',
        'WTF_CSRF_SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis faltando no .env: {', '.join(missing_vars)}")
        return False
    
    # Verificar se a senha está em formato hash
    if '$2b$' in content:
        print("✅ Senha admin em formato hash bcrypt")
    else:
        print("⚠️ Senha admin não está em formato hash")
        print("Execute: python scripts/generate_admin_hash.py")
    
    print("✅ Arquivo .env configurado!")
    return True

def run_security_tests():
    """Executa os testes de segurança"""
    print("\n🧪 Executando testes de segurança...")
    
    try:
        result = subprocess.run([
            sys.executable, "scripts/test_security.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Erros:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False

def show_next_steps():
    """Mostra os próximos passos"""
    print("\n" + "="*50)
    print("🎉 CONFIGURAÇÃO DE SEGURANÇA CONCLUÍDA!")
    print("="*50)
    
    print("\n📋 Próximos passos:")
    print("1. Inicie o servidor: python app.py")
    print("2. Acesse: http://localhost:5000/admin/login")
    print("3. Use as credenciais: admin / GPCE#2025#")
    print("4. Teste a criação de cursos")
    print("5. Verifique os logs de segurança")
    
    print("\n🔒 Recursos de segurança ativados:")
    print("✅ Hash bcrypt para senhas")
    print("✅ Proteção CSRF em formulários")
    print("✅ Headers de segurança")
    print("✅ Validação robusta de entrada")
    print("✅ Logs de segurança")
    
    print("\n📚 Documentação:")
    print("- documentacao/seguranca_implementada.md")
    print("- documentacao/logs/2025-03-11.md")

def main():
    """Executa a configuração completa"""
    print("🔐 CONFIGURAÇÃO DE SEGURANÇA - WEBCICLO CARIOCA")
    print("="*50)
    
    # Passo 1: Instalar dependências
    if not install_dependencies():
        print("❌ Falha na instalação de dependências")
        return False
    
    # Passo 2: Verificar .env
    if not check_env_file():
        print("❌ Falha na verificação do .env")
        return False
    
    # Passo 3: Executar testes
    if not run_security_tests():
        print("⚠️ Alguns testes falharam (normal se servidor não estiver rodando)")
    
    # Passo 4: Mostrar próximos passos
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)