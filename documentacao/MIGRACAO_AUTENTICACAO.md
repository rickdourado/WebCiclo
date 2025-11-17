# Migração de Autenticação para Banco de Dados MySQL

## 📋 Visão Geral

Este documento descreve a migração do sistema de autenticação do WebCiclo Carioca, que anteriormente utilizava credenciais armazenadas no arquivo `.env` para um sistema baseado em banco de dados MySQL.

## 🎯 Objetivos

- ✅ Migrar autenticação de variáveis de ambiente para banco de dados
- ✅ Permitir múltiplos usuários administrativos
- ✅ Rastrear último acesso dos usuários
- ✅ Manter segurança com hash bcrypt
- ✅ Facilitar gerenciamento de usuários

## 🔄 Mudanças Implementadas

### 1. Estrutura do Banco de Dados

#### Tabela `users`
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    ativo ENUM('sim','nao') DEFAULT 'sim',
    ultimo_acesso TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Campos:**
- `id`: Identificador único do usuário
- `email`: Email usado para login (único)
- `senha`: Hash bcrypt da senha
- `ativo`: Status do usuário (sim/nao)
- `ultimo_acesso`: Data/hora do último login
- `created_at`: Data de criação do usuário
- `updated_at`: Data da última atualização

### 2. Arquivos Criados

#### `repositories/user_repository.py`
Repositório responsável por todas as operações de persistência de usuários:

**Métodos:**
- `find_by_email(email)`: Busca usuário por email
- `update_last_access(user_id)`: Atualiza último acesso
- `create_user(email, senha_hash)`: Cria novo usuário
- `deactivate_user(user_id)`: Desativa usuário (soft delete)

#### `scripts/create_admin_user.py`
Script para criar usuário administrador:
```bash
python scripts/create_admin_user.py
```

**Funcionalidades:**
- Solicita email e senha
- Valida formato de email
- Gera hash bcrypt automaticamente
- Cria usuário no banco de dados

#### `scripts/test_auth.py`
Script para testar autenticação:
```bash
python scripts/test_auth.py
```

**Opções:**
1. Testar autenticação com email/senha
2. Listar todos os usuários cadastrados

### 3. Arquivos Modificados

#### `services/auth_service.py`

**Antes:**
```python
def authenticate_admin(self, username: str, password: str) -> Tuple[bool, Optional[str]]:
    # Verificava contra Config.ADMIN_USERNAME e Config.ADMIN_PASSWORD
    if username != self.admin_username:
        return False, "Credenciais inválidas"
    if not self.verify_password(password, Config.ADMIN_PASSWORD):
        return False, "Credenciais inválidas"
    return True, None
```

**Depois:**
```python
def authenticate_admin(self, email: str, password: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    # Busca usuário no banco de dados
    user = self.user_repository.find_by_email(email)
    if not user:
        return False, "Credenciais inválidas", None
    if not self.verify_password(password, user['senha']):
        return False, "Credenciais inválidas", None
    
    # Atualiza último acesso
    self.user_repository.update_last_access(user['id'])
    
    # Retorna dados do usuário
    return True, None, {'id': user['id'], 'email': user['email']}
```

**Novo método adicionado:**
```python
def create_user(self, email: str, password: str) -> Tuple[bool, Optional[str], Optional[int]]:
    # Valida email e senha
    # Gera hash bcrypt
    # Cria usuário no banco
    return True, None, user_id
```

#### `app.py`

**Antes:**
```python
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    success, error_message = auth_service.authenticate_admin(username, password)
    if success:
        session['logged_in'] = True
        session['admin_username'] = username
```

**Depois:**
```python
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    success, error_message, user_data = auth_service.authenticate_admin(email, password)
    if success and user_data:
        session['logged_in'] = True
        session['user_id'] = user_data['id']
        session['user_email'] = user_data['email']
```

**Logout atualizado:**
```python
@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)      # Novo
    session.pop('user_email', None)   # Novo
```

#### `forms.py`

**Antes:**
```python
class LoginForm(FlaskForm):
    username = StringField(
        'Usuário',
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={'placeholder': 'Digite seu usuário'}
    )
```

**Depois:**
```python
class LoginForm(FlaskForm):
    username = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(min=3, max=100)],
        render_kw={'placeholder': 'seu.email@exemplo.com', 'type': 'email'}
    )
```

## 🚀 Como Usar

### 1. Criar Primeiro Usuário Admin

```bash
python scripts/create_admin_user.py
```

