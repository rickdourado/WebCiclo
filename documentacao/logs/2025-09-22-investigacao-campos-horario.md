# Changelog - 22 de Setembro de 2025 - Investigação dos Campos de Horário

## 🐛 Problema Identificado: Campos de Horário Não Chegam no Backend

### **Descrição do Problema**
Após a correção da função `garantirCamposAssincronos`, o usuário reportou que os campos de horário ainda não estão chegando no backend, mesmo quando preenchidos no frontend.

### **Log de Erro:**
```
2025-09-22 14:47:47,393: Iniciando criação de curso
2025-09-22 14:47:47,405: Falha na criação do curso: [
  "Campo 'Horario Inicio' é obrigatório para aulas síncronas online",
  "Campo 'Horario Fim' é obrigatório para aulas síncronas online"
]
```

### **Análise do Problema**
O usuário estava correto ao dizer que é "uma questão de validação" e que "os dados foram preenchidos, porém o sistema não interpreta como tivessem sido".

---

## 🔍 Investigação Realizada

### **1. Verificação dos Nomes dos Campos**
✅ **Campos definidos corretamente:**
```html
<select id="horario_inicio_online" name="horario_inicio[]">
<select id="horario_fim_online" name="horario_fim[]">
```

### **2. Verificação do Container**
❌ **PROBLEMA IDENTIFICADO:**
```html
<div id="horarios_detalhados_online_container" style="display: none;">
```

**Causa Raiz:** O container `horarios_detalhados_online_container` está inicializado com `style="display: none;"`, e quando um elemento tem `display: none`, **ele não é enviado no formulário HTML**!

### **3. Fluxo Problemático Identificado**
1. **Página carrega:** Container com `display: none`
2. **Usuário muda para "NÃO":** `toggleAulasAssincronas(false)` é chamada
3. **Container é mostrado:** `horariosContainer.style.display = 'block'`
4. **Usuário preenche campos:** Valores são inseridos nos selects
5. **Múltiplas chamadas:** `garantirCamposAssincronos()` é chamada várias vezes
6. **Problema:** Container pode ser ocultado novamente ou campos não ficarem obrigatórios
7. **Resultado:** Campos não são enviados no formulário

---

## 🛠️ Solução Implementada

### **Logs de Debug Adicionados**

**Arquivo:** `templates/index.html`

#### 1. Logs na Função `toggleAulasAssincronas`:
```javascript
function toggleAulasAssincronas(isAssincronas) {
    const horariosContainer = document.getElementById('horarios_detalhados_online_container');
    const horariosOnlineContainer = document.getElementById('horarios_online_container');
    
    console.log('toggleAulasAssincronas chamada com isAssincronas:', isAssincronas);
    console.log('horariosContainer encontrado:', !!horariosContainer);
    console.log('horariosOnlineContainer encontrado:', !!horariosOnlineContainer);
    
    if (horariosContainer && horariosOnlineContainer) {
        if (isAssincronas) {
            // Aulas assíncronas - ocultar campos de horário e dias
            horariosContainer.style.display = 'none';
            horariosOnlineContainer.style.display = 'none';
            console.log('Campos ocultos para aulas assíncronas');
        } else {
            // Aulas síncronas - mostrar campos de horário e dias
            horariosContainer.style.display = 'block';
            horariosOnlineContainer.style.display = 'block';
            console.log('Campos mostrados para aulas síncronas');
            console.log('horariosContainer.style.display:', horariosContainer.style.display);
            console.log('horariosOnlineContainer.style.display:', horariosOnlineContainer.style.display);
            
            // Adicionar required aos campos visíveis
            const camposHorario = [
                document.getElementById('horario_inicio_online'),
                document.getElementById('horario_fim_online')
            ];
            
            camposHorario.forEach(campo => {
                if (campo) {
                    campo.setAttribute('required', 'required');
                    console.log('Campo marcado como required:', campo.name, campo.value);
                }
            });
        }
    }
}
```

