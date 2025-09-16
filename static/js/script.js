function setupRealTimeValidation() {
    const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.classList.add('error');
            } else {
                this.classList.remove('error');
            }
        });
        
        field.addEventListener('input', function() {
            if (this.classList.contains('error') && this.value.trim() !== '') {
                this.classList.remove('error');
            }
        });
    });
}

// Contador de caracteres para textareas
function setupCharacterCounters() {
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.className = 'character-counter';
            counter.textContent = `0/${maxLength}`;
            textarea.parentNode.appendChild(counter);
            
            textarea.addEventListener('input', function() {
                const currentLength = this.value.length;
                counter.textContent = `${currentLength}/${maxLength}`;
                
                if (currentLength > maxLength * 0.9) {
                    counter.style.color = '#ff6b6b';
                } else {
                    counter.style.color = '#888';
                }
            });
        }
    });
}

// Auto-save do formulário
function setupAutoSave() {
    const form = document.querySelector('.course-form');
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            localStorage.setItem('course_form_draft', JSON.stringify(data));
        });
    });
    
    // Carregar dados salvos
    const savedData = localStorage.getItem('course_form_draft');
    if (savedData) {
        const data = JSON.parse(savedData);
        Object.keys(data).forEach(key => {
            // Não carregar os campos de valor do curso, da bolsa e arquivos
            if (key !== 'valor_curso' && key !== 'valor_bolsa') {
                const field = form.querySelector(`[name="${key}"]`);
                if (field && !field.value && field.type !== 'file') {
                    field.value = data[key];
                }
            }
        });
    }
}

// Limpar flag ao submeter
function setupSubmitButton() {
    const form = document.querySelector('.course-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', function() {
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Criando Curso...';
        submitBtn.disabled = true;
    });
}

// Configurar funcionalidades específicas do formulário
function setupFormFeatures() {
    // Configurar máscaras para campos de horário
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.backgroundColor = '#333';
        });
        
        input.addEventListener('blur', function() {
            this.style.backgroundColor = '#2a2a2a';
        });
    });
    
    // Sincronizar datas quando necessário
    const inicioData = document.getElementById('inicio_inscricoes_data');
    const fimData = document.getElementById('fim_inscricoes_data');
    
    if (inicioData && fimData) {
        inicioData.addEventListener('change', function() {
            if (fimData.value < this.value) {
                fimData.value = this.value;
            }
        });
    }
}

