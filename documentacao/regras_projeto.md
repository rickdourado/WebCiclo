# Regras do Projeto CadastroCurso

## Visão Geral

O CadastroCurso é um sistema de curadoria de cursos desenvolvido com Flask para frontend e backend, utilizando HTML5, CSS3 e JavaScript Vanilla para a interface. O sistema é projetado para ser hospedado na plataforma CicloCarioca.pythonanywhere.com.

## Arquitetura do Sistema

A estrutura do sistema se divide em três partes principais:

- **Frontend (HTML5 + CSS3 + JS Vanilla):** Interface do usuário renderizada por Flask, com páginas HTML5 semânticas, estilização CSS3 responsiva e interações básicas em JavaScript puro.
- **Backend (Python/Flask):** Controla a lógica de negócio, processamento de dados, renderização de templates e gerenciamento de arquivos.
- **Armazenamento de Dados:** Utiliza arquivos CSV e PDF para armazenar informações dos cursos, em vez de um banco de dados tradicional.

## Estrutura de Arquivos do Projeto

```
CadastroCurso/
├── app.py                    # Aplicação Flask principal
├── flask_app.py              # Arquivo WSGI para CicloCarioca.pythonanywhere.com
├── requirements.txt          # Dependências Python
├── last_id.json              # Armazena o último ID utilizado
├── README_PYTHONANYWHERE.md  # Instruções para deploy
├── CSV/                      # Diretório para armazenar arquivos CSV
├── PDF/                      # Diretório para armazenar arquivos PDF
├── documentacao/             # Documentação do projeto
│   └── logs/                 # Logs de alterações
├── scripts/                  # Scripts auxiliares
│   ├── __init__.py
│   ├── csv_generator.py      # Gerador de arquivos CSV
│   ├── csv_reader.py         # Leitor de arquivos CSV
│   ├── id_manager.py         # Gerenciador de IDs
│   └── pdf_generator.py      # Gerador de arquivos PDF
├── static/                   # Arquivos estáticos
│   ├── css/
│   │   └── style.css        # Estilos CSS
│   └── js/
│       └── script.js         # Scripts JavaScript
└── templates/                # Templates HTML
    ├── index.html           # Página inicial com formulário de criação de curso
    ├── course_list.html      # Lista de cursos
    └── course_success.html   # Página de sucesso após criação
```

## Tecnologias Utilizadas

### Frontend
- **HTML5:** Estrutura semântica das páginas web
- **CSS3:** Estilização responsiva com flexbox/grid
- **JavaScript Vanilla:** Interações básicas e validações de formulário
- **Jinja2:** Sistema de templates do Flask para renderização dinâmica

### Backend
- **Flask:** Framework web para renderização de templates e rotas
- **ReportLab:** Biblioteca para geração de arquivos PDF
- **CSV:** Módulo para manipulação de arquivos CSV

## Regras de Desenvolvimento

- **Linguagem:** Toda documentação e comentários em português brasileiro
- **Controle de Versão:** Verificar a data do sistema ao registrar mudanças
- **Documentação:** Manter arquivos .md de documentação na pasta `documentacao`
- **Changelog:** Registrar alterações diárias em arquivos com formato `AAAA-MM-DD.md` na pasta `documentacao/logs`
- **Padrões:** Utilizar HTML5 semântico, CSS modular e JavaScript ES6+ compatível
- **Acessibilidade:** Garantir que as páginas sejam acessíveis e responsivas
- **Segurança:** Implementar validação de dados e proteção contra ataques comuns

## Fluxo de Trabalho

1. Usuário acessa o formulário de criação de curso
2. Preenche os dados do curso e submete o formulário
3. Sistema gera arquivos CSV e PDF com os dados do curso
4. Usuário é redirecionado para página de sucesso com links para os arquivos
5. Usuário pode visualizar a lista de todos os cursos criados

## Observações Importantes

- O sistema utiliza arquivos CSV e PDF para armazenamento de dados em vez de um banco de dados tradicional
- A estrutura do projeto está otimizada para funcionar no ambiente CicloCarioca.pythonanywhere.com
- O sistema utiliza Flask para servir tanto o backend quanto o frontend
- Não são utilizados frameworks JavaScript como React ou bibliotecas como jQuery