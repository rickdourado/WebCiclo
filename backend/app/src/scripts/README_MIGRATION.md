# 🚀 Migração CSV → MySQL

Scripts para migrar dados dos arquivos CSV para o banco de dados MySQL.

## 📋 Scripts Disponíveis

### 1. `migrate_csv_to_mysql.py` - Script Principal de Migração
Migra todos os cursos dos arquivos CSV para o banco de dados MySQL.

**Uso:**
```bash
python scripts/migrate_csv_to_mysql.py
```

**O que faz:**
- ✅ Lê todos os arquivos CSV do diretório `CSV/`
- ✅ Processa e valida os dados
- ✅ Insere cursos na tabela `cursos`
- ✅ Insere turmas presenciais na tabela `turmas`
- ✅ Insere dias da semana na tabela `turmas_dias_semana`
- ✅ Insere plataformas online na tabela `plataformas_online`
- ✅ Mostra estatísticas da migração
- ✅ Verifica automaticamente os dados migrados

**Saída esperada:**
```
================================================================================
🚀 INICIANDO MIGRAÇÃO CSV → MySQL
================================================================================
✅ Conexão com banco de dados estabelecida
📁 Encontrados 19 arquivos CSV
--------------------------------------------------------------------------------
📄 Processando: 20251114_1_BARBEARIA.csv
   ✅ Curso 'BARBEARIA' migrado (ID: 1)
...
--------------------------------------------------------------------------------
📊 ESTATÍSTICAS DA MIGRAÇÃO
   • Cursos migrados: 19
   • Erros: 0
   • Taxa de sucesso: 100.0%
================================================================================
```

---

### 2. `verify_mysql_data.py` - Verificação de Integridade
Verifica a integridade e consistência dos dados migrados.

**Uso:**
```bash
python scripts/verify_mysql_data.py
```

**O que verifica:**
- ✅ Cursos presenciais sem turmas
- ✅ Cursos online sem plataforma
- ✅ Campos obrigatórios vazios
- ✅ Datas inválidas (início > fim)
- ✅ Turmas sem dias da semana
- ✅ Estatísticas por modalidade e órgão
- ✅ Mostra dados de exemplo

**Saída esperada:**
```
================================================================================
🔍 VERIFICAÇÃO DE INTEGRIDADE DOS DADOS
================================================================================

📋 Verificando cursos presenciais sem turmas...
✅ Todos os cursos presenciais têm turmas

💻 Verificando cursos online sem plataforma...
✅ Todos os cursos online têm plataforma

📝 Verificando campos obrigatórios...
✅ Todos os cursos têm campos obrigatórios preenchidos

📅 Verificando datas...
✅ Todas as datas estão corretas

📊 Estatísticas por modalidade:
   • Presencial: 15 cursos
   • Online: 3 cursos
   • Híbrido: 1 curso

================================================================================
✅ VERIFICAÇÃO CONCLUÍDA - NENHUM PROBLEMA ENCONTRADO!
================================================================================
```

---

## 🔧 Pré-requisitos

1. **Banco de dados MySQL configurado**
   - Tabelas criadas (use `scripts/create_database.sql`)
   - Usuário admin criado (use `scripts/create_admin_user.py`)

2. **Variáveis de ambiente configuradas** (`.env`)
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=sua_senha
   DB_NAME=cursoscarioca
   ```

3. **Dependências Python instaladas**
   ```bash
   pip install pymysql python-dotenv
   ```

---

## 📝 Processo Completo de Migração

### Passo 1: Backup dos dados CSV (opcional mas recomendado)
```bash
python scripts/compress_csv_backup.py
```

### Passo 2: Executar migração
```bash
python scripts/migrate_csv_to_mysql.py
```

### Passo 3: Verificar dados
```bash
python scripts/verify_mysql_data.py
```

### Passo 4: Testar aplicação
```bash
# Inicie o servidor Flask
python app.py

# Acesse http://localhost:5000
# Faça login no admin
# Verifique se os cursos aparecem corretamente
```

### Passo 5: Limpeza (após confirmar que está tudo OK)
```bash
# Delete os scripts temporários
rm scripts/migrate_csv_to_mysql.py
rm scripts/verify_mysql_data.py
rm scripts/compress_csv_backup.py
rm scripts/compress_csv_simple.py
rm scripts/README_MIGRATION.md
```

---

## ⚠️ Problemas Comuns

### Erro: "Conexão recusada"
**Causa:** MySQL não está rodando ou credenciais incorretas
**Solução:** 
```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql

# Testar conexão
mysql -u root -p
```

### Erro: "Tabela não existe"
**Causa:** Banco de dados não foi criado
**Solução:**
```bash
# Criar banco e tabelas
mysql -u root -p < scripts/create_database.sql
```

### Erro: "Duplicate entry"
**Causa:** Tentando migrar dados que já existem
**Solução:**
```bash
# Limpar tabelas antes de migrar novamente
mysql -u root -p cursoscarioca -e "
TRUNCATE TABLE turmas_dias_semana;
TRUNCATE TABLE turmas;
TRUNCATE TABLE plataformas_online;
TRUNCATE TABLE cursos;
"
```

### Aviso: "Cursos sem turmas"
**Causa:** Dados incompletos no CSV
**Solução:** Verificar arquivo CSV original e corrigir manualmente no banco

---

## 📊 Estrutura dos Dados

### Arquivo CSV
```csv
tipo_acao,titulo,descricao_original,inicio_inscricoes,fim_inscricoes,...
Curso,BARBEARIA,"Descrição do curso",2025/10/10,2025/10/31,...
```

### Banco de Dados MySQL
```
cursos (tabela principal)
├── turmas (1:N)
│   └── turmas_dias_semana (1:N)
└── plataformas_online (1:1)
```

---

## 🎯 Resultado Esperado

Após a migração bem-sucedida:
- ✅ Todos os cursos dos arquivos CSV estarão no MySQL
- ✅ Turmas presenciais com endereços e horários
- ✅ Dias da semana de cada turma
- ✅ Plataformas online para cursos EAD
- ✅ Dados acessíveis via aplicação web
- ✅ Sistema pronto para produção

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs detalhados no console
2. Execute o script de verificação
3. Revise as configurações do `.env`
4. Verifique se o MySQL está acessível

---

**Data:** 2025-11-18  
**Versão:** 1.0  
**Autor:** Sistema WebCiclo