// Validações customizadas
function setupCustomValidation() {
    const form = document.querySelector('.course-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // VALIDAÇÃO COM LOGS DETALHADOS
        console.log('=== INICIANDO VALIDAÇÃO DETALHADA ===');
        
        // Verificar campos básicos essenciais
        const camposBasicos = ['titulo', 'descricao', 'orgao', 'tema', 'modalidade', 'carga_horaria'];
        
        camposBasicos.forEach(campoName => {
            const campo = form.querySelector(`[name="${campoName}"]`);
            console.log(`Verificando campo: ${campoName}`);
            console.log(`Campo encontrado: ${!!campo}`);
            console.log(`Campo tem required: ${campo ? campo.hasAttribute('required') : 'N/A'}`);
            console.log(`Valor do campo: "${campo ? campo.value : 'N/A'}"`);
            
            if (campo && campo.hasAttribute('required')) {
                if (campo.value.trim() === '') {
                    isValid = false;
                    console.log(`❌ ERRO: ${campoName} vazio`);
                } else {
                    console.log(`✅ OK: ${campoName} = ${campo.value}`);
                }
            }
        });
        
        // Verificar radio buttons críticos
        const radioCriticos = ['curso_gratuito', 'oferece_bolsa', 'oferece_certificado', 'parceiro_externo'];
        radioCriticos.forEach(campoName => {
            console.log(`Verificando radio group: ${campoName}`);
            const group = form.querySelectorAll(`input[name="${campoName}"]`);
            console.log(`Encontrados ${group.length} radios para ${campoName}`);
            
            const algumMarcado = Array.from(group).some(radio => radio.checked);
            console.log(`Algum marcado: ${algumMarcado}`);
            
            if (!algumMarcado) {
                isValid = false;
                console.log(`❌ ERRO: ${campoName} não selecionado`);
            } else {
                const selecionado = Array.from(group).find(radio => radio.checked);
                console.log(`✅ OK: ${campoName} = ${selecionado.value}`);
            }
        });
        
        // Verificar publico_alvo separadamente (é textarea, não radio)
        console.log('Verificando publico_alvo...');
        const publicoAlvo = form.querySelector('[name="publico_alvo"]');
        console.log(`Campo publico_alvo encontrado: ${!!publicoAlvo}`);
        console.log(`Campo tem required: ${publicoAlvo ? publicoAlvo.hasAttribute('required') : 'N/A'}`);
        console.log(`Valor: "${publicoAlvo ? publicoAlvo.value : 'N/A'}"`);
        
        if (publicoAlvo && publicoAlvo.hasAttribute('required')) {
            if (publicoAlvo.value.trim() === '') {
                isValid = false;
                console.log('❌ ERRO: publico_alvo vazio');
            } else {
                console.log(`✅ OK: publico_alvo = ${publicoAlvo.value}`);
            }
        }
        
        // Validar parceiro externo se necessário
        console.log('Verificando parceiro externo...');
        const parceiroExterno = document.querySelector('input[name="parceiro_externo"]:checked');
        console.log(`Parceiro externo selecionado: ${parceiroExterno ? parceiroExterno.value : 'nenhum'}`);
        
        if (parceiroExterno && parceiroExterno.value === 'sim') {
            console.log('Parceiro externo = SIM, validando campos...');
            const parceiroNome = document.getElementById('parceiro_nome');
            const parceiroContainer = document.getElementById('parceiro_externo_container');
            
            console.log(`Container parceiro encontrado: ${!!parceiroContainer}`);
            console.log(`Container parceiro visível: ${parceiroContainer ? parceiroContainer.style.display : 'não encontrado'}`);
            console.log(`Campo nome encontrado: ${!!parceiroNome}`);
            console.log(`Nome do parceiro: "${parceiroNome ? parceiroNome.value : 'campo não encontrado'}"`);
            
            if (parceiroNome && parceiroNome.value.trim() === '') {
                isValid = false;
                console.log('❌ ERRO: Nome do parceiro vazio quando parceiro externo = sim');
            } else {
                console.log(`✅ OK: parceiro_nome = ${parceiroNome?.value}`);
            }
        } else {
            console.log('Parceiro externo = NÃO, pulando validação');
        }
        
        // Validar campos baseado na modalidade selecionada
        console.log('Verificando campos de unidades...');
        const modalidadeValue = document.getElementById('modalidade')?.value;
        console.log(`Modalidade selecionada: ${modalidadeValue}`);
        
        const unidadesContainer = document.getElementById('unidades_container');
        console.log(`Container unidades encontrado: ${!!unidadesContainer}`);
        console.log(`Container unidades visível: ${unidadesContainer ? unidadesContainer.style.display : 'não encontrado'}`);
        
        if (modalidadeValue && unidadesContainer && unidadesContainer.style.display !== 'none') {
            if (modalidadeValue === 'Online') {
                console.log('✅ Modalidade Online: campos de unidade não são obrigatórios');
            } else {
                console.log(`Modalidade ${modalidadeValue}: validando campos de unidade...`);
                
                // Validar apenas dias de aula para modalidades não-Online
                const unidades = unidadesContainer.querySelectorAll('.unidade-item');
                console.log(`Encontradas ${unidades.length} unidades`);
                
                unidades.forEach((unidade, index) => {
                    console.log(`Validando unidade ${index + 1}...`);
                    const diasCheckboxes = unidade.querySelectorAll('input[name="dias_aula[]"]');
                    console.log(`Encontrados ${diasCheckboxes.length} checkboxes de dias`);
                    
                    const algumDiaSelecionado = Array.from(diasCheckboxes).some(cb => cb.checked);
                    console.log(`Algum dia selecionado: ${algumDiaSelecionado}`);
                    
                    if (!algumDiaSelecionado) {
                        isValid = false;
                        console.log(`❌ ERRO: Unidade ${index + 1} - Nenhum dia selecionado`);
                    } else {
                        const diasSelecionados = Array.from(diasCheckboxes)
                            .filter(cb => cb.checked)
                            .map(cb => cb.value);
                        console.log(`✅ OK: Unidade ${index + 1} - Dias: ${diasSelecionados.join(', ')}`);
                    }
                });
            }
        } else {
            console.log('Container de unidades não visível ou modalidade não selecionada');
        }
        
        // Validar se fim das inscrições é posterior ao início
        const inicioData = document.getElementById('inicio_inscricoes_data');
        const inicioHora = document.getElementById('inicio_inscricoes_hora');
        const fimData = document.getElementById('fim_inscricoes_data');
        const fimHora = document.getElementById('fim_inscricoes_hora');
        
        if (inicioData && fimData && inicioData.value && fimData.value) {
            const inicioDateTime = new Date(`${inicioData.value}T${inicioHora ? inicioHora.value : '00:00'}`);
            const fimDateTime = new Date(`${fimData.value}T${fimHora ? fimHora.value : '23:59'}`);
            
            if (fimDateTime <= inicioDateTime) {
                alert('O fim das inscrições deve ser posterior ao início das inscrições.');
                isValid = false;
            }
        }
        
        if (!isValid) {
            e.preventDefault();
            // Restaurar o botão de submit se a validação falhar
            submitBtn.innerHTML = '<i class="fas fa-save"></i> Criar Curso';
            submitBtn.disabled = false;
        }
    });
}