#### 2. Logs na Função `garantirCamposAssincronos`:
```javascript
function garantirCamposAssincronos() {
    const aulasAssincronasSim = document.querySelector('input[name="aulas_assincronas"][value="sim"]');
    const aulasAssincronasNao = document.querySelector('input[name="aulas_assincronas"][value="nao"]');
    const horarioInicioOnline = document.getElementById('horario_inicio_online');
    const horarioFimOnline = document.getElementById('horario_fim_online');
    
    console.log('garantirCamposAssincronos chamada');
    console.log('aulasAssincronasSim checked:', aulasAssincronasSim ? aulasAssincronasSim.checked : 'não encontrado');
    console.log('aulasAssincronasNao checked:', aulasAssincronasNao ? aulasAssincronasNao.checked : 'não encontrado');
    
    if (aulasAssincronasSim && aulasAssincronasSim.checked) {
        // SIM está marcado - garantir que campos de horário não sejam obrigatórios
        if (horarioInicioOnline) horarioInicioOnline.removeAttribute('required');
        if (horarioFimOnline) horarioFimOnline.removeAttribute('required');
        
        // Garantir que containers estejam ocultos
        const horariosContainer = document.getElementById('horarios_detalhados_online_container');
        const horariosOnlineContainer = document.getElementById('horarios_online_container');
        if (horariosContainer) horariosContainer.style.display = 'none';
        if (horariosOnlineContainer) horariosOnlineContainer.style.display = 'none';
        console.log('Campos ocultos por garantirCamposAssincronos (SIM)');
    } else if (aulasAssincronasNao && aulasAssincronasNao.checked) {
        // NÃO está marcado - garantir que campos de horário sejam obrigatórios e visíveis
        if (horarioInicioOnline) horarioInicioOnline.setAttribute('required', 'required');
        if (horarioFimOnline) horarioFimOnline.setAttribute('required', 'required');
        
        // Garantir que containers estejam visíveis
        const horariosContainer = document.getElementById('horarios_detalhados_online_container');
        const horariosOnlineContainer = document.getElementById('horarios_online_container');
        if (horariosContainer) horariosContainer.style.display = 'block';
        if (horariosOnlineContainer) horariosOnlineContainer.style.display = 'block';
        console.log('Campos mostrados por garantirCamposAssincronos (NÃO)');
        console.log('horariosContainer.style.display:', horariosContainer ? horariosContainer.style.display : 'não encontrado');
        console.log('horariosOnlineContainer.style.display:', horariosOnlineContainer ? horariosOnlineContainer.style.display : 'não encontrado');
    }
}
```

#### 3. Função de Verificação Antes do Envio:
```javascript
function verificarEstadoCampos() {
    const aulasAssincronasNao = document.querySelector('input[name="aulas_assincronas"][value="nao"]');
    const horariosContainer = document.getElementById('horarios_detalhados_online_container');
    const horarioInicioOnline = document.getElementById('horario_inicio_online');
    const horarioFimOnline = document.getElementById('horario_fim_online');
    
    console.log('=== VERIFICAÇÃO ANTES DO ENVIO ===');
    console.log('aulas_assincronas = nao:', aulasAssincronasNao ? aulasAssincronasNao.checked : 'não encontrado');
    console.log('horariosContainer encontrado:', !!horariosContainer);
    console.log('horariosContainer.style.display:', horariosContainer ? horariosContainer.style.display : 'não encontrado');
    console.log('horarioInicioOnline encontrado:', !!horarioInicioOnline);
    console.log('horarioInicioOnline.value:', horarioInicioOnline ? horarioInicioOnline.value : 'não encontrado');
    console.log('horarioFimOnline encontrado:', horarioFimOnline ? horarioFimOnline.value : 'não encontrado');
    console.log('================================');
}
```

#### 4. Event Listener para Verificação:
```javascript
// Verificar estado dos campos antes do envio do formulário
const form = document.querySelector('form');
if (form) {
    form.addEventListener('submit', function(e) {
        verificarEstadoCampos();
    });
}
```

---

## 🎯 Objetivo dos Logs

### **Para Identificar:**
1. **Estado dos containers:** Se estão visíveis ou ocultos
2. **Valores dos campos:** Se estão preenchidos corretamente
3. **Chamadas das funções:** Quando e como são executadas
4. **Conflitos entre funções:** Se uma função está sobrescrevendo a outra
5. **Timing das operações:** Se há problemas de sincronização

