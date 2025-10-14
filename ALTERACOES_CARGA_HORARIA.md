# Alterações Realizadas - Campo Carga Horária

## Resumo das Mudanças

O campo "Carga Horária" foi movido dos subformulários de modalidade para a página principal do formulário, posicionado entre os campos "Categoria" e "Modalidade".

## Arquivos Modificados

### 1. templates/index.html
- ✅ Adicionado campo "Carga Horária" na página principal (entre Categoria e Modalidade)
- ✅ Removido campo "Carga Horária" do subformulário presencial
- ✅ Removido campo "Carga Horária" do subformulário online
- ✅ Removido campo "Carga Horária" do template de nova unidade
- ✅ Removidas referências JavaScript aos campos de carga horária dos subformulários
- ✅ Corrigido caractere × para &times; nos botões

### 2. templates/course_edit.html
- ✅ Adicionado campo "Carga Horária" na página principal (entre Categoria e Modalidade)
- ✅ Removido campo "Carga Horária" do subformulário presencial
- ✅ Removido campo "Carga Horária" do subformulário online
- ✅ Corrigido caractere × para &times; nos botões

### 3. templates/course_duplicate.html
- ✅ Adicionado campo "Carga Horária" na página principal (entre Categoria e Modalidade)
- ✅ Removido campo "Carga Horária" do subformulário presencial
- ✅ Removido campo "Carga Horária" do subformulário online
- ✅ Removido campo "Carga Horária" do template de nova unidade
- ✅ Removida verificação JavaScript especial para campos de carga horária ocultos
- ✅ Corrigido caractere × para &times; nos botões

### 4. templates/index_unidades_clean.html
- ✅ Removido campo "Carga Horária" dos subformulários

## Benefícios da Alteração

1. **Consistência**: Cada curso agora tem uma carga horária fixa, independente da modalidade
2. **Simplicidade**: Campo único na página principal, mais fácil de preencher
3. **Lógica de negócio**: Alinhado com o requisito de que a carga horária não varia por unidade
4. **UX melhorada**: Menos campos repetitivos nos subformulários

## Estrutura do Formulário Após as Alterações

```
Página Principal:
├── Nome do Curso
├── Descrição
├── Categoria ⭐
├── Carga Horária ⭐ (NOVO POSICIONAMENTO)
├── Modalidade ⭐
└── [Subformulários baseados na modalidade selecionada]
    ├── Presencial/Híbrido: Endereço, Bairro, Vagas, Datas, Horários
    └── Online: Plataforma, Vagas, Aulas Assíncronas, Datas, Horários
```

## Status
✅ **CONCLUÍDO** - Todas as alterações foram implementadas com sucesso.