// Função para exibir/ocultar o campo de plataforma digital
function togglePlataformaDigital() {
    const modalidade = document.getElementById('modalidade').value;
    const plataformaContainer = document.getElementById('plataforma_digital_container');
    
    if (modalidade === 'Online') {
        plataformaContainer.style.display = 'block';
    } else {
        plataformaContainer.style.display = 'none';
        document.getElementById('plataforma_digital').value = '';
    }
}

// Função para adicionar evento de clique direto no botão de submit
function setupSubmitButtonClick() {
    const form = document.querySelector('.course-form');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    submitBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Evitar validação duplicada
        if (submitBtn.disabled) return;
        
        let isValid = true;
        
        // VALIDAÇÃO COM LOGS DETALHADOS
        console.log('=== INICIANDO VALIDAÇÃO DETALHADA ===');
        
        // Verificar campos básicos essenciais
        const camposBasicos = ['titulo', 'descricao', 'orgao', 'tema', 'modalidade', 'carga_horaria'];
        
        camposBasicos.forEach(campoName => {
            const campo = form.querySelector(`[name="${campoName}"]`);
            console.log(`Verificando campo: ${campoName}`);
            console.log(`Campo encontrado: ${!!campo}`);
            console.log(`Campo tem required: ${campo ? campo.hasAttribute('required') : 'N/A'}`);
            console.log(`Valor do campo: "${campo ? campo.value : 'N/A'}"`);
            
            if (campo && campo.hasAttribute('required')) {
                if (campo.value.trim() === '') {
                    isValid = false;
                    console.log(`❌ ERRO: ${campoName} vazio`);
                } else {
                    console.log(`✅ OK: ${campoName} = ${campo.value}`);
                }
            }
        });
        
        // Verificar radio buttons críticos
        const radioCriticos = ['curso_gratuito', 'oferece_bolsa', 'oferece_certificado', 'parceiro_externo'];
        radioCriticos.forEach(campoName => {
            console.log(`Verificando radio group: ${campoName}`);
            const group = form.querySelectorAll(`input[name="${campoName}"]`);
            console.log(`Encontrados ${group.length} radios para ${campoName}`);
            
            const algumMarcado = Array.from(group).some(radio => radio.checked);
            console.log(`Algum marcado: ${algumMarcado}`);
            
            if (!algumMarcado) {
                isValid = false;
                console.log(`❌ ERRO: ${campoName} não selecionado`);
            } else {
                const selecionado = Array.from(group).find(radio => radio.checked);
                console.log(`✅ OK: ${campoName} = ${selecionado.value}`);
            }
        });
        
        // Verificar publico_alvo separadamente (é textarea, não radio)
        console.log('Verificando publico_alvo...');
        const publicoAlvo = form.querySelector('[name="publico_alvo"]');
        console.log(`Campo publico_alvo encontrado: ${!!publicoAlvo}`);
        console.log(`Campo tem required: ${publicoAlvo ? publicoAlvo.hasAttribute('required') : 'N/A'}`);
        console.log(`Valor: "${publicoAlvo ? publicoAlvo.value : 'N/A'}"`);
        
        if (publicoAlvo && publicoAlvo.hasAttribute('required')) {
            if (publicoAlvo.value.trim() === '') {
                isValid = false;
                console.log('❌ ERRO: publico_alvo vazio');
            } else {
                console.log(`✅ OK: publico_alvo = ${publicoAlvo.value}`);
            }
        }
        
        // Validar parceiro externo se necessário
        console.log('Verificando parceiro externo...');
        const parceiroExterno = document.querySelector('input[name="parceiro_externo"]:checked');
        console.log(`Parceiro externo selecionado: ${parceiroExterno ? parceiroExterno.value : 'nenhum'}`);
        
        if (parceiroExterno && parceiroExterno.value === 'sim') {
            console.log('Parceiro externo = SIM, validando campos...');
            const parceiroNome = document.getElementById('parceiro_nome');
            const parceiroContainer = document.getElementById('parceiro_externo_container');
            
            console.log(`Container parceiro encontrado: ${!!parceiroContainer}`);
            console.log(`Container parceiro visível: ${parceiroContainer ? parceiroContainer.style.display : 'não encontrado'}`);
            console.log(`Campo nome encontrado: ${!!parceiroNome}`);
            console.log(`Nome do parceiro: "${parceiroNome ? parceiroNome.value : 'campo não encontrado'}"`);
            
            if (parceiroNome && parceiroNome.value.trim() === '') {
                isValid = false;
                console.log('❌ ERRO: Nome do parceiro vazio quando parceiro externo = sim');
            } else {
                console.log(`✅ OK: parceiro_nome = ${parceiroNome?.value}`);
            }
        } else {
            console.log('Parceiro externo = NÃO, pulando validação');
        }
        
        // Validar campos baseado na modalidade selecionada
        console.log('Verificando campos de unidades...');
        const modalidadeValue = document.getElementById('modalidade')?.value;
        console.log(`Modalidade selecionada: ${modalidadeValue}`);
        
        const unidadesContainer = document.getElementById('unidades_container');
        console.log(`Container unidades encontrado: ${!!unidadesContainer}`);
        console.log(`Container unidades visível: ${unidadesContainer ? unidadesContainer.style.display : 'não encontrado'}`);
        
        if (modalidadeValue && unidadesContainer && unidadesContainer.style.display !== 'none') {
            if (modalidadeValue === 'Online') {
                console.log('✅ Modalidade Online: campos de unidade não são obrigatórios');
            } else {
                console.log(`Modalidade ${modalidadeValue}: validando campos de unidade...`);
                
                // Validar apenas dias de aula para modalidades não-Online
                const unidades = unidadesContainer.querySelectorAll('.unidade-item');
                console.log(`Encontradas ${unidades.length} unidades`);
                
                unidades.forEach((unidade, index) => {
                    console.log(`Validando unidade ${index + 1}...`);
                    const diasCheckboxes = unidade.querySelectorAll('input[name="dias_aula[]"]');
                    console.log(`Encontrados ${diasCheckboxes.length} checkboxes de dias`);
                    
                    const algumDiaSelecionado = Array.from(diasCheckboxes).some(cb => cb.checked);
                    console.log(`Algum dia selecionado: ${algumDiaSelecionado}`);
                    
                    if (!algumDiaSelecionado) {
                        isValid = false;
                        console.log(`❌ ERRO: Unidade ${index + 1} - Nenhum dia selecionado`);
                    } else {
                        const diasSelecionados = Array.from(diasCheckboxes)
                            .filter(cb => cb.checked)
                            .map(cb => cb.value);
                        console.log(`✅ OK: Unidade ${index + 1} - Dias: ${diasSelecionados.join(', ')}`);
                    }
                });
            }
        } else {
            console.log('Container de unidades não visível ou modalidade não selecionada');
        }
        
        // Validar se fim das inscrições é posterior ao início
        const inicioData = document.getElementById('inicio_inscricoes_data');
        const inicioHora = document.getElementById('inicio_inscricoes_hora');
        const fimData = document.getElementById('fim_inscricoes_data');
        const fimHora = document.getElementById('fim_inscricoes_hora');
        
        if (inicioData && fimData && inicioData.value && fimData.value) {
            const inicioDateTime = new Date(`${inicioData.value}T${inicioHora ? inicioHora.value : '00:00'}`);
            const fimDateTime = new Date(`${fimData.value}T${fimHora ? fimHora.value : '23:59'}`);
            
            if (fimDateTime <= inicioDateTime) {
                alert('O fim das inscrições deve ser posterior ao início das inscrições.');
                isValid = false;
            }
        }
        
        console.log('Validação concluída. Válido:', isValid);
        
        if (isValid) {
            // Se o formulário for válido, mostrar animação de loading e enviar
            console.log('Formulário válido, enviando...');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Criando Curso...';
            submitBtn.disabled = true;
            
            // Debug: verificar dados do formulário
            const formData = new FormData(form);
            console.log('Dados do formulário:');
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }
            
            form.submit();
        } else {
            // Exibir mensagem de erro
            console.log('Formulário inválido, não enviando...');
            alert('Por favor, preencha todos os campos obrigatórios visíveis.');
        }
    });
}