**Exemplo de uso:**
```
Digite o email do administrador [admin@cicloscarioca.rio]: admin@prefeitura.rio
Digite a senha do administrador: admin123

📧 Email: admin@prefeitura.rio
🔑 Senha: ********

Deseja criar este usuário? (s/n): s

✅ USUÁRIO CRIADO COM SUCESSO!
   ID: 1
   Email: admin@prefeitura.rio
```

### 2. Testar Autenticação

```bash
python scripts/test_auth.py
```

**Opção 1 - Testar Login:**
```
Escolha uma opção:
1. Testar autenticação
2. Listar usuários cadastrados

Opção (1 ou 2): 1

Email: admin@prefeitura.rio
Senha: admin123

✅ AUTENTICAÇÃO BEM-SUCEDIDA!
   ID: 1
   Email: admin@prefeitura.rio
   Último acesso: 2025-01-17 20:11:32
```

**Opção 2 - Listar Usuários:**
```
Opção (1 ou 2): 2

👥 USUÁRIOS CADASTRADOS

ID: 1
   Email: admin@prefeitura.rio
   Status: ✅ Ativo
   Último acesso: 2025-01-17 20:11:32
   Criado em: 2025-01-17 20:10:13

Total: 1 usuário(s)
```

### 3. Fazer Login no Sistema

1. Acesse: `http://localhost:5000/admin/login`
2. Digite o email: `admin@prefeitura.rio`
3. Digite a senha: `admin123`
4. Clique em "Entrar"

## 🔐 Segurança

### Hash de Senhas
- Utiliza **bcrypt** com 12 rounds
- Senhas nunca são armazenadas em texto plano
- Hash gerado automaticamente na criação do usuário

### Validações
- Email deve ser válido (formato email@dominio.com)
- Senha deve ter no mínimo 6 caracteres
- Usuário deve estar ativo para fazer login
- Último acesso é atualizado a cada login

### Proteção CSRF
- Mantida em todos os formulários
- Token CSRF validado em cada requisição POST

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes (.env) | Depois (MySQL) |
|---------|-------------|----------------|
| **Armazenamento** | Arquivo .env | Banco de dados |
| **Múltiplos usuários** | ❌ Não | ✅ Sim |
| **Rastreamento de acesso** | ❌ Não | ✅ Sim |
| **Gerenciamento** | Manual no .env | Scripts + Interface |
| **Auditoria** | ❌ Não | ✅ Sim (created_at, updated_at) |
| **Desativação** | ❌ Não | ✅ Sim (soft delete) |
| **Segurança** | ✅ Hash bcrypt | ✅ Hash bcrypt |

## 🔄 Migração de Dados

### Variáveis .env (Descontinuadas para Auth)
```env
# Estas variáveis não são mais usadas para autenticação
ADMIN_USERNAME=admin
ADMIN_PASSWORD=$2b$12$...
```

### Novo Fluxo
1. Usuários são criados via script ou interface
2. Credenciais armazenadas na tabela `users`
3. Login usa email ao invés de username

## ⚠️ Observações Importantes

1. **Primeiro Usuário**: Deve ser criado manualmente via script
2. **Email Único**: Cada email só pode ser cadastrado uma vez
3. **Senha Segura**: Recomenda-se senhas com no mínimo 8 caracteres
4. **Backup**: Sempre faça backup da tabela `users` antes de alterações
5. **Ambiente de Produção**: Use senhas fortes e únicas

## 🎯 Próximos Passos

- [ ] Criar interface web para gerenciar usuários
- [ ] Implementar recuperação de senha
- [ ] Adicionar níveis de permissão (admin, editor, visualizador)
- [ ] Implementar log de ações dos usuários
- [ ] Adicionar autenticação de dois fatores (2FA)

## 📝 Notas de Desenvolvimento

### Testado e Funcionando
- ✅ Criação de usuário via script
- ✅ Autenticação via banco de dados
- ✅ Atualização de último acesso
- ✅ Validação de email e senha
- ✅ Proteção CSRF mantida
- ✅ Session management atualizado

### Compatibilidade
- Python 3.8+
- MySQL 8.0+
- Flask 2.3+
- PyMySQL 1.1+
- bcrypt 4.1+

## 📞 Suporte

Em caso de problemas:
1. Verifique conexão com banco de dados: `python scripts/test_db_connection.py`
2. Liste usuários cadastrados: `python scripts/test_auth.py` (opção 2)
3. Teste autenticação: `python scripts/test_auth.py` (opção 1)
4. Verifique logs da aplicação Flask

---

**Data da Migração:** 17/01/2025  
**Versão:** WebCiclo v4  
**Status:** ✅ Concluída e Testada
