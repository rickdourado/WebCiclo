# Changelog - 2025-09-18

## Sincronização de Templates

- **Objetivo:** Padronizar os campos exibidos em todos os templates de exibição de cursos
- **Templates atualizados:** `course_edit_success.html` e `course_list.html`

## Campos Adicionados

### 1. Total de Vagas
- **Localização:** Seção "Informações Acadêmicas"
- **Funcionalidade:** Soma todas as vagas das unidades usando o separador `|`
- **Implementação:** Cálculo correto usando lista e filtro `sum` do Jinja2

### 2. Informações de Localização
- **Localização:** Nova seção específica para cursos presenciais/híbridos
- **Campos incluídos:**
  - Endereço por unidade
  - Bairro por unidade
  - Vagas por unidade
  - Período das aulas por unidade
  - Horário por unidade
  - Dias da aula por unidade
- **Condição:** Exibida apenas para modalidades "Presencial" e "Híbrido"

### 3. Data de Realização
- **Localização:** Seção "Informações Básicas"
- **Funcionalidade:** Exibe período de início e fim das aulas
- **Formato:** DD/MM/AAAA

### 4. Campos de Acessibilidade
- **Acessibilidade:** Status de acessibilidade do curso
- **Recursos de Acessibilidade:** Detalhes dos recursos disponíveis

## Melhorias Implementadas

### Cálculo de Total de Vagas
- **Problema anterior:** Cálculo incorreto devido a limitação do Jinja2
- **Solução:** Uso de lista `vagas_numericas` e filtro `sum`
- **Resultado:** Cálculo preciso da soma de todas as vagas

### Consistência Visual
- **Padronização:** Todos os templates agora exibem as mesmas informações
- **Organização:** Seções bem estruturadas e organizadas
- **Responsividade:** Mantida a responsividade em todos os dispositivos

## Arquivos Modificados

1. **`templates/course_edit_success.html`**
   - Adicionado campo "Total de Vagas"
   - Adicionada seção "Informações de Localização"
   - Adicionado campo "Data de Realização"
   - Adicionados campos de acessibilidade

2. **`templates/course_list.html`**
   - Adicionado campo "Total de Vagas"
   - Adicionada seção "Informações de Localização"
   - Adicionado campo "Data de Realização"
   - Adicionados campos de acessibilidade

## Status
✅ **Concluído:** Todos os templates agora exibem informações consistentes e completas
