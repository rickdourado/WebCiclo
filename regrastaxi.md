---
trigger: always_on
---

## 🎯 VISÃO GERAL DO PROJETO

### Objetivo

Sistema para gerenciamento e análise de solicitações de serviços de táxi do município do Rio de Janeiro, com foco em:

- Cadastro de usuários autorizados
- Validação de conformidade com regras estabelecidas
- API REST para integração com frontend

---

# Regras Backend - Sistema TaxiRio

## 🎯 VISÃO GERAL

Sistema de cadastro de usuários com **FastAPI + SQLAlchemy + Alembic + MariaDB**.

**Stack Tecnológico:**

- Backend: FastAPI (Python 3.13+)
- Banco de Dados: MariaDB 12.1.2
- ORM: SQLAlchemy 2.0
- Migrations: Alembic 1.13
- Validação: Pydantic 2.5
- Gerenciador de Pacotes: uv

---

## 📋 MODELAGEM DE DADOS

### Tabela: usuarios

- `id`: INTEGER, PRIMARY KEY
- `nome`: VARCHAR(200), NOT NULL
- `cpf`: VARCHAR(14), UNIQUE, INDEX
- `matricula`: VARCHAR(50), UNIQUE, INDEX
- `orgao`: VARCHAR(200), NOT NULL
- `email`: VARCHAR(200), NOT NULL
- `celular`: VARCHAR(20)
- `chefe_imediato`: VARCHAR(200)
- `ativo`: BOOLEAN, DEFAULT TRUE

### Tabela: chefia

- `id`: INTEGER, PRIMARY KEY
- `orgao`: VARCHAR(200), UNIQUE, INDEX
- `criado_em`: DATETIME
- `atualizado_em`: DATETIME

---

## 🗂️ ESTRUTURA DE ARQUIVOS

```
taxirio/
├── backend/
│   ├── app/
│   │   ├── main.py           # Ponto de entrada FastAPI
│   │   ├── routes.py         # Definição de rotas da API
│   │   ├── schemas.py        # Validação de dados (Pydantic)
│   │   └── src/
│   │       ├── models/       # Modelos do Banco de Dados (usuarios.py, chefia.py)
│   │       └── scripts/      # Scripts (import_usuarios.py, ativar_usuarios.py)
│   ├── alembic/              # Configurações de Migração
│   └── logs/                 # Logs de execução (backend.log, frontend.log)
├── documentacao/             # Documentação Centralizada
│   ├── changelogs/           # Logs diários de mudanças (AAAA-MM-DD.md)
│   ├── design-mockups/       # Mockups e especificações Figma
│   └── refs/                 # Arquivos CSV e referências de dados
├── web/
│   ├── templates/            # Páginas HTML (index, show_users, view_user)
│   └── static/
│       ├── css/              # Estilos (style.css)
│       └── js/               # Lógica (script.js, users.js, view_user.js)
└── start.sh                  # Script de inicialização do sistema
```

---

## 🚀 COMANDOS E FLUXOS

1. **Ativação Obrigatória:** Sempre executar `source .venv/bin/activate` em cada novo terminal aberto.
2. **Migrações:** `alembic revision --autogenerate -m "msg"` e `alembic upgrade head`
3. **Carga de Dados:** `python backend/app/src/scripts/import_chefia.py` (ou `import_usuarios.py`)
4. **Iniciar Servidores:** `./start.sh`
5. **Endpoint Órgãos:** `GET /api/chefia` (Usado para o dropdown no frontend)
6. **SEMPRE** unifique os changelogs usando primeiramente o dia em que foram feitos (padrão `AAAA-MM-DD.md`) na pasta `documentacao/changelogs`.
7. **SEMPRE** Execute um comando no terminal por vez, ao invés de utilizar `&&`, para evitar erros.
8. **SEMPRE** Utilize o `uv` como principal comando, evitando o uso de `pip`.
9. **SEMPRE** seguir a estrutura de arquivos e convenções de nomenclatura definidas.
10. **SEMPRE** delete scripts temporários criados para tarefas pontuais após o uso.
11. **SEMPRE** coloque arquivos de documentação na pasta `documentacao`.
12. **SEMPRE** priorize a **confiabilidade**, **usabilidade** e **acessibilidade**.

---

## 📝 REGRAS DE DESENVOLVIMENTO

1. **Preenchimento de Chefia:** O campo `chefe_imediato` é de preenchimento livre pelo usuário. O campo `Órgão` deve ser selecionado via dropdown.
2. **Frontend:** Usar `fetch` para carregar dados dinâmicos no `DOMContentLoaded`.
3. **Layout:** Manter campos relacionados na mesma linha usando a classe `.form-row`.
4. **Dados Sensíveis:** Nunca incluir CPFs ou senhas reais nos logs ou documentação pública.