// Função auxiliar para verificar se um campo está visível
function isFieldVisible(field) {
    // Verificar se o próprio campo está visível
    if (window.getComputedStyle(field).display === 'none') return false;
    
    // Verificar se algum container pai está oculto
    let parent = field.parentElement;
    while (parent && parent !== document) {
        if (window.getComputedStyle(parent).display === 'none') return false;
        parent = parent.parentElement;
    }
    
    return true;
}

// Função para formatar valores monetários
function formatarValor(input) {
    // Remove todos os caracteres não numéricos
    let valor = input.value.replace(/\D/g, '');
    
    // Converte para número e divide por 100 para obter o valor em reais
    valor = (parseInt(valor) || 0) / 100;
    
    // Formata o valor como moeda brasileira
    input.value = valor.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
}

// Adiciona evento de blur para garantir formatação ao sair do campo
document.addEventListener('DOMContentLoaded', function() {
    const camposValor = document.querySelectorAll('#valor_curso, #valor_bolsa');
    
    camposValor.forEach(campo => {
        campo.addEventListener('blur', function() {
            if (this.value === '') return;
            
            // Remove qualquer caractere que não seja número ou vírgula
            let valor = this.value.replace(/[^0-9,]/g, '');
            
            // Trata o caso onde há mais de uma vírgula
            if (valor.split(',').length > 2) {
                const partes = valor.split(',');
                valor = partes[0] + ',' + partes.slice(1).join('');
            }
            
            // Verifica se o valor tem vírgula
            if (!valor.includes(',')) {
                // Se não tem vírgula, adiciona ,00 no final
                valor = valor + ',00';
            } else {
                // Se tem vírgula, garante que tenha 2 casas decimais
                const partes = valor.split(',');
                const inteiro = partes[0] || '0';
                let decimal = partes[1] || '00';
                
                // Limita a 2 casas decimais
                if (decimal.length > 2) {
                    decimal = decimal.substring(0, 2);
                } else if (decimal.length === 1) {
                    decimal = decimal + '0';
                } else if (decimal.length === 0) {
                    decimal = '00';
                }
                
                valor = inteiro + ',' + decimal;
            }
            
            this.value = valor;
        });
    });
});