### **Para Rastrear:**
1. **Fluxo completo:** Desde a mudança até o envio
2. **Múltiplas chamadas:** Se `garantirCamposAssincronos` está sendo chamada várias vezes
3. **Estado inconsistente:** Se containers ficam ocultos após serem mostrados
4. **Valores perdidos:** Se campos são limpos inadvertidamente

---

## 🧪 Cenários de Teste com Logs

### **Cenário 1: Curso Online Síncrono (Primeira Tentativa)**
1. **Modalidade:** Online
2. **Aulas Assíncronas:** NÃO
3. **Preenchimento:** Horários preenchidos
4. **Envio:** Clicar em "Criar Curso"
5. **Logs esperados:**
   - `toggleAulasAssincronas chamada com isAssincronas: false`
   - `Campos mostrados para aulas síncronas`
   - `horariosContainer.style.display: block`
   - `Campo marcado como required: horario_inicio[] [valor]`
   - `Campo marcado como required: horario_fim[] [valor]`
   - `garantirCamposAssincronos chamada`
   - `aulasAssincronasNao checked: true`
   - `Campos mostrados por garantirCamposAssincronos (NÃO)`
   - `=== VERIFICAÇÃO ANTES DO ENVIO ===`
   - `horariosContainer.style.display: block`
   - `horarioInicioOnline.value: [valor]`
   - `horarioFimOnline.value: [valor]`

### **Cenário 2: Múltiplas Chamadas da Função**
1. **Inicialização:** `garantirCamposAssincronos()` chamada múltiplas vezes
2. **Estado:** Aulas Síncronas (NÃO)
3. **Logs esperados:**
   - Múltiplas chamadas de `garantirCamposAssincronos`
   - `aulasAssincronasNao checked: true` em todas as chamadas
   - `Campos mostrados por garantirCamposAssincronos (NÃO)` em todas as chamadas
   - `horariosContainer.style.display: block` consistente

### **Cenário 3: Conflito Entre Funções**
1. **`toggleAulasAssincronas(false)`:** Mostra campos
2. **`garantirCamposAssincronos()`:** Pode ocultar campos
3. **Logs esperados:**
   - `Campos mostrados para aulas síncronas`
   - `horariosContainer.style.display: block`
   - `garantirCamposAssincronos chamada`
   - `Campos mostrados por garantirCamposAssincronos (NÃO)`
   - `horariosContainer.style.display: block` (deve permanecer)

---

## 📊 Informações que os Logs Vão Revelar

### **Se o Problema é de Visibilidade:**
- `horariosContainer.style.display: none` = Container oculto
- `horariosContainer.style.display: block` = Container visível

### **Se o Problema é de Valores:**
- `horarioInicioOnline.value: ""` = Campo vazio
- `horarioInicioOnline.value: "08:00"` = Campo preenchido

### **Se o Problema é de Conflito:**
- Múltiplas chamadas de `garantirCamposAssincronos`
- `Campos ocultos por garantirCamposAssincronos (SIM)` após `Campos mostrados para aulas síncronas`

### **Se o Problema é de Timing:**
- `garantirCamposAssincronos chamada` antes de `toggleAulasAssincronas`
- `horariosContainer.style.display: none` após `horariosContainer.style.display: block`

---

## 🚀 Próximos Passos

### **Com os Logs Implementados:**
1. **Testar** criação de curso online síncrono
2. **Analisar** logs no console do navegador
3. **Identificar** onde está o problema específico
4. **Corrigir** baseado nas informações dos logs

### **Possíveis Correções Baseadas nos Logs:**
1. **Se container fica oculto:** Ajustar ordem das chamadas
2. **Se valores são perdidos:** Corrigir lógica de limpeza
3. **Se há conflito:** Sincronizar funções
4. **Se há timing:** Ajustar delays e sequência

---

## ✅ Status Final

**Status:** 🔍 **Logs de debug implementados para investigação**
**Próximo passo:** Testar e analisar logs para identificar problema específico
**Cobertura:** Todas as funções relevantes têm logs detalhados
**Objetivo:** Identificar exatamente onde e por que os campos não chegam no backend

---

*Esta investigação implementou logs abrangentes para rastrear todo o fluxo dos campos de horário, desde a inicialização até o envio do formulário, permitindo identificar exatamente onde está o problema que impede os campos de chegarem no backend.*
