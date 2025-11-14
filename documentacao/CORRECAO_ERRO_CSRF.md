# Correção: Erro de Mensagem CSRF Incorreta

## Resumo do Problema

Ao tentar criar um curso online no PythonAnywhere, o sistema exibia incorretamente:
```
"Erro de Validação: Erro de segurança: Token CSRF inválido ou expirado. Tente novamente"
```

Quando na verdade o erro era de **validação de datas**.

## Análise Técnica

### Logs do PythonAnywhere
```
Falha na criação do curso: ['Início das aulas da unidade 1 deve ser posterior ou igual ao fim das inscrições (14/11/2025)', ...]
csrf_token: ImE0NWIyYjM0Nzc3OGNhMzhmNTgyMDI1ZDFlY2ZkM2M0MjRlMjM2NmIi.aRdoFA.fvY5Fb0bQaqBRw5Ndnnql_WSkLA
```

**Conclusão**: O token CSRF estava válido. O erro era de validação de datas.

## Correções Implementadas

### 1. Handler de Erro 400 (`app.py`)

**Problema**: O handler interceptava todos os erros HTTP 400, incluindo redirecionamentos após validação.

**Solução**: Verificar se o erro é realmente CSRF antes de exibir a mensagem.

```python
@app.errorhandler(400)
def csrf_error(e):
    """Handler personalizado para erros CSRF"""
    # Verificar se é realmente um erro CSRF e não um erro de validação
    error_description = str(e.description) if hasattr(e, 'description') else str(e)
    if 'CSRF' in error_description or 'csrf' in error_description.lower():
        logger.warning(f"🔒 Erro CSRF detectado: {e}")
        flash('Erro de segurança: Token CSRF inválido ou expirado. Tente novamente.', 'error')
        return redirect(request.referrer or url_for('index'))
    # Se não for erro CSRF, deixar o Flask tratar normalmente
    return e
```

### 2. Validação de Datas para Cursos Online (`services/validation_service.py`)

**Problema**: A validação de datas estava sendo aplicada a cursos online assíncronos, que não têm datas fixas de aulas.

**Solução**: Pular validação de datas de aulas para cursos online assíncronos.

```python
def _validate_aulas_dates(self, form_data: Dict, inicio_inscricoes: str, fim_inscricoes: str):
    """Valida datas das aulas em relação às datas de inscrições"""
    if not inicio_inscricoes or not fim_inscricoes:
        return
    
    # Para cursos online com aulas assíncronas, não validar datas de aulas
    modalidade = form_data.get('modalidade')
    aulas_assincronas = form_data.get('aulas_assincronas')
    
    if modalidade == 'Online' and aulas_assincronas == 'sim':
        # Cursos online assíncronos não têm datas de início/fim de aulas
        return
    
    # ... resto da validação
```

## Melhorias Adicionais

1. **Filtro de datas válidas**: Agora só valida datas que não estão vazias
2. **Validação adicional**: Verifica se fim das aulas >= início das aulas
3. **Mensagens mais claras**: Erros específicos para cada tipo de problema

## Como Testar

### Teste 1: Curso Online Assíncrono
1. Criar curso com modalidade "Online"
2. Selecionar "Aulas Assíncronas: Sim"
3. Não preencher datas de início/fim de aulas
4. ✅ Deve criar sem erro

### Teste 2: Curso Online Síncrono
1. Criar curso com modalidade "Online"
2. Selecionar "Aulas Assíncronas: Não"
3. Preencher datas de início/fim de aulas
4. ✅ Deve validar que início >= fim das inscrições

### Teste 3: Erro de Validação Real
1. Criar curso com data de início de aulas < fim das inscrições
2. ✅ Deve exibir: "Início das aulas deve ser posterior ou igual ao fim das inscrições"
3. ❌ NÃO deve exibir: "Token CSRF inválido"

### Teste 4: Erro CSRF Real
1. Deixar formulário aberto por muito tempo (token expira)
2. Tentar submeter
3. ✅ Deve exibir: "Token CSRF inválido ou expirado"

## Arquivos Modificados

- `app.py` - Handler de erro 400
- `services/validation_service.py` - Validação de datas
- `documentacao/logs/2025-11-14.md` - Changelog

## Próximos Passos

1. ✅ Deploy no PythonAnywhere
2. ✅ Testar todos os cenários acima
3. 🔄 Considerar adicionar validação de datas no frontend (JavaScript)
4. 🔄 Melhorar UX com mensagens de ajuda sobre regras de datas
