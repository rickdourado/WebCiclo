#!/usr/bin/env python3
# scripts/setup_environment.py
"""
Script para configurar automaticamente o ambiente 'ciclo' como padrão
para o projeto WebCiclo Carioca.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_conda():
    """Verifica se conda está disponível"""
    try:
        result = subprocess.run(['conda', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Conda encontrado: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Conda não encontrado. Instale Anaconda/Miniconda primeiro.")
    return False

def check_environment():
    """Verifica se o ambiente 'ciclo' existe"""
    try:
        result = subprocess.run(['conda', 'env', 'list'], 
                              capture_output=True, text=True)
        if 'ciclo' in result.stdout:
            print("✅ Ambiente 'ciclo' encontrado")
            return True
        else:
            print("⚠️ Ambiente 'ciclo' não encontrado")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar ambientes: {e}")
        return False

def create_environment():
    """Cria o ambiente 'ciclo' se não existir"""
    print("📝 Criando ambiente 'ciclo'...")
    
    # Verificar se existe environment.yml
    if Path("environment.yml").exists():
        print("📄 Usando environment.yml...")
        cmd = ['conda', 'env', 'create', '-f', 'environment.yml']
    else:
        print("📄 Criando ambiente básico...")
        cmd = ['conda', 'create', '-n', 'ciclo', 'python=3.13', '-y']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ambiente 'ciclo' criado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao criar ambiente: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False

def install_dependencies():
    """Instala dependências no ambiente 'ciclo'"""
    print("📦 Instalando dependências...")
    
    if not Path("requirements.txt").exists():
        print("⚠️ requirements.txt não encontrado")
        return True
    
    try:
        # Ativar ambiente e instalar dependências
        cmd = [
            'conda', 'run', '-n', 'ciclo', 
            'pip', 'install', '-r', 'requirements.txt'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso!")
            return True
        else:
            print(f"❌ Erro ao instalar dependências: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_activation_script():
    """Cria script de ativação para diferentes shells"""
    
    # Script para bash/zsh
    bash_script = """#!/bin/bash
# Ativação automática do ambiente 'ciclo' para WebCiclo
if command -v conda &> /dev/null; then
    conda activate ciclo
    echo "✅ Ambiente 'ciclo' ativado para WebCiclo"
else
    echo "❌ Conda não encontrado"
fi
"""
    
    with open("activate_ciclo.sh", "w") as f:
        f.write(bash_script)
    
    os.chmod("activate_ciclo.sh", 0o755)
    print("✅ Script de ativação criado: activate_ciclo.sh")

def update_vscode_settings():
    """Atualiza configurações do VS Code"""
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    settings_file = vscode_dir / "settings.json"
    
    # Detectar caminho do conda
    try:
        result = subprocess.run(['which', 'conda'], capture_output=True, text=True)
        conda_path = result.stdout.strip()
        if conda_path:
            conda_base = str(Path(conda_path).parent.parent)
        else:
            conda_base = "~/miniconda3"
    except:
        conda_base = "~/miniconda3"
    
    settings = {
        "python.defaultInterpreterPath": f"{conda_base}/envs/ciclo/bin/python",
        "python.terminal.activateEnvironment": True,
        "python.terminal.activateEnvInCurrentTerminal": True,
        "python.condaPath": f"{conda_base}/bin/conda",
        "python.envFile": "${workspaceFolder}/.env",
        "terminal.integrated.env.linux": {
            "CONDA_DEFAULT_ENV": "ciclo"
        }
    }
    
    # Ler configurações existentes se houver
    if settings_file.exists():
        import json
        try:
            with open(settings_file, 'r') as f:
                existing_settings = json.load(f)
            existing_settings.update(settings)
            settings = existing_settings
        except:
            pass
    
    # Salvar configurações
    import json
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=4)
    
    print("✅ Configurações do VS Code atualizadas")

def create_project_files():
    """Cria arquivos de configuração do projeto"""
    
    # .python-version
    with open(".python-version", "w") as f:
        f.write("ciclo\n")
    print("✅ Arquivo .python-version criado")
    
    # .envrc para direnv (opcional)
    envrc_content = """# Ativação automática com direnv
layout anaconda ciclo
"""
    with open(".envrc", "w") as f:
        f.write(envrc_content)
    print("✅ Arquivo .envrc criado (para direnv)")

def show_instructions():
    """Mostra instruções finais"""
    print("\n" + "="*60)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA!")
    print("="*60)
    
    print("\n📋 Como usar o ambiente 'ciclo':")
    print("1. Ativação manual:")
    print("   conda activate ciclo")
    
    print("\n2. Script de ativação:")
    print("   source activate_ciclo.sh")
    
    print("\n3. VS Code:")
    print("   - Abra o projeto no VS Code")
    print("   - O ambiente será ativado automaticamente")
    
    print("\n4. Verificar ambiente ativo:")
    print("   conda info --envs")
    print("   echo $CONDA_DEFAULT_ENV")
    
    print("\n🚀 Para executar o projeto:")
    print("   python app.py")
    
    print("\n📚 Arquivos criados:")
    print("   - .python-version")
    print("   - .envrc (para direnv)")
    print("   - activate_ciclo.sh")
    print("   - .vscode/settings.json (atualizado)")
    print("   - environment.yml")

def main():
    """Executa a configuração completa"""
    print("🔧 CONFIGURAÇÃO DO AMBIENTE 'CICLO' - WEBCICLO CARIOCA")
    print("="*60)
    
    # Verificar conda
    if not check_conda():
        return False
    
    # Verificar/criar ambiente
    if not check_environment():
        if not create_environment():
            return False
    
    # Instalar dependências
    if not install_dependencies():
        print("⚠️ Continuando mesmo com erro nas dependências...")
    
    # Criar arquivos de configuração
    create_activation_script()
    update_vscode_settings()
    create_project_files()
    
    # Mostrar instruções
    show_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)