// Função para exibir/ocultar campos de unidades com base na modalidade selecionada
function toggleUnidades() {
    const modalidade = document.getElementById('modalidade').value;
    const unidadesContainer = document.getElementById('unidades_container');
    const unidadesList = document.getElementById('unidades_list');
    
    if (modalidade === 'Presencial' || modalidade === 'Híbrido' || modalidade === 'Online') {
        unidadesContainer.style.display = 'block';
        
        // Atualizar todas as unidades existentes
        const unidades = unidadesList.querySelectorAll('.unidade-item');
        unidades.forEach((unidade, index) => {
            const legend = unidade.querySelector('legend');
            const enderecoInputs = unidade.querySelectorAll('input[name="endereco_unidade[]"], input[name="bairro_unidade[]"]');
            const enderecoLabels = unidade.querySelectorAll('label');
        
        // Tratamento específico para modalidade Online
        if (modalidade === 'Online') {
            // Altera o título para "Informações do Curso"
                if (legend) {
                    legend.textContent = `Informações do Curso ${index + 1}`;
                    legend.style.fontSize = '1.2em';
            }
            
            // Oculta campos de endereço e bairro para modalidade Online
                enderecoInputs.forEach(field => {
                field.style.display = 'none';
                field.removeAttribute('required');
            });
            
                // Oculta labels de endereço e bairro
                enderecoLabels.forEach(label => {
                    if (label.textContent.includes('Endereço') || label.textContent.includes('Bairro')) {
                        label.style.display = 'none';
                    }
                });
                
        } else {
            // Para Presencial e Híbrido, mostra todos os campos e restaura o título original
                if (legend) {
                    legend.textContent = `Informações da Unidade ${index + 1}`;
                    legend.style.fontSize = '1.2em';
                }
                
                enderecoInputs.forEach(field => {
                field.style.display = '';
                    field.setAttribute('required', 'required');
                });
                
                // Mostra todas as labels
                enderecoLabels.forEach(label => {
                    label.style.display = '';
                });
            }
        });
        
    } else {
        unidadesContainer.style.display = 'none';
        // Remove o atributo required de todos os campos dentro do container de unidades
        document.querySelectorAll('#unidades_container input, #unidades_container select').forEach(field => {
            field.removeAttribute('required');
        });
    }
}

// Função para exibir/ocultar campo de informações adicionais do curso
function toggleInfoAdicionais(mostrar) {
    const infoAdicionaisContainer = document.getElementById('info_adicionais_container');
    const infoAdicionaisField = document.getElementById('info_adicionais');
    
    if (mostrar) {
        infoAdicionaisContainer.style.display = 'block';
        infoAdicionaisField.setAttribute('required', 'required');
    } else {
        infoAdicionaisContainer.style.display = 'none';
        infoAdicionaisField.removeAttribute('required');
        infoAdicionaisField.value = '';
    }
}

// Função para adicionar nova unidade
function addUnidade() {
    const unidadesContainer = document.getElementById('unidades_list');
    const unidadeCount = unidadesContainer.children.length + 1;
    
    const unidadeDiv = document.createElement('div');
    unidadeDiv.className = 'unidade-item';
    unidadeDiv.setAttribute('data-unidade', unidadeCount - 1);
    
    // Verificar se é modalidade Online para ajustar campos
    const modalidade = document.getElementById('modalidade').value;
    const isOnline = modalidade === 'Online';
    
    unidadeDiv.innerHTML = `
        <fieldset class="unidade-fieldset">
            <legend>Informações da Unidade ${unidadeCount}</legend>
            <label>Endereço da unidade*</label>
            <input type="text" name="endereco_unidade[]" ${isOnline ? 'style="display:none;"' : 'required'}>
            <label>Bairro*</label>
            <input type="text" name="bairro_unidade[]" ${isOnline ? 'style="display:none;"' : 'required'}>
            <label>Número de vagas*</label>
            <input type="number" name="vagas_unidade[]" min="1" required>
            <div class="data-group">
                <div class="data-field">
                    <label>Início das aulas*</label>
                    <input type="date" name="inicio_aulas_data[]" required>
                </div>
                <div class="data-field">
                    <label>Fim das aulas*</label>
                    <input type="date" name="fim_aulas_data[]" required>
                </div>
            </div>
            <div class="horario-group">
                <div class="horario-field">
                    <label>Horário-Início*</label>
                    <select name="horario_inicio[]" required>
                        <option value="">Selecione o horário</option>
                        <option value="06:00">06:00</option>
                        <option value="07:00">07:00</option>
                        <option value="08:00">08:00</option>
                        <option value="09:00">09:00</option>
                        <option value="10:00">10:00</option>
                        <option value="11:00">11:00</option>
                        <option value="12:00">12:00</option>
                        <option value="13:00">13:00</option>
                        <option value="14:00">14:00</option>
                        <option value="15:00">15:00</option>
                        <option value="16:00">16:00</option>
                        <option value="17:00">17:00</option>
                        <option value="18:00">18:00</option>
                        <option value="19:00">19:00</option>
                        <option value="20:00">20:00</option>
                        <option value="21:00">21:00</option>
                        <option value="22:00">22:00</option>
                        <option value="23:00">23:00</option>
                    </select>
                </div>
                <div class="horario-field">
                    <label>Horário-Fim*</label>
                    <select name="horario_fim[]" required>
                        <option value="">Selecione o horário</option>
                        <option value="06:00">06:00</option>
                        <option value="07:00">07:00</option>
                        <option value="08:00">08:00</option>
                        <option value="09:00">09:00</option>
                        <option value="10:00">10:00</option>
                        <option value="11:00">11:00</option>
                        <option value="12:00">12:00</option>
                        <option value="13:00">13:00</option>
                        <option value="14:00">14:00</option>
                        <option value="15:00">15:00</option>
                        <option value="16:00">16:00</option>
                        <option value="17:00">17:00</option>
                        <option value="18:00">18:00</option>
                        <option value="19:00">19:00</option>
                        <option value="20:00">20:00</option>
                        <option value="21:00">21:00</option>
                        <option value="22:00">22:00</option>
                        <option value="23:00">23:00</option>
                    </select>
                </div>
        </div>
            <label>Dias de aula*</label>
            <div class="checkbox-group dias-aula">
                <label class="checkbox-label">
                    <input type="checkbox" name="dias_aula[]" value="Segunda-feira">
                    <span>Segunda-feira</span>
                </label>
                <label class="checkbox-label">
                    <input type="checkbox" name="dias_aula[]" value="Terça-feira">
                    <span>Terça-feira</span>
                </label>
                <label class="checkbox-label">
                    <input type="checkbox" name="dias_aula[]" value="Quarta-feira">
                    <span>Quarta-feira</span>
                </label>
                <label class="checkbox-label">
                    <input type="checkbox" name="dias_aula[]" value="Quinta-feira">
                    <span>Quinta-feira</span>
                </label>
                <label class="checkbox-label">
                    <input type="checkbox" name="dias_aula[]" value="Sexta-feira">
                    <span>Sexta-feira</span>
                </label>
                <label class="checkbox-label">
                    <input type="checkbox" name="dias_aula[]" value="Sábado">
                    <span>Sábado</span>
                </label>
                <label class="checkbox-label">
                    <input type="checkbox" name="dias_aula[]" value="Domingo">
                    <span>Domingo</span>
                </label>
        </div>
        </fieldset>
    `;
    
    unidadesContainer.appendChild(unidadeDiv);
    
    // Adicionar validação aos novos checkboxes de dias
    const novosCheckboxes = unidadeDiv.querySelectorAll('input[name="dias_aula[]"]');
    novosCheckboxes.forEach(cb => {
        cb.addEventListener('change', validateDiasAula);
    });
    
    // Scroll suave para a nova unidade
    unidadeDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    setupRealTimeValidation();
    setupCharacterCounters();
    setupAutoSave();
    // Função setupPageLeaveConfirmation() foi removida para evitar o popup de confirmação ao sair da página
    setupSubmitButton();
    setupFormFeatures();
    setupCustomValidation();
    setupSubmitButtonClick(); // Adicionar nova função
    // Configurar exibição dinâmica das unidades
    const modalidadeSelect = document.getElementById('modalidade');
    if (modalidadeSelect) {
        toggleUnidades();
        modalidadeSelect.addEventListener('change', toggleUnidades);
    }
    
    console.log('WebApp v3 - Formulário inicializado com sucesso!');
});