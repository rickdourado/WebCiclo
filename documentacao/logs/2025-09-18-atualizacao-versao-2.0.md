# Changelog - 2025-09-18

## Atualização de Versão

- **Versão anterior:** v1.0
- **Nova versão:** v2.0
- **Motivo:** Reflete as melhorias significativas implementadas no sistema

## Templates Atualizados

Todos os templates foram atualizados para exibir a versão 2.0 no cabeçalho:

1. **`templates/index.html`** - Página principal do formulário
2. **`templates/course_success.html`** - Página de sucesso após criação
3. **`templates/course_edit_success.html`** - Página de sucesso após edição
4. **`templates/course_list.html`** - Lista de cursos
5. **`templates/course_edit.html`** - Página de edição de curso

## Melhorias da Versão 2.0

### Funcionalidades Implementadas
- ✅ Correção do cálculo de Total de Vagas
- ✅ Sincronização de campos entre todos os templates
- ✅ Seção "Informações de Localização" para cursos presenciais/híbridos
- ✅ Campo "Data de Realização" formatado
- ✅ Campos de acessibilidade completos
- ✅ Correção de duplicação de valores monetários (R$ R$)
- ✅ Validação de datas de aulas vs. datas de inscrição
- ✅ Melhoria nas mensagens de erro para usuários
- ✅ Correção de separadores para evitar conflitos com vírgulas em endereços
- ✅ Funcionalidade de adicionar/remover unidades e plataformas
- ✅ Validação robusta de campos obrigatórios

### Correções Técnicas
- ✅ Problema de modificação de variáveis em loops Jinja2
- ✅ Filtros não disponíveis no Jinja2 (`map`, `strip`, `unique`)
- ✅ Limpeza de código duplicado
- ✅ Consolidação de funções JavaScript

## Status
✅ **Concluído:** Sistema atualizado para versão 2.0 com todas as melhorias implementadas
