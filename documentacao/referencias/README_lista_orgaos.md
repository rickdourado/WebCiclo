# Lista de Órgãos - Arquivo CSV

## 📋 Descrição

Este arquivo contém a lista completa e estruturada de todos os órgãos municipais do Rio de Janeiro disponíveis no sistema WebCiclo.Carioca.

## 📁 Localização

```
documentacao/referencias/lista_orgaos.csv
```

## 📊 Estrutura do Arquivo

### Colunas:
- **id**: Identificador único sequencial (1-60)
- **orgao**: Nome completo do órgão
- **sigla**: Sigla oficial do órgão
- **categoria**: Tipo/classificação do órgão

### Exemplo:
```csv
id,orgao,sigla,categoria
1,Secretaria Municipal da Casa Civil - CVL,CVL,Secretaria Municipal
2,Secretaria Municipal de Coordenação Governamental - SMCG,SMCG,Secretaria Municipal
```

## 🏛️ Categorias de Órgãos

### **Secretaria Municipal** (24 órgãos)
- Secretarias administrativas e setoriais
- Exemplos: SME, SMS, SMF, SMCT

### **Secretaria Especial** (8 órgãos)
- Secretarias com foco específico
- Exemplos: JUV-RIO, SPM-RIO, SEDHIR

### **Fundação** (6 órgãos)
- Fundações municipais
- Exemplos: GEO-RIO, RIO-ÁGUAS, PLANETÁRIO

### **Empresa Municipal** (6 órgãos)
- Empresas públicas municipais
- Exemplos: MULTIRIO, IPLANRIO, RIOTUR

### **Companhia Municipal** (4 órgãos)
- Companhias municipais
- Exemplos: COMLURB, RIOLUZ, CET-RIO

### **Instituto** (3 órgãos)
- Institutos municipais
- Exemplos: IPP, IRPH, PREVI-RIO

### **Outros** (9 órgãos)
- Controladoria, Procuradoria, Guarda Municipal, etc.

## 📈 Estatísticas

- **Total de órgãos**: 60
- **Linhas no arquivo**: 61 (incluindo cabeçalho)
- **Categorias diferentes**: 9
- **Última atualização**: 29/09/2025

## 🔄 Atualizações

### Versão Atual (29/09/2025):
- ✅ Adicionados 9 novos órgãos
- ✅ Padronizadas siglas e nomes
- ✅ Criada estrutura CSV organizada
- ✅ Classificação por categorias

### Órgãos Adicionados:
1. Secretaria Municipal da Casa Civil - CVL
2. Secretaria Municipal de Administração - SMA
3. Secretaria Especial de Proteção e Defesa do Consumidor - SEDECON
4. Secretaria Especial de Direitos Humanos e Igualdade Racial - SEDHIR
5. Secretaria Especial de Inclusão - SINC-RIO
6. Fundação Jardim Zoológico da Cidade do Rio de Janeiro - RIO-ZOO
7. Companhia Carioca de Parcerias e Investimentos - CCPAR
8. Companhia Municipal de Transportes Coletivos - CMTC-RIO
9. Riocentro S.A. - Centro de Feiras, Exposições e Congressos do Rio de Janeiro - RIOCENTRO
10. Agência de Fomento do Município do Rio de Janeiro S.A. - INVEST.RIO

## 💻 Uso Técnico

### Importação em Python:
```python
import pandas as pd
df = pd.read_csv('documentacao/referencias/lista_orgaos.csv')
print(df.head())
```

### Importação em JavaScript:
```javascript
// Usando fetch
fetch('documentacao/referencias/lista_orgaos.csv')
  .then(response => response.text())
  .then(data => {
    const lines = data.split('\n');
    const headers = lines[0].split(',');
    // Processar dados...
  });
```

### Uso em Excel/Google Sheets:
1. Abrir arquivo CSV diretamente
2. Separar colunas por vírgula
3. Filtrar por categoria conforme necessário

## 🔗 Relacionamentos

### Arquivos Relacionados:
- `app.py` - Lista ORGAOS (linhas 40-101)
- `documentacao/Listadecursos.txt` - Fonte original
- `templates/index.html` - Formulário de criação
- `templates/course_edit.html` - Formulário de edição

### Integração com Sistema:
- Dropdown de seleção nos formulários
- Validação de órgãos válidos
- Geração de relatórios por órgão
- Análise estatística de cursos por órgão

## 📝 Manutenção

### Para Adicionar Novos Órgãos:
1. Atualizar `documentacao/Listadecursos.txt`
2. Atualizar lista `ORGAOS` em `app.py`
3. Atualizar este arquivo CSV
4. Incrementar ID sequencial
5. Definir categoria apropriada

### Para Modificar Órgãos Existentes:
1. Atualizar nome/sigla nos arquivos fonte
2. Atualizar este CSV
3. Verificar impacto em cursos existentes
4. Testar formulários

## 🎯 Casos de Uso

### **Desenvolvimento:**
- Referência para novos desenvolvedores
- Validação de dados de entrada
- Testes automatizados

### **Análise:**
- Relatórios por categoria de órgão
- Estatísticas de cursos por secretaria
- Análise de distribuição de ofertas

### **Integração:**
- APIs externas
- Sistemas de terceiros
- Importação em outras plataformas

## 📞 Suporte

Para dúvidas sobre este arquivo ou atualizações:
- Verificar changelog em `documentacao/logs/`
- Consultar documentação técnica
- Revisar commits relacionados

---

**Última atualização:** 29 de Setembro de 2025  
**Versão:** 1.0  
**Status:** ✅ Ativo e atualizado
