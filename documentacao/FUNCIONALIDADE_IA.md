# Funcionalidade de Integração com IA

## Visão Geral

O WebCiclo utiliza a API do Google Gemini para melhorar automaticamente as descrições dos cursos cadastrados no sistema. A integração é feita de forma transparente durante o processo de criação de cursos, garantindo que as descrições sejam objetivas, claras e adequadas ao público-alvo.

## Tecnologia Utilizada

- **API:** Google Gemini AI
- **Modelo:** `gemini-2.5-pro` (versão estável testada)
- **Biblioteca:** `google.generativeai` (Python)

## Arquitetura da Funcionalidade

### Estrutura de Arquivos

```
services/
├── ai_service.py          # Serviço principal de integração com IA
└── course_service.py      # Serviço que utiliza o AIService

config.py                  # Configurações da API (chave e modelo)
```

### Fluxo de Execução

```
1. Usuário preenche formulário de criação de curso
   ↓
2. CourseService.create_course() é chamado
   ↓
3. CourseService._enhance_description() é executado
   ↓
4. AIService.enhance_description() faz chamada à API Gemini
   ↓
5. Descrição melhorada é retornada e salva no curso
```

## Funcionalidades Disponíveis

### 1. Melhoria Automática de Descrições (`enhance_description`)

**Localização:** `services/ai_service.py` (linhas 25-63)

**Função:** Melhora automaticamente a descrição do curso cadastrado, tornando-a mais objetiva e clara.

**Como funciona:**
- Recebe a descrição original digitada pelo usuário
- Verifica se a API key está configurada
- Configura o modelo Gemini (`gemini-2.5-pro`)
- Envia um prompt específico para o Gemini solicitando uma versão simplificada em até 3 linhas
- O prompt instrui a IA a manter o texto em português, ser direto e objetivo
- Retorna a descrição melhorada ou a original em caso de erro

**Código completo da função:**
```25:63:services/ai_service.py
def enhance_description(self, description: str) -> str:
    """
    Melhora a descrição usando Gemini
    
    Args:
        description: Descrição original
        
    Returns:
        str: Descrição melhorada ou original se houver erro
    """
    print(f"\nTentando melhorar descrição com Gemini...")
    print(f"Descrição original: {description}")
    
    # Verificar se a API key está configurada
    if not self.api_key:
        print("API key do Gemini não configurada. Retornando descrição original.")
        return description
    
    try:
        print("Configurando modelo Gemini...")
        model = genai.GenerativeModel(model_name=self.model_name)
        
        prompt = f"""Explique de forma simples o que o curso ensina em no máximo 3 linhas. Mantenha em português, seja direto e objetivo:

{description}"""
        print("Enviando prompt para o Gemini...")
        
        response = model.generate_content(prompt)
        enhanced = response.text.strip()
        
        print(f"Descrição melhorada: {enhanced}")
        return enhanced
        
    except Exception as e:
        print(f"\nERRO ao melhorar descrição com Gemini: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")
        import traceback
        print(f"Traceback completo:\n{traceback.format_exc()}")
        return description
```

**Prompt utilizado:**
```47:49:services/ai_service.py
prompt = f"""Explique de forma simples o que o curso ensina em no máximo 3 linhas. Mantenha em português, seja direto e objetivo:

{description}"""
```

**Características:**
- ✅ Execução automática durante a criação do curso
- ✅ Fallback gracioso: retorna descrição original em caso de erro
- ✅ Não bloqueia o cadastro se a IA falhar
- ✅ Logs detalhados para debug

**Exemplo de uso:**
```276:289:services/course_service.py
def _enhance_description(self, course_data: Dict) -> Dict:
    """Melhora a descrição usando IA"""
    try:
        original_description = course_data.get('descricao_original', '')
        if original_description:
            enhanced_description = self.ai_service.enhance_description(original_description)
            course_data['descricao'] = enhanced_description
        else:
            course_data['descricao'] = original_description
    except Exception as e:
        print(f"Erro ao melhorar descrição: {str(e)}")
        course_data['descricao'] = course_data.get('descricao_original', '')
    
    return course_data
```

### 2. Análise de Imagem de Capa (`analyze_course_image`)

**Localização:** `services/ai_service.py` (linhas 69-165)

**Função:** Analisa se a imagem de capa do curso é adequada para uso.

**Status:** ⚠️ **Disponível mas não implementado no fluxo principal**

**Como funciona:**
- Recebe o caminho da imagem e o título do curso (opcional)
- Verifica se a API key está configurada
- Faz upload da imagem usando PIL (Pillow)
- Utiliza o modelo `gemini-2.5-flash` para análise de imagem
- Avalia aspectos como:
  - Presença excessiva de textos ou logotipos
  - Clareza visual
  - Simplicidade dos elementos
  - Representatividade educacional
  - Qualidade visual
- Processa a resposta JSON e trata erros de parsing

