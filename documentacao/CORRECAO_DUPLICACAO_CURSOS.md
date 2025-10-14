# Correção do Sistema de Duplicação de Cursos

## Problema Identificado

Quando um curso era duplicado com o mesmo nome (ex: "Primeiros Socorros"), o sistema sobrescrevia a primeira versão em vez de criar um novo curso com ID único.

## Causa Raiz

O problema estava na **geração dos nomes dos arquivos CSV e PDF**:

### Antes da Correção:
```
Nome do arquivo: YYYYMMDD_Titulo_do_Curso.csv
Exemplo: 20241014_Primeiros_Socorros.csv
```

### Problema:
- Cursos duplicados no mesmo dia com o mesmo nome geravam arquivos com nomes idênticos
- O segundo arquivo sobrescrevia o primeiro
- Resultado: apenas um curso existia, mesmo com IDs diferentes

## Soluções Implementadas

### 1. Inclusão do ID Único nos Nomes dos Arquivos

#### CSV Generator (`scripts/csv_generator.py`):
```python
# ANTES:
filename = f"{data_atual}_{titulo_formatado}.csv"

# DEPOIS:
course_id = course_data.get('id', 'unknown')
filename = f"{data_atual}_{course_id}_{titulo_formatado}.csv"
```

#### PDF Generator (`scripts/pdf_generator.py`):
```python
# ANTES:
filename = f"{data_atual}_{titulo_formatado}.pdf"

# DEPOIS:
course_id = course_data.get('id', 'unknown')
filename = f"{data_atual}_{course_id}_{titulo_formatado}.pdf"
```

### 2. Melhoria na Exclusão de Cursos

Atualizado o método `delete_course()` no repositório para:
- ✅ Buscar arquivos pelo ID do curso (mais preciso)
- ✅ Manter compatibilidade com arquivos antigos (fallback)
- ✅ Logs detalhados para debug

### 3. Novo Formato dos Nomes de Arquivos

#### Antes:
```
20241014_Primeiros_Socorros.csv
20241014_Primeiros_Socorros.pdf
```

#### Depois:
```
20241014_123_Primeiros_Socorros.csv  (ID: 123)
20241014_124_Primeiros_Socorros.csv  (ID: 124)
20241014_125_Primeiros_Socorros.csv  (ID: 125)
```

## Benefícios da Correção

### ✅ **Cursos Únicos Garantidos**
- Cada duplicação gera um novo ID único
- Arquivos nunca são sobrescritos
- Múltiplas versões do mesmo curso podem coexistir

### ✅ **Rastreabilidade Melhorada**
- ID único no nome do arquivo facilita identificação
- Logs detalhados para debug
- Busca mais precisa por ID

### ✅ **Compatibilidade Mantida**
- Sistema funciona com arquivos antigos
- Migração transparente
- Sem perda de dados existentes

## Fluxo Após a Correção

### Duplicação de "Primeiros Socorros":

1. **Primeira duplicação:**
   - ID: 123
   - Arquivos: `20241014_123_Primeiros_Socorros.csv/pdf`

2. **Segunda duplicação:**
   - ID: 124 (novo ID único)
   - Arquivos: `20241014_124_Primeiros_Socorros.csv/pdf`

3. **Terceira duplicação:**
   - ID: 125 (novo ID único)
   - Arquivos: `20241014_125_Primeiros_Socorros.csv/pdf`

### Resultado:
- ✅ **3 cursos distintos** com o mesmo nome
- ✅ **3 conjuntos de arquivos** únicos
- ✅ **Nenhuma sobrescrita** de dados

## Arquivos Modificados

1. **`scripts/csv_generator.py`** - Inclusão do ID no nome do arquivo CSV
2. **`scripts/pdf_generator.py`** - Inclusão do ID no nome do arquivo PDF  
3. **`repositories/course_repository.py`** - Melhoria na exclusão de cursos

## Status
✅ **CONCLUÍDO** - Sistema de duplicação corrigido com sucesso!

Agora é possível ter múltiplos cursos com o mesmo nome, cada um com seu ID único e arquivos distintos.