# Regras do Projeto - WebCiclo (Ciclo Carioca)

## 1. Regras Fundamentais (SEMPRE)

1.  **SEMPRE** Execute um comando no terminal por vez, ao invés de utilizar `&&`, para evitar erros.
2.  **SEMPRE** Utilize o `uv` como principal comando, evitando o uso de `pip`.
3.  **SEMPRE** ative o ambiente virtual correto: `source .venv/bin/activate`.
    - _Nota: Se instruído anteriormente, usar `conda activate ciclo`, mas priorizar venv local se disponível._
4.  **SEMPRE** seguir a estrutura de arquivos e convenções de nomenclatura definidas.
5.  **SEMPRE** unifique os changelogs usando primeiramente o dia em que foram feitos (padrão `AAAA-MM-DD.md`) na pasta `documentacao/logs`.
6.  **SEMPRE** delete scripts temporários criados para tarefas pontuais após o uso.
7.  **SEMPRE** coloque arquivos de documentação na pasta `documentacao`.
8.  **SEMPRE** priorize a **confiabilidade**, **usabilidade** e **acessibilidade**.

## 2. Contexto e Arquitetura

**WebApp v4 - Ciclo Carioca** é um sistema de gerenciamento de cursos para a Prefeitura do Rio de Janeiro.

### Padrões de Código Python/Flask (v3.13+)

- Use **type hints** sempre que possível.
- Docstrings no formato Google Style.
- Tratamento de exceções com logs detalhados.
- Separação clara entre camadas: `Service` → `Repository` → `Scripts`.
- Use f-strings para formatação.
- Organização de imports: Stdlib → Third-party → Local.

### Frontend

- **Templates:** Jinja2 com escape automático.
- **CSS:** Grid e Flexbox, variáveis CSS, semântica BEM quando apropriado.
- **JS:** Vanilla JavaScript (sem jQuery).
- **UX:** Feedback visual para ações, loading states, mensagens de erro claras, tooltips.

## 3. Diretrizes de Desenvolvimento

### Validação e Segurança

- Validar **SEMPRE** dados de entrada.
- Sanitizar uploads de arquivos.
- Usar proteção CSRF em formulários.
- Logs detalhados para debugging.

### Performance

- Lazy loading para listas grandes.
- Compressão automática de imagens.
- Minimizar requisições desnecessárias.

### Funcionalidades Específicas

- **Cursos:** Modalidades (Presencial, Online, Híbrido), múltiplas unidades, persistência híbrida (MySQL + CSV/PDF).
- **Arquivos Gerados:** CSV para importação, PDF para impressão.
- **Integração IA (Gemini):** Enriquecimento de descrições de cursos com fallback seguro e rate limiting.

## 4. Debugging e Manutenção

### Logs Importantes

Monitorar logs de:

- Criação/edição de cursos.
- Uploads de arquivos.
- Erros de validação.
- Operações de IA.

### Deployment (PythonAnywhere)

- Configuração via WSGI.
- Middleware para tratamento de requests.
- Verificação de host.

---

_Este documento serve como guia de referência rápida. Para detalhes completos, consulte a documentação original em `.kiro/steering/regraskiro.md`._
