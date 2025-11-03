# 🐍 Configuração do Ambiente 'ciclo' - WebCiclo Carioca

Este documento explica como configurar e usar o ambiente conda 'ciclo' como padrão para o projeto WebCiclo Carioca.

## 🚀 Configuração Manual

Para configurar o ambiente 'ciclo':

```bash
# Criar ambiente se não existir
conda create -n ciclo python=3.13 -y

# Ativar ambiente
conda activate ciclo

# Instalar dependências
pip install -r requirements.txt
```

Configurações automáticas:
- ✅ VS Code detecta automaticamente via .vscode/settings.json
- ✅ Kiro IDE configurado via .kiro/settings/python.json
- ✅ direnv ativa automaticamente via .envrc
- ✅ pyenv detecta via .python-version

## 🔧 Métodos de Ativação

### 1. Ativação Manual
```bash
conda activate ciclo
```

### 2. Usando direnv (Automático)
```bash
# Se direnv estiver instalado e configurado
cd /caminho/para/WebCiclo  # Ativa automaticamente
```

### 3. Ativação Automática no Terminal
Adicione ao seu `~/.bashrc` ou `~/.zshrc`:
```bash
# Auto-ativar ambiente 'ciclo' no diretório WebCiclo
if [[ "$PWD" == *"WebCiclo"* ]]; then
    conda activate ciclo 2>/dev/null || true
fi
```

### 4. Usando direnv (Opcional)
Se você tem o `direnv` instalado:
```bash
# Instalar direnv (Ubuntu/Debian)
sudo apt install direnv

# Adicionar ao shell
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

# Permitir no projeto
direnv allow
```

## 🎯 IDEs e Editores

### VS Code
As configurações foram automaticamente criadas em `.vscode/settings.json`:
- Interpretador Python: `~/miniconda3/envs/ciclo/bin/python`
- Ativação automática do ambiente
- Configuração do terminal integrado

### Kiro IDE
Configurações criadas em `.kiro/settings/python.json`:
- Ambiente padrão: `ciclo`
- Ativação automática habilitada

### PyCharm
1. Abra o projeto no PyCharm
2. Vá em `File > Settings > Project > Python Interpreter`
3. Clique em `Add Interpreter > Conda Environment`
4. Selecione `Existing environment`
5. Escolha: `~/miniconda3/envs/ciclo/bin/python`

## 📁 Arquivos de Configuração Criados

| Arquivo | Propósito |
|---------|-----------|
| `.python-version` | Especifica versão/ambiente Python |
| `.envrc` | Configuração para direnv |
| `environment.yml` | Definição completa do ambiente conda |
| `.vscode/settings.json` | Configurações do VS Code |
| `.kiro/settings/python.json` | Configurações do Kiro IDE |

## 🔍 Verificação

### Verificar Ambiente Ativo
```bash
# Mostrar ambiente atual
echo $CONDA_DEFAULT_ENV

# Listar todos os ambientes
conda env list

# Verificar interpretador Python
which python
python --version
```

### Verificar Dependências
```bash
# Listar pacotes instalados
conda list

# Verificar pacotes específicos do projeto
pip list | grep -E "(Flask|bcrypt|reportlab)"
```

## 🛠️ Comandos Úteis

### Recriar Ambiente
```bash
# Remover ambiente existente
conda env remove -n ciclo

# Recriar do environment.yml
conda env create -f environment.yml

# Ou recriar básico
conda create -n ciclo python=3.13 -y
conda activate ciclo
pip install -r requirements.txt
```

### Atualizar Dependências
```bash
conda activate ciclo
pip install -r requirements.txt --upgrade
```

### Exportar Ambiente
```bash
# Exportar environment.yml atualizado
conda env export -n ciclo > environment.yml

# Exportar requirements.txt atualizado
pip freeze > requirements.txt
```

## 🚨 Solução de Problemas

### Problema: Conda não encontrado
```bash
# Verificar instalação
which conda

# Adicionar ao PATH (se necessário)
export PATH="~/miniconda3/bin:$PATH"
echo 'export PATH="~/miniconda3/bin:$PATH"' >> ~/.bashrc
```

### Problema: Ambiente não ativa automaticamente
```bash
# Verificar configuração do conda
conda config --show

# Habilitar auto-ativação
conda config --set auto_activate_base false
conda config --set changeps1 true
```

### Problema: Dependências não instalam
```bash
# Limpar cache do pip
pip cache purge

# Instalar com verbose
pip install -r requirements.txt -v

# Usar conda para pacotes problemáticos
conda install -n ciclo package_name
```

## 📚 Recursos Adicionais

- [Documentação do Conda](https://docs.conda.io/)
- [Guia de Ambientes Virtuais](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Configuração do VS Code com Python](https://code.visualstudio.com/docs/python/environments)

## 🎯 Próximos Passos

Após configurar o ambiente:

1. **Ativar o ambiente**: `conda activate ciclo` (ou automático via IDE/direnv)
2. **Executar o projeto**: `python app.py`
3. **Acessar**: `http://localhost:5000`
4. **Desenvolver**: O ambiente estará sempre pronto!

---

**Configuração realizada em**: 11/03/2025  
**Ambiente**: ciclo (Python 3.13)  
**Projeto**: WebCiclo Carioca v4