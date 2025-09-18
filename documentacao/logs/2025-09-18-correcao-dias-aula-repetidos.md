# Changelog - 2025-09-18

## Correção

- **Campo "Dias da Aula" nas Informações Básicas:**
  - Corrigido o problema de repetição de dias de aula na seção "Informações Básicas" das páginas de sucesso e listagem de cursos.
  - O campo agora exibe apenas os dias únicos, evitando duplicação quando há múltiplas unidades com os mesmos dias.
  - A correção foi aplicada nos templates:
    - `templates/course_success.html`
    - `templates/course_list.html` 
    - `templates/course_edit_success.html`
  - Os dias específicos de cada unidade continuam sendo exibidos na seção "Informações de Localização" com detalhes por unidade.

## Implementação

- Implementado loop manual para remover dias duplicados (o filtro `unique` não estava disponível)
- Utilizado método `strip()` para remover espaços em branco
- Mantida a funcionalidade de exibir dias específicos por unidade na seção de localização
- Preservada a separação por pipe (`|`) para dados de múltiplas unidades

## Correção de Erro

- **Erro corrigido:** `No filter named 'strip'` - substituído por implementação manual usando loop e método `.strip()`
- **Solução:** Criado loop que percorre os dias, remove espaços e adiciona apenas dias únicos à lista
