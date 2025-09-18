# Changelog - 2025-09-18

## Correção

- **Cálculo do Total de Vagas:**
  - Corrigido o cálculo do "Total de Vagas" na seção "Informações Acadêmicas" da página de sucesso
  - O sistema agora soma corretamente as vagas de todas as unidades quando há múltiplas unidades
  - Melhorada a robustez do código para lidar com valores vazios ou inválidos

## Implementação

- **Arquivo corrigido:** `templates/course_success.html`
- **Melhorias implementadas:**
  - Adicionada validação `vaga_limpa.isdigit()` para garantir que apenas números válidos sejam somados
  - Removidos valores vazios do campo `vagas_unidade` no arquivo CSV do curso "Primeiros Socorros"
  - Mantida a separação por pipe (`|`) para dados de múltiplas unidades

## Arquivo CSV Corrigido

- **Arquivo:** `CSV/20250918_Primeiros_Socorros_Básicos.csv`
- **Correção:** Removido valor vazio no final do campo `vagas_unidade` (era `25|10|`, agora é `25|10`)
- **Resultado:** Cálculo correto do total de vagas (25 + 10 = 35 vagas)

## Funcionalidade

- O campo "Total de Vagas" agora exibe a soma correta de todas as vagas das unidades
- Valores individuais por unidade continuam sendo exibidos na seção "Informações de Localização"
- Sistema robusto contra valores inválidos ou vazios
