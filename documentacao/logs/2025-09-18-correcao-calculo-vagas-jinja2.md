# Changelog - 2025-09-18

## Correção Crítica

- **Problema:** O campo "Total de Vagas" na página de sucesso estava exibindo "0 vagas" mesmo com dados válidos
- **Causa:** Limitação do Jinja2 em modificar variáveis dentro de loops (`total_vagas = total_vagas + valor`)

## Solução Implementada

- **Arquivo corrigido:** `templates/course_success.html`
- **Nova abordagem:**
  1. Criar lista `vagas_numericas` para armazenar valores válidos
  2. Usar `vagas_numericas.append()` para adicionar valores
  3. Usar filtro `sum` para calcular o total: `vagas_numericas|sum`
  4. Resultado: Cálculo correto de 35 vagas (25 + 10)

## Código Anterior (Problemático)
```jinja2
{% set total_vagas = 0 %}
{% for vaga in course.vagas_unidade.split('|') %}
    {% set total_vagas = total_vagas + (vaga_limpa|int) %}
{% endfor %}
```

## Código Corrigido
```jinja2
{% set vagas_lista = course.vagas_unidade.split('|') %}
{% set vagas_numericas = [] %}
{% for vaga in vagas_lista %}
    {% set vaga_limpa = vaga.strip() %}
    {% if vaga_limpa and vaga_limpa.isdigit() %}
        {% set _ = vagas_numericas.append(vaga_limpa|int) %}
    {% endif %}
{% endfor %}
{% set total_vagas = vagas_numericas|sum %}
```

## Teste Realizado

- **Curso testado:** Primeiros Socorros Básicos (ID: 10)
- **Dados:** `vagas_unidade = "25|10"`
- **Resultado:** Total de 35 vagas exibido corretamente
- **Status:** ✅ Funcionando
