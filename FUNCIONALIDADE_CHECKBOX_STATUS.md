# Funcionalidade: Checkbox de Status dos Cursos

## Descrição
Esta funcionalidade adiciona checkboxes na página de listagem de cursos (`course_list`) que permitem marcar quais cursos já foram inseridos no sistema. O estado dos checkboxes é persistido mesmo após reinicializações do sistema.

## Características

### ✅ Funcionalidades Implementadas
- **Checkboxes visuais**: Cada curso na listagem possui um checkbox do lado esquerdo
- **Preenchimento verde**: Quando marcado, o checkbox fica verde com um ícone de check (✓)
- **Persistência de dados**: O estado é salvo em `course_status.json` e mantido entre sessões
- **Feedback visual**: Animações e tooltips para melhor experiência do usuário
- **Estatísticas atualizadas**: Contador de "Cursos Inseridos" na parte superior
- **API REST**: Endpoints para gerenciar o status via JavaScript

### 🎨 Design e UX
- **Animação suave**: Transições animadas ao marcar/desmarcar
- **Tooltip informativo**: Mostra o status atual ao passar o mouse
- **Loading state**: Indicador visual durante requisições
- **Feedback toast**: Notificações de sucesso/erro no canto superior direito
- **Prevenção de cliques**: Checkbox não interfere na expansão dos detalhes do curso

## Arquivos Modificados/Criados

### 📁 Novos Arquivos
- `services/course_status_service.py` - Serviço para gerenciar status dos cursos
- `course_status.json` - Arquivo de persistência (criado automaticamente)

### 📝 Arquivos Modificados
- `app.py` - Adicionadas rotas da API e integração com o serviço
- `templates/course_list.html` - Interface com checkboxes e JavaScript

## API Endpoints

### POST `/api/course/<course_id>/toggle-status`
Alterna o status de inserção de um curso.

**Resposta de sucesso:**
```json
{
    "success": true,
    "course_id": 123,
    "inserted": true,
    "message": "Curso marcado como inserido"
}
```

### GET `/api/courses/status`
Retorna o status de todos os cursos.

**Resposta:**
```json
{
    "success": true,
    "inserted_courses": [1, 3, 5, 7]
}
```

## Estrutura de Dados

### course_status.json
```json
{
  "1": true,
  "3": true,
  "5": true
}
```

## Como Usar

1. **Acessar a listagem**: Vá para `/courses` (área administrativa)
2. **Marcar curso**: Clique no checkbox à esquerda do curso
3. **Visualizar status**: 
   - ✅ Verde com check = Curso inserido
   - ⬜ Branco = Curso não inserido
4. **Ver estatísticas**: O contador "Inseridos" é atualizado automaticamente

## Benefícios

- **Controle visual**: Fácil identificação de quais cursos já foram processados
- **Persistência**: Dados mantidos mesmo com reinicializações
- **Performance**: Operações rápidas via AJAX sem recarregar a página
- **Experiência**: Interface intuitiva com feedback visual claro

## Tecnologias Utilizadas

- **Backend**: Python Flask, JSON para persistência
- **Frontend**: JavaScript vanilla, CSS3 com animações
- **API**: REST endpoints para comunicação assíncrona
- **UX**: Tooltips, animações CSS, feedback toast

## Manutenção

O arquivo `course_status.json` é criado automaticamente na primeira execução. Para resetar todos os status, simplesmente delete este arquivo.

---

**Implementado em:** Outubro 2024  
**Versão:** 1.0  
**Compatibilidade:** WebApp v4 - Ciclo Carioca