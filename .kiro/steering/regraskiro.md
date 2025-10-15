---
inclusion: always
---

# Regras Kiro - Projeto Ciclo Carioca

## Contexto do Projeto
Este é o **WebApp v4 - Ciclo Carioca**, um sistema de criação e gerenciamento de cursos para a Prefeitura do Rio de Janeiro. O sistema permite criar, editar, listar e gerenciar cursos com diferentes modalidades (Presencial, Online, Híbrido).

## Arquitetura do Sistema

### Estrutura de Pastas
```
WebCiclo/
├── app.py                          # Aplicação Flask principal
├── config.py                       # Configurações
├── services/                       # Camada de serviços
│   ├── course_service.py           # Lógica de negócio dos cursos
│   ├── course_status_service.py    # Gerenciamento de status
│   ├── validation_service.py       # Validações
│   ├── ai_service.py              # Integração com Gemini AI
│   └── file_service.py            # Manipulação de arquivos
├── repositories/                   # Camada de dados
│   └── course_repository.py       # Persistência dos cursos
├── templates/                      # Templates HTML
├── static/                         # Arquivos estáticos
├── scripts/                        # Scripts utilitários
└── data/                          # Dados persistidos
```

### Padrões de Código

#### Python/Flask
- Use **type hints** sempre que possível
- Docstrings no formato Google Style
- Tratamento de exceções com logs detalhados
- Separação clara entre camadas (Service → Repository → Scripts)
- Use f-strings para formatação de strings
- Imports organizados: stdlib → third-party → local

#### Templates HTML
- Use **Jinja2** com escape automático
- Classes CSS semânticas e bem estruturadas
- JavaScript vanilla (sem jQuery)
- Responsividade mobile-first
- Acessibilidade (ARIA labels, alt texts)

#### CSS
- Use **CSS Grid** e **Flexbox** para layouts
- Variáveis CSS para cores e espaçamentos
- Animações suaves com `transition`
- Nomenclatura BEM quando apropriado

## Regras de Desenvolvimento

### 1. Validação e Segurança
- **SEMPRE** validar dados de entrada
- Sanitizar uploads de arquivos
- Usar CSRF protection em formulários
- Logs detalhados para debugging
- Tratamento gracioso de erros

### 2. Experiência do Usuário
- Feedback visual para todas as ações
- Loading states para operações assíncronas
- Mensagens de erro claras e acionáveis
- Confirmações para ações destrutivas
- Tooltips e ajuda contextual

### 3. Performance
- Lazy loading para listas grandes
- Compressão de imagens automática
- Cache de dados quando apropriado
- Minimizar requisições desnecessárias

### 4. Manutenibilidade
- Código autodocumentado
- Funções pequenas e focadas
- Reutilização de componentes
- Testes unitários para lógica crítica

## Funcionalidades Específicas

### Sistema de Cursos
- **Modalidades**: Presencial, Online, Híbrido
- **Múltiplas unidades** para cursos presenciais
- **Geração automática** de CSV e PDF
- **Integração com IA** para melhorar descrições
- **Sistema de status** para marcar cursos inseridos

### Autenticação
- Área pública (visualização e duplicação)
- Área administrativa (CRUD completo)
- Login simples com credenciais configuráveis

### Arquivos Gerados
- **CSV**: Dados estruturados para importação
- **PDF**: Documento formatado para impressão
- **Imagens**: Logos de parceiros e capas de cursos

## Convenções de Nomenclatura

### Variáveis e Funções
```python
# Variáveis: snake_case
course_data = {}
user_input = ""

# Funções: snake_case com verbos
def create_course():
def validate_form_data():
def generate_pdf_file():

# Classes: PascalCase
class CourseService:
class ValidationError:
```

### Arquivos e Diretórios
```
# Arquivos: snake_case
course_service.py
validation_service.py

# Templates: snake_case
course_list.html
course_edit.html

# CSS/JS: kebab-case
main-style.css
course-management.js
```

## Tratamento de Erros

### Logs Estruturados
```python
logger.info(f"✅ Curso criado com sucesso: ID {course_id}")
logger.warning(f"⚠️ Aviso na validação: {warning_message}")
logger.error(f"❌ Erro ao processar: {error_message}")
```

### Mensagens Flash
- `success`: Operações bem-sucedidas
- `warning`: Avisos importantes
- `error`: Erros que impedem a operação
- `info`: Informações gerais

## Integração com IA (Gemini)

### Melhoramento de Descrições
- Usar IA para enriquecer descrições de cursos
- Manter descrição original separada
- Fallback gracioso se IA falhar
- Rate limiting para evitar abuse

## Deployment

### PythonAnywhere
- Configuração via `application = app`
- Logs específicos para debug
- Verificação de host para comportamentos específicos
- Middleware para tratamento de requests

## Boas Práticas Específicas

### 1. Formulários Dinâmicos
- JavaScript para adicionar/remover campos
- Validação client-side + server-side
- Preservar dados em caso de erro
- UX intuitiva para múltiplas unidades

### 2. Gestão de Arquivos
- Nomes únicos com timestamps
- Limpeza de arquivos órfãos
- Validação de tipos e tamanhos
- Redimensionamento automático de imagens

### 3. API Design
- Endpoints RESTful
- Respostas JSON consistentes
- Status codes apropriados
- Documentação inline

## Debugging e Manutenção

### Logs Importantes
- Criação/edição de cursos
- Uploads de arquivos
- Erros de validação
- Operações de IA

### Monitoramento
- Tamanho dos diretórios de arquivos
- Performance das operações de IA
- Erros recorrentes
- Uso de recursos

---
# Regras do Projeto WebCiclo
**SEMPRE** Execute um comando no terminal por vez, ao invés de utilizar &&, para evitar erros.
**SEMPRE** Execute o comando conda activate ciclo quando um terminal for aberto.
**SEMPRE** seguir a estrutura de arquivos definida abaixo
5. **SEMPRE** seguir as convenções de nomenclatura e organização
6. **SEMPRE** aplicar as regras de desenvolvimento sem exceção
7. **SEMPRE** usar o ambiente `csv` como principal de desenvolvimento, através do comando `conda activate csv`
8. **SEMPRE** unifique os changelogs usando primeiramente o dia em que foram feitos, mantendo o padrão AAAA-MM-DD.md. Os logs deverão ser armazenados na pasta documentacao/logs
9. **SEMPRE** que precisar criar um script para uma tarefa temporária, delete-o depois
10. **SEMPRE** que criar um arquivo de documentação, coloque-o na pasta documentacao.

**Lembre-se**: Este sistema é usado pela Prefeitura do Rio de Janeiro para gerenciar cursos públicos. Priorize sempre a **confiabilidade**, **usabilidade** e **acessibilidade**.