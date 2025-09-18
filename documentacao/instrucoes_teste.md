# Instruções para Execução dos Testes do Formulário

## Visão Geral

Este documento contém instruções para executar os testes manuais do formulário de criação de curso do WebCiclo. Foram criados 10 casos de teste aleatórios que cobrem diferentes cenários de uso.

## Arquivos Criados

### 1. **casos_teste_formulario.md**
- Documentação completa dos 10 casos de teste
- Descrição detalhada de cada cenário
- Observações sobre campos obrigatórios e condicionais

### 2. **dados_teste_estruturados.json**
- Dados estruturados em formato JSON
- Facilita a consulta dos dados de teste
- Contém todas as informações necessárias para cada caso

## Pré-requisitos

### 1. Verificar se a Aplicação está Rodando
```bash
# No diretório do projeto
python app.py
```

A aplicação deve estar rodando em `http://localhost:5001`

## Execução dos Testes

### Método: Execução Manual
```bash
# Abrir o navegador manualmente
# Navegar para http://localhost:5001
# Usar os dados do arquivo casos_teste_formulario.md
```

## Casos de Teste Disponíveis

### 1. **Curso Presencial de Tecnologia**
- Modalidade: Presencial
- Categoria: Tech
- Curso gratuito
- Com certificado

### 2. **Curso Online de Marketing Digital**
- Modalidade: Online
- Categoria: Marketing
- Curso pago (com valores inteira/meia)
- Com bolsa e parceiro externo

### 3. **Curso Híbrido de Gastronomia**
- Modalidade: Híbrido
- Categoria: Gastronomia
- Curso pago
- Não acessível para PCD

### 4. **Curso Online Assíncrono de Design**
- Modalidade: Online
- Categoria: Design
- Aulas assíncronas
- Curso gratuito

### 5. **Curso Presencial de Saúde**
- Modalidade: Presencial
- Categoria: Saúde
- Curso gratuito
- Com parceiro externo (Corpo de Bombeiros)

### 6. **Curso Online de Finanças**
- Modalidade: Online
- Categoria: Finanças
- Curso pago com bolsa
- Aulas síncronas

### 7. **Curso Presencial de Educação**
- Modalidade: Presencial
- Categoria: Educação
- Curso gratuito
- Com parceiro externo (UFRJ)

### 8. **Curso Online de Cibersegurança**
- Modalidade: Online
- Categoria: Cibersegurança
- Curso gratuito
- Aulas síncronas

### 9. **Curso Híbrido de Sustentabilidade**
- Modalidade: Híbrido
- Categoria: Sustentabilidade
- Curso pago com bolsa
- Com parceiro externo (INEA)

### 10. **Curso Presencial de Artes**
- Modalidade: Presencial
- Categoria: Artes
- Curso pago com bolsa
- Com parceiro externo (Teatro Municipal)

## Validações Testadas

### Campos Obrigatórios
- ✅ Nome do Curso
- ✅ Descrição
- ✅ Datas de inscrição
- ✅ Órgão
- ✅ Categoria
- ✅ Modalidade
- ✅ Acessibilidade
- ✅ Público-alvo
- ✅ Curso gratuito/pago
- ✅ Oferece certificado
- ✅ Oferece bolsa
- ✅ Informações adicionais
- ✅ Parceiro externo

### Campos Condicionais
- ✅ **Modalidade Presencial/Híbrido**: Endereço, bairro, vagas, carga horária, datas e horários
- ✅ **Modalidade Online**: Plataforma digital, vagas, carga horária, aulas assíncronas
- ✅ **Curso Pago**: Valores inteira/meia, condições para meia-entrada
- ✅ **Oferece Certificado**: Pré-requisitos para certificado
- ✅ **Oferece Bolsa**: Valor da bolsa, requisitos para bolsa
- ✅ **Acessibilidade**: Recursos de acessibilidade (se acessível ou exclusivo)
- ✅ **Informações Adicionais**: Campo de informações adicionais (se sim)
- ✅ **Parceiro Externo**: Nome do parceiro, logo, link (se sim)

### Validações de Negócio
- ✅ Datas de fim posteriores às datas de início
- ✅ Horário de fim posterior ao horário de início
- ✅ Pelo menos um dia da semana selecionado
- ✅ Valores monetários no formato correto
- ✅ URLs de parceiros válidas

## Interpretação dos Resultados

### Sucesso ✅
- Formulário preenchido completamente
- Submissão bem-sucedida
- Redirecionamento para página de sucesso
- Geração de arquivos CSV e PDF

### Falha ❌
- Campo obrigatório não preenchido
- Validação de negócio falhou
- Erro na submissão do formulário
- Problema de conectividade

## Troubleshooting

### Problema: Aplicação não está rodando
```bash
# Verificar se a aplicação está rodando
curl http://localhost:5001

# Ou iniciar a aplicação
python app.py
```

### Problema: Elementos não encontrados
- Verificar se o formulário carregou completamente
- Verificar se os IDs dos elementos estão corretos
- Verificar se há JavaScript que modifica o DOM

## Personalização dos Testes

### Adicionar Novos Casos de Teste
1. Editar o arquivo `dados_teste_estruturados.json`
2. Adicionar novo objeto no array `casos_teste`
3. Documentar no arquivo `casos_teste_formulario.md`

### Modificar Dados Existentes
1. Editar o arquivo `dados_teste_estruturados.json`
2. Modificar os dados desejados
3. Atualizar documentação se necessário

## Relatórios

Para cada teste manual, documente:
- ✅ Caso de teste executado
- ✅ Campos preenchidos corretamente
- ✅ Validações que funcionaram
- ❌ Problemas encontrados
- 📝 Observações importantes

## Próximos Passos

1. **Executar os testes** com os dados fornecidos
2. **Analisar os resultados** e identificar problemas
3. **Corrigir bugs** encontrados nos testes
4. **Expandir os casos de teste** conforme necessário
5. **Documentar** novos cenários encontrados

## Contato

Para dúvidas ou problemas com os testes, consulte:
- Documentação do projeto em `documentacao/`
- Logs da aplicação
- Issues do repositório