**Código completo da função:**
```69:165:services/ai_service.py
def analyze_course_image(self, image_path: str, course_title: str = None) -> dict:
    """
    Analisa se a imagem é adequada para uso como capa de curso
    
    Args:
        image_path: Caminho para a imagem
        course_title: Título do curso (opcional)
        
    Returns:
        dict: Resultado da análise com recomendações
    """
    print(f"\nAnalisando imagem do curso com Gemini...")
    print(f"Imagem: {image_path}")
    print(f"Curso: {course_title}")
    
    # Verificar se a API key está configurada
    if not self.api_key:
        print("API key do Gemini não configurada. Pulando análise de imagem.")
        return {
            'is_suitable': True,
            'confidence': 0,
            'issues': [],
            'suggestions': [],
            'message': 'Análise não disponível (API key não configurada)'
        }
    
    try:
        # Upload da imagem para o Gemini
        print("Fazendo upload da imagem para o Gemini...")
        import PIL.Image
        img = PIL.Image.open(image_path)
        
        model = genai.GenerativeModel(model_name='gemini-2.5-flash')
        
        # Prompt para análise
        context = f" para o curso '{course_title}'" if course_title else ""
        prompt = f"""Analise esta imagem que será usada como capa{context}.

Avalie se a imagem é adequada considerando:
1. Contém textos, logotipos ou grafismos excessivos?
2. É visualmente limpa e de fácil leitura?
3. Os elementos visuais são poucos e simples?
4. A imagem é representativa de conteúdo educacional?
5. A qualidade visual é adequada?

Responda em formato JSON com:
{{
    "is_suitable": true/false,
    "confidence": 0-100,
    "issues": ["lista de problemas encontrados"],
    "suggestions": ["lista de sugestões de melhoria"],
    "summary": "resumo da análise em 1-2 linhas"
}}"""

        print("Enviando imagem e prompt para análise...")
        response = model.generate_content([prompt, img])
        
        print(f"Resposta recebida do Gemini")
        
        # Processar resposta
        response_text = response.text.strip()
        
        # Remover marcadores de código se existirem
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        # Tentar parsear JSON
        import json
        try:
            result = json.loads(response_text)
            print(f"Análise completa: {result.get('summary', 'Sem resumo')}")
            return result
        except json.JSONDecodeError:
            # Se não for JSON válido, criar resposta padrão
            print("Resposta não está em formato JSON, usando análise básica")
            return {
                'is_suitable': True,
                'confidence': 50,
                'issues': [],
                'suggestions': [],
                'summary': response_text[:200],
                'message': 'Análise concluída'
            }
            
    except Exception as e:
        print(f"Erro ao analisar imagem com Gemini: {str(e)}")
        print(f"Detalhes do erro: {type(e).__name__}")
        return {
            'is_suitable': True,
            'confidence': 0,
            'issues': [],
            'suggestions': [],
            'message': f'Erro na análise: {str(e)}'
        }
```

**Retorno (formato JSON):**
```json
{
    "is_suitable": true/false,
    "confidence": 0-100,
    "issues": ["lista de problemas encontrados"],
    "suggestions": ["lista de sugestões de melhoria"],
    "summary": "resumo da análise em 1-2 linhas"
}
```

**Prompt utilizado:**
```103:121:services/ai_service.py
context = f" para o curso '{course_title}'" if course_title else ""
prompt = f"""Analise esta imagem que será usada como capa{context}.

Avalie se a imagem é adequada considerando:
1. Contém textos, logotipos ou grafismos excessivos?
2. É visualmente limpa e de fácil leitura?
3. Os elementos visuais são poucos e simples?
4. A imagem é representativa de conteúdo educacional?
5. A qualidade visual é adequada?

Responda em formato JSON com:
{{
    "is_suitable": true/false,
    "confidence": 0-100,
    "issues": ["lista de problemas encontrados"],
    "suggestions": ["lista de sugestões de melhoria"],
    "summary": "resumo da análise em 1-2 linhas"
}}"""
```

## Configuração

### Variáveis de Ambiente Necessárias

A chave da API do Gemini deve ser configurada através de variável de ambiente:

```bash
# .env ou variável de ambiente do sistema
GEMINI_API_KEY=sua_chave_api_aqui
```

### Configuração no Código

**Arquivo:** `config.py` (linhas 33-35)

```33:35:config.py
# Configurações de API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-2.5-pro'  # Stable Pro version (June 2025) - TESTADO E FUNCIONANDO
```

### Inicialização do Serviço

**Arquivo:** `services/ai_service.py` (linhas 11-23)

```11:23:services/ai_service.py
def __init__(self):
    self.api_key = Config.GEMINI_API_KEY
    self.model_name = Config.GEMINI_MODEL
    self._configure_gemini()

def _configure_gemini(self):
    """Configura a API do Gemini"""
    if self.api_key:
        genai.configure(api_key=self.api_key)
        print(f"GEMINI_API_KEY configurada: Sim")
        print(f"GEMINI_API_KEY (primeiros 10 chars): {self.api_key[:10]}...")
    else:
        print("AVISO: GEMINI_API_KEY não configurada. A função de melhoria de descrição não estará disponível.")
```

