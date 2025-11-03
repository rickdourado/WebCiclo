# 🎓 WebCiclo Carioca - Sistema de Gestão de Cursos

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-Prefeitura%20RJ-orange.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-CSRF%20%2B%20bcrypt-red.svg)](#segurança)

Sistema de curadoria e gestão de cursos desenvolvido para a **Prefeitura do Rio de Janeiro**. Permite criar, gerenciar e publicar informações sobre cursos de capacitação oferecidos pelos órgãos municipais.

## 🚀 Funcionalidades Principais

### 📝 Gestão de Cursos
- ✅ **Criação de cursos** com formulário completo e validação
- ✅ **Edição e duplicação** de cursos existentes
- ✅ **Múltiplas modalidades**: Presencial, Online e Híbrido
- ✅ **Múltiplas unidades** para cursos presenciais
- ✅ **Upload de imagens** (capas e logos de parceiros)
- ✅ **Geração automática** de arquivos CSV e PDF

### 🤖 Inteligência Artificial
- ✅ **Integração com Google Gemini AI** para melhorar descrições
- ✅ **Processamento automático** de conteúdo
- ✅ **Fallback gracioso** quando IA não está disponível

### 🔐 Segurança Avançada
- ✅ **Proteção CSRF** em todos os formulários
- ✅ **Hash bcrypt** para senhas administrativas
- ✅ **Headers de segurança** (XSS, Clickjacking, CSP)
- ✅ **Validação robusta** de entrada de dados
- ✅ **Autenticação administrativa** segura

### 🎨 Interface Moderna
- ✅ **Design responsivo** mobile-first
- ✅ **Ícones Font Awesome** com sistema de fallback
- ✅ **Animações suaves** e feedback visual
- ✅ **Tema glassmorphism** com gradientes
- ✅ **Acessibilidade** (ARIA labels, alt texts)

## 🏗️ Arquitetura do Sistema

### Frontend
- **HTML5** - Estrutura semântica e acessível
- **CSS3** - Design moderno com Grid e Flexbox
- **JavaScript Vanilla** - Interações sem dependências externas
- **Jinja2** - Templates dinâmicos do Flask

### Backend
- **Flask 2.3.3** - Framework web principal
- **Python 3.13** - Linguagem de programação
- **Flask-WTF** - Proteção CSRF e validação de formulários
- **bcrypt** - Hash seguro de senhas

### Armazenamento
- **CSV** - Dados estruturados dos cursos
- **PDF** - Relatórios formatados para impressão
- **JSON** - Configurações e metadados
- **Arquivos** - Imagens e documentos

## 📁 Estrutura do Projeto

```
WebCiclo/
├── 📄 app.py                     # Aplicação Flask principal
├── ⚙️ config.py                  # Configurações centralizadas
├── 📋 forms.py                   # Formulários WTF com CSRF
├── 📦 requirements.txt           # Dependências Python
├── 🔧 flask_app.py              # WSGI para PythonAnywhere
├── 📊 CSV/                      # Arquivos CSV gerados
├── 📄 PDF/                      # Relatórios PDF gerados
├── 🛠️ services/                 # Camada de serviços
│   ├── course_service.py        # Lógica de negócio dos cursos
│   ├── auth_service.py          # Autenticação e segurança
│   ├── ai_service.py            # Integração com Gemini AI
│   ├── validation_service.py    # Validações de dados
│   └── file_service.py          # Manipulação de arquivos
├── 🗄️ repositories/             # Camada de dados
│   └── course_repository.py     # Persistência dos cursos
├── 🔧 scripts/                  # Scripts utilitários
│   ├── csv_generator.py         # Geração de CSV
│   ├── pdf_generator.py         # Geração de PDF
│   ├── generate_admin_hash.py   # Gerador de hash de senhas
│   ├── test_security.py         # Testes de segurança
│   └── diagnose_icons.py        # Diagnóstico de ícones
├── 🎨 static/                   # Arquivos estáticos
│   ├── css/                     # Estilos CSS
│   ├── js/                      # Scripts JavaScript
│   └── images/                  # Imagens e uploads
├── 📄 templates/                # Templates HTML
│   ├── index.html               # Formulário de criação
│   ├── course_list.html         # Lista administrativa
│   ├── course_list_public.html  # Lista pública
│   ├── course_edit.html         # Edição de cursos
│   └── admin_login.html         # Login administrativo
└── 📚 documentacao/             # Documentação completa
    ├── logs/                    # Changelog diário
    ├── seguranca_implementada.md # Documentação de segurança
    └── solucao_icones.md        # Solução para ícones
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.13+
- pip (gerenciador de pacotes Python)
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/prefeitura-rio/webciclo-carioca.git
cd webciclo-carioca
```

### 2. Crie um Ambiente Virtual
```bash
# Usando conda (recomendado)
conda create -n ciclo python=3.13
conda activate ciclo

# Ou usando venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

### 5. Configure a Segurança
```bash
# Gere um hash seguro para a senha admin
python scripts/generate_admin_hash.py

# Execute a configuração automática de segurança
python scripts/setup_security.py
```

### 6. Execute o Sistema
```bash
python app.py
```

Acesse: `http://localhost:5000`

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# Autenticação Administrativa
ADMIN_USERNAME=admin
ADMIN_PASSWORD=$2b$12$...  # Hash bcrypt gerado

# Segurança Flask
SECRET_KEY=sua_chave_secreta_forte
WTF_CSRF_SECRET_KEY=chave_csrf_especifica

# API do Google Gemini (opcional)
GEMINI_API_KEY=sua_chave_api_gemini

# Integração Notion (opcional)
NOTION_TOKEN=seu_token_notion
NOTION_DATABASE_ID_CURSOS=id_database_cursos
```

### Configurações de Produção

Para deploy no **PythonAnywhere**:

1. Configure as variáveis de ambiente no painel
2. Use o arquivo `flask_app.py` como WSGI
3. Configure os diretórios de upload
4. Ative HTTPS para máxima segurança

## 🔐 Segurança

### Proteções Implementadas

- **🛡️ CSRF Protection**: Tokens únicos em todos os formulários
- **🔒 Hash bcrypt**: Senhas com salt e 12 rounds
- **🚫 XSS Protection**: Headers de segurança configurados
- **🔐 Content Security Policy**: Controle de recursos carregados
- **✅ Validação Robusta**: Sanitização de todas as entradas
- **📝 Logs de Segurança**: Monitoramento de tentativas suspeitas

### Testes de Segurança

```bash
# Teste completo de segurança
python scripts/test_security.py

# Diagnóstico de problemas
python scripts/diagnose_icons.py
```

## 🎯 Uso do Sistema

### Área Pública
- **Visualização de cursos**: Lista todos os cursos disponíveis
- **Duplicação de cursos**: Permite duplicar cursos existentes
- **Filtros e busca**: Encontre cursos por categoria ou texto

### Área Administrativa
- **Login seguro**: `/admin/login`
- **CRUD completo**: Criar, editar, excluir cursos
- **Gestão de status**: Marcar cursos como inseridos
- **Downloads**: CSV e PDF dos cursos
- **Dashboard**: Estatísticas e visão geral

### Modalidades de Curso

#### 🏢 Presencial
- Múltiplas unidades/turmas
- Endereços e bairros específicos
- Horários e dias da semana
- Vagas por unidade

#### 💻 Online
- Plataforma digital (Zoom, Teams, etc.)
- Aulas síncronas ou assíncronas
- Links de acesso
- Recursos digitais

#### 🔄 Híbrido
- Combinação de presencial e online
- Flexibilidade de horários
- Múltiplas modalidades

## 🤖 Integração com IA

### Google Gemini AI
- **Melhoria automática** de descrições de cursos
- **Processamento inteligente** de conteúdo
- **Fallback gracioso** quando indisponível
- **Rate limiting** para evitar abuse

### Configuração da IA
```python
# config.py
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-2.5-pro'  # Modelo estável
```

## 📊 Relatórios e Exportação

### Formatos Disponíveis
- **📄 CSV**: Dados estruturados para importação
- **📋 PDF**: Documento formatado para impressão
- **📊 JSON**: Dados para integração com APIs

### Campos Exportados
- Informações básicas do curso
- Modalidade e horários
- Dados de inscrição
- Informações de acessibilidade
- Parceiros e certificações

## 🛠️ Scripts Utilitários

### Segurança
```bash
python scripts/generate_admin_hash.py    # Gerar hash de senha
python scripts/test_security.py          # Testar segurança
python scripts/setup_security.py         # Configuração automática
```

### Diagnóstico
```bash
python scripts/diagnose_icons.py         # Verificar ícones
python scripts/add_icon_fallback.py      # Adicionar fallback
```

### Dados
```bash
python scripts/csv_generator.py          # Gerar CSV
python scripts/pdf_generator.py          # Gerar PDF
python scripts/csv_reader.py             # Ler dados CSV
```

## 🧪 Testes

### Testes Automatizados
```bash
# Teste de segurança completo
python scripts/test_security.py

# Diagnóstico de ícones
python scripts/diagnose_icons.py

# Validação de configurações
python -c "from config import Config; Config.validate_required_config()"
```

### Testes Manuais
1. **Criação de curso**: Teste todos os campos e validações
2. **Upload de arquivos**: Verifique imagens e documentos
3. **Modalidades**: Teste presencial, online e híbrido
4. **Segurança**: Tente acessar áreas protegidas
5. **Responsividade**: Teste em diferentes dispositivos

## 📈 Performance

### Otimizações Implementadas
- **Lazy loading** para listas grandes
- **Compressão automática** de imagens
- **Cache de dados** quando apropriado
- **Minimização** de requisições desnecessárias

### Monitoramento
- Logs detalhados de performance
- Métricas de tempo de resposta
- Monitoramento de uso de recursos

## 🤝 Contribuição

### Padrões de Código
- **Type hints** sempre que possível
- **Docstrings** no formato Google Style
- **Tratamento de exceções** com logs detalhados
- **Separação clara** entre camadas (Service → Repository → Scripts)

### Convenções
- **Variáveis**: `snake_case`
- **Funções**: `snake_case` com verbos
- **Classes**: `PascalCase`
- **Arquivos**: `snake_case`
- **Templates**: `snake_case`

### Processo de Desenvolvimento
1. Crie uma branch para sua feature
2. Implemente seguindo os padrões
3. Adicione testes quando necessário
4. Atualize a documentação
5. Faça commit com mensagem descritiva
6. Abra um Pull Request

## 📚 Documentação

### Documentos Disponíveis
- `documentacao/seguranca_implementada.md` - Segurança detalhada
- `documentacao/solucao_icones.md` - Solução para ícones
- `documentacao/logs/` - Changelog diário
- `documentacao/relatorio_projeto_webciclo.md` - Relatório completo

### Logs e Changelog
- Logs diários em `documentacao/logs/AAAA-MM-DD.md`
- Versionamento semântico
- Registro detalhado de mudanças

## 🚀 Deploy

### PythonAnywhere (Produção)
1. Upload dos arquivos via Git ou interface web
2. Configuração das variáveis de ambiente
3. Configuração do WSGI com `flask_app.py`
4. Configuração de domínio personalizado
5. Ativação de HTTPS

### Outros Provedores
- **Heroku**: Use `Procfile` e configure buildpacks
- **DigitalOcean**: Deploy via Docker ou servidor tradicional
- **AWS**: Use Elastic Beanstalk ou EC2
- **Google Cloud**: App Engine ou Compute Engine

## 📞 Suporte

### Contato
- **Prefeitura do Rio de Janeiro**
- **Secretaria Municipal de Educação**
- **Equipe de Desenvolvimento**: WebCiclo Team

### Problemas Conhecidos
- Consulte `documentacao/logs/` para problemas recentes
- Verifique issues no repositório
- Execute scripts de diagnóstico

### FAQ
**P: Os ícones não aparecem?**
R: Execute `python scripts/diagnose_icons.py` para diagnóstico

**P: Erro de CSRF?**
R: Verifique se os tokens estão sendo incluídos nos formulários

**P: Problema com upload de imagens?**
R: Verifique permissões de diretório e tamanho dos arquivos

## 📄 Licença

Este projeto é desenvolvido para a **Prefeitura do Rio de Janeiro** e está sujeito às políticas de software da administração municipal.

## 🎉 Agradecimentos

- **Prefeitura do Rio de Janeiro** - Patrocinador do projeto
- **Equipe de Desenvolvimento** - Implementação e manutenção
- **Comunidade Flask** - Framework e bibliotecas
- **Google** - API Gemini AI
- **Font Awesome** - Ícones da interface

---

**WebCiclo Carioca v4** - Sistema de Gestão de Cursos  
Desenvolvido com ❤️ para a Prefeitura do Rio de Janeiro  
© 2025 - Todos os direitos reservados