## Tratamento de Erros e Fallback

### Estratégia de Fallback

O sistema implementa uma estratégia de **fallback gracioso**:

1. **Se a API key não estiver configurada:**
   - Retorna a descrição original sem modificações
   - Loga aviso informativo
   - Não bloqueia o processo de cadastro

2. **Se houver erro na chamada à API:**
   - Captura a exceção
   - Loga o erro completo para debug
   - Retorna a descrição original
   - Não interrompe o cadastro do curso

3. **Se a resposta da IA estiver em formato inesperado:**
   - Para `analyze_course_image`: cria resposta padrão com análise básica
   - Para `enhance_description`: retorna descrição original

### Exemplo de Tratamento de Erro

```276:289:services/course_service.py
def _enhance_description(self, course_data: Dict) -> Dict:
    """Melhora a descrição usando IA"""
    try:
        original_description = course_data.get('descricao_original', '')
        if original_description:
            enhanced_description = self.ai_service.enhance_description(original_description)
            course_data['descricao'] = enhanced_description
        else:
            course_data['descricao'] = original_description
    except Exception as e:
        print(f"Erro ao melhorar descrição: {str(e)}")
        course_data['descricao'] = course_data.get('descricao_original', '')
    
    return course_data
```

## Verificação de Disponibilidade

O serviço possui um método para verificar se está disponível:

```65:67:services/ai_service.py
def is_available(self) -> bool:
    """Verifica se o serviço de IA está disponível"""
    return bool(self.api_key)
```

## Integração no Fluxo de Criação de Curso

### Localização no Código

**Arquivo:** `services/course_service.py`

**Método:** `create_course()` (linha 19-52)

**Fluxo:**
1. Validação dos dados do formulário (linha 32)
2. Processamento dos dados (linha 37)
3. Processamento de arquivos (linha 40-41)
4. **Melhoria da descrição com IA** (linha 44) ⭐
5. Salvamento do curso (linha 47)

### Código de Integração

```19:52:services/course_service.py
def create_course(self, form_data: Dict, files: Dict = None) -> Tuple[bool, Dict, List[str]]:
    """
    Cria um novo curso
    
    Args:
        form_data: Dados do formulário
        files: Arquivos enviados (logos, etc.)
        
    Returns:
        Tuple[bool, Dict, List[str]]: (sucesso, dados_curso, erros)
    """
    try:
        # Validar dados
        is_valid, errors, warnings = self.validator.validate_course_data(form_data)
        if not is_valid:
            return False, {}, errors
        
        # Processar dados do formulário
        course_data = self._process_form_data(form_data)
        
        # Processar arquivos se fornecidos
        if files:
            self._process_uploaded_files(course_data, files)
        
        # Melhorar descrição com IA
        course_data = self._enhance_description(course_data)
        
        # Salvar curso
        saved_course = self.repository.save_course(course_data)
        
        return True, saved_course, warnings
        
    except Exception as e:
        return False, {}, [f"Erro interno: {str(e)}"]
```

## Logs e Debug

O serviço de IA produz logs detalhados para facilitar o debug:

- ✅ Confirmação de configuração da API key
- ✅ Log da descrição original antes do processamento
- ✅ Log da descrição melhorada após processamento
- ✅ Logs detalhados de erros com traceback completo
- ✅ Logs de análise de imagem (quando utilizada)

## Benefícios da Implementação

1. **Qualidade Consistente:** Descrições sempre objetivas e claras
2. **Economia de Tempo:** Usuário não precisa refinar manualmente a descrição
3. **Padronização:** Descrições seguem um padrão de formato (máximo 3 linhas)
4. **Resiliência:** Sistema continua funcionando mesmo se a IA falhar
5. **Transparência:** Logs detalhados permitem monitoramento e debug

## Considerações Importantes

### Limitações

- ⚠️ Requer conexão com internet para funcionar
- ⚠️ Depende da disponibilidade da API do Gemini
- ⚠️ Pode ter custos associados ao uso da API (dependendo do plano)
- ⚠️ Análise de imagem não está integrada no fluxo principal

### Melhores Práticas

1. **Sempre configure a API key** antes de usar em produção
2. **Monitore os logs** para identificar problemas
3. **Teste o fallback** em ambiente de desenvolvimento
4. **Considere rate limiting** para evitar abuso da API

## Próximos Passos Sugeridos

1. ✅ Integrar `analyze_course_image` no fluxo de upload de capas
2. ✅ Adicionar feedback visual ao usuário quando a IA melhorar a descrição
3. ✅ Implementar cache de descrições melhoradas para economizar chamadas à API
4. ✅ Adicionar métricas de uso da API para monitoramento

## Referências

- **Documentação Gemini API:** [Google AI Studio](https://aistudio.google.com/)
- **Biblioteca Python:** `google-generativeai`
- **Arquivo de Configuração:** `config.py`
- **Serviço Principal:** `services/ai_service.py`
- **Integração:** `services/course_service.py`

---

**Última atualização:** 2025-11-06
**Versão:** 1.1


