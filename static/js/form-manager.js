// form-manager.js
// Gerenciador de formulários dinâmicos

class FormManager {
    constructor() {
        this.setupEventListeners();
        this.initializeForm();
    }
    
    setupEventListeners() {
        // Event listener para modalidade
        const modalidadeSelect = document.getElementById('modalidade');
        if (modalidadeSelect) {
            modalidadeSelect.addEventListener('change', () => this.toggleUnidades());
        }
        
        // Event listeners para botões de adicionar/remover
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-unidade-btn')) {
                e.preventDefault();
                this.addUnidade();
            }
            
            if (e.target.classList.contains('remove-unidade-btn')) {
                e.preventDefault();
                this.removeUnidade(e.target);
            }
            
            if (e.target.classList.contains('add-plataforma-btn')) {
                e.preventDefault();
                this.addPlataforma();
            }
            
            if (e.target.classList.contains('remove-plataforma-btn')) {
                e.preventDefault();
                this.removePlataforma(e.target);
            }
        });
        
        // Event listeners para campos condicionais
        this.setupConditionalFields();
    }
    
    initializeForm() {
        // Definir data atual para campos de data
        this.setCurrentDate();
        
        // Configurar campos de valor monetário
        this.setupCurrencyFields();
        
        // Inicializar campos de aulas assíncronas
        this.initializeAsyncFields();
    }
    
    setCurrentDate() {
        const hoje = new Date();
        const ano = hoje.getFullYear();
        const mes = String(hoje.getMonth() + 1).padStart(2, '0');
        const dia = String(hoje.getDate()).padStart(2, '0');
        const dataAtual = `${ano}-${mes}-${dia}`;
        
        const inicioData = document.getElementById('inicio_inscricoes_data');
        const fimData = document.getElementById('fim_inscricoes_data');
        
        if (inicioData) inicioData.value = dataAtual;
        if (fimData) fimData.value = dataAtual;
    }
    
    setupCurrencyFields() {
        const camposValor = document.querySelectorAll('#valor_curso, #valor_bolsa');
        
        camposValor.forEach(campo => {
            campo.addEventListener('blur', () => {
                if (campo.value === '') return;
                
                // Remove qualquer caractere que não seja número ou vírgula
                let valor = campo.value.replace(/[^0-9,]/g, '');
                
                // Trata o caso onde há mais de uma vírgula
                if (valor.split(',').length > 2) {
                    const partes = valor.split(',');
                    valor = partes[0] + ',' + partes.slice(1).join('');
                }
                
                // Verifica se o valor tem vírgula
                if (!valor.includes(',')) {
                    valor = valor + ',00';
                } else {
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
                
                campo.value = valor;
            });
        });
    }
    
    initializeAsyncFields() {
        // Inicializar campo de aulas assíncronas como "SIM"
        const aulasAssincronasSim = document.querySelector('input[name="aulas_assincronas"][value="sim"]');
        if (aulasAssincronasSim) {
            aulasAssincronasSim.checked = true;
            this.toggleAulasAssincronas(true);
        }
        
        // Inicializar campos de plataforma digital se modalidade for Online
        const modalidadeSelect = document.getElementById('modalidade');
        if (modalidadeSelect && modalidadeSelect.value === 'Online') {
            this.togglePlataformaDigital();
        }
    }
    
    setupConditionalFields() {
        // Campo de plataforma digital
        const modalidadeSelect = document.getElementById('modalidade');
        if (modalidadeSelect) {
            modalidadeSelect.addEventListener('change', () => this.togglePlataformaDigital());
        }
        
        // Campo de aulas assíncronas
        const aulasAssincronasRadios = document.querySelectorAll('input[name="aulas_assincronas"]');
        aulasAssincronasRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                this.toggleAulasAssincronas(radio.value === 'sim');
            });
        });
    }
    
    toggleUnidades() {
        const modalidadeSelect = document.getElementById('modalidade');
        if (!modalidadeSelect) return;
        
        const modalidade = modalidadeSelect.value;
        const unidadesContainer = document.getElementById('unidades_container');
        const plataformaContainer = document.getElementById('plataforma_container');
        
        // Verificar se há dados de duplicação (unidades já renderizadas pelo servidor)
        const unidadesList = document.getElementById('unidades_list');
        const hasPreRenderedUnits = unidadesList && unidadesList.querySelectorAll('.unidade-item').length > 1;
        
        if (modalidade === 'Presencial' || modalidade === 'Híbrido') {
            // Para Presencial e Híbrido: mostrar apenas unidades
            if (unidadesContainer) {
                unidadesContainer.style.display = 'block';
                this.setFieldsRequired(unidadesContainer, true);
            }
            if (plataformaContainer) {
                plataformaContainer.style.display = 'none';
                this.setFieldsRequired(plataformaContainer, false);
            }
            
            // Só atualizar unidades existentes se não há unidades pré-renderizadas
            if (!hasPreRenderedUnits) {
                this.updateExistingUnits(modalidade);
            }
        } else if (modalidade === 'Online') {
            // Para Online: mostrar apenas plataforma
            if (unidadesContainer) {
                unidadesContainer.style.display = 'none';
                this.setFieldsRequired(unidadesContainer, false);
            }
            if (plataformaContainer) {
                plataformaContainer.style.display = 'block';
                this.setFieldsRequired(plataformaContainer, true);
            }
        } else {
            // Para outras modalidades: ocultar ambos
            if (unidadesContainer) {
                unidadesContainer.style.display = 'none';
                this.setFieldsRequired(unidadesContainer, false);
            }
            if (plataformaContainer) {
                plataformaContainer.style.display = 'none';
                this.setFieldsRequired(plataformaContainer, false);
            }
        }
    }
    
    updateExistingUnits(modalidade) {
        const unidadesList = document.getElementById('unidades_list');
        if (!unidadesList) return;
        
        const unidades = unidadesList.querySelectorAll('.unidade-item');
        
        unidades.forEach((unidade, index) => {
            const legend = unidade.querySelector('legend');
            const enderecoInputs = unidade.querySelectorAll('input[name="endereco_unidade[]"], input[name="bairro_unidade[]"]');
            const enderecoLabels = unidade.querySelectorAll('label');
            
            if (modalidade === 'Online') {
                if (legend) {
                    legend.textContent = `Informações do Curso ${index + 1}`;
                }
                
                enderecoInputs.forEach(field => {
                    field.style.display = 'none';
                    field.removeAttribute('required');
                });
                
                enderecoLabels.forEach(label => {
                    if (label.textContent.includes('Endereço') || label.textContent.includes('Bairro')) {
                        label.style.display = 'none';
                    }
                });
            } else {
                if (legend) {
                    legend.textContent = `Informações da Unidade ou Turma ${index + 1}`;
                }
                
                enderecoInputs.forEach(field => {
                    field.style.display = '';
                    field.setAttribute('required', 'required');
                });
                
                enderecoLabels.forEach(label => {
                    label.style.display = '';
                });
            }
        });
    }
    
    togglePlataformaDigital() {
        const modalidadeSelect = document.getElementById('modalidade');
        if (!modalidadeSelect) return;
        
        const modalidade = modalidadeSelect.value;
        const plataformaContainer = document.getElementById('plataforma_digital_container');
        const plataformaDigitalField = document.getElementById('plataforma_digital');
        
        if (plataformaContainer) {
            if (modalidade === 'Online') {
                plataformaContainer.style.display = 'block';
            } else {
                plataformaContainer.style.display = 'none';
                if (plataformaDigitalField) {
                    plataformaDigitalField.value = '';
                }
            }
        }
    }
    
    toggleAulasAssincronas(isAsync) {
        // Tratar containers principais
        const horariosContainer = document.getElementById('horarios_detalhados_online_container');
        const horariosOnlineContainer = document.getElementById('horarios_online_container');
        
        if (horariosContainer && horariosOnlineContainer) {
            if (isAsync) {
                horariosContainer.style.display = 'none';
                horariosOnlineContainer.style.display = 'none';
                
                // Remover required dos campos ocultos
                this.setFieldsRequired(horariosContainer, false);
                this.setFieldsRequired(horariosOnlineContainer, false);
            } else {
                horariosContainer.style.display = 'block';
                horariosOnlineContainer.style.display = 'block';
                
                // Adicionar required aos campos visíveis
                this.setFieldsRequired(horariosContainer, true);
                this.setFieldsRequired(horariosOnlineContainer, true);
            }
        }
        
        // Tratar containers criados dinamicamente
        const horariosDetalhados = document.querySelectorAll('.horarios-detalhados-container');
        const horariosOnline = document.querySelectorAll('.horarios-online-container');
        
        horariosDetalhados.forEach(container => {
            if (isAsync) {
                container.style.display = 'none';
                this.setFieldsRequired(container, false);
            } else {
                container.style.display = 'block';
                this.setFieldsRequired(container, true);
            }
        });
        
        horariosOnline.forEach(container => {
            if (isAsync) {
                container.style.display = 'none';
                this.setFieldsRequired(container, false);
            } else {
                container.style.display = 'block';
                this.setFieldsRequired(container, true);
            }
        });
    }
    
    setFieldsRequired(container, isRequired) {
        if (!container) return;
        
        const fields = container.querySelectorAll('input, select, textarea');
        fields.forEach(field => {
            // Nunca adicionar required a checkboxes de dias da semana
            // A validação é feita via JavaScript na função validateOnlineFields()
            const isDiasAulaCheckbox = field.name === 'dias_aula_presencial[]' || field.name === 'dias_aula_online[]';
            
            if (isDiasAulaCheckbox) {
                // Sempre remover required dos checkboxes de dias da semana
                field.removeAttribute('required');
            } else if (isRequired) {
                field.setAttribute('required', 'required');
            } else {
                field.removeAttribute('required');
            }
        });
    }
    
    isAsyncMode() {
        const aulasAssincronasSim = document.querySelector('input[name="aulas_assincronas"][value="sim"]');
        return aulasAssincronasSim && aulasAssincronasSim.checked;
    }
    
    addUnidade() {
        const unidadesContainer = document.getElementById('unidades_list');
        if (!unidadesContainer) {
            console.error('Container unidades_list não encontrado!');
            return;
        }
        
        const unidadeCount = unidadesContainer.children.length + 1;
        
        const unidadeDiv = document.createElement('div');
        unidadeDiv.className = 'unidade-item';
        unidadeDiv.setAttribute('data-unidade', unidadeCount - 1);
        
        const modalidadeSelect = document.getElementById('modalidade');
        const modalidade = modalidadeSelect ? modalidadeSelect.value : 'Presencial';
        const isOnline = modalidade === 'Online';
        
        unidadeDiv.innerHTML = this.generateUnidadeHTML(unidadeCount, isOnline);
        
        unidadesContainer.appendChild(unidadeDiv);
        
        // Atualizar visibilidade dos botões de remover
        this.updateRemoveButtonsVisibility();
        
        // Scroll suave para a nova unidade
        unidadeDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    generateUnidadeHTML(count, isOnline) {
        const legendText = isOnline ? `Informações do Curso ${count}` : `Informações da Unidade ou Turma ${count}`;
        
        // Para cursos online, não incluir campos de endereço e bairro
        const enderecoFields = isOnline ? '' : `
                <label>Endereço da unidade ou turma*</label>
                <input type="text" name="endereco_unidade[]" required>
                <label>Bairro*</label>
                <input type="text" name="bairro_unidade[]" required>`;
        
        return `
            <fieldset class="unidade-fieldset">
                <legend>${legendText} <button type="button" class="remove-unidade-btn" onclick="removeUnidade(this)" style="display:none;">×</button></legend>
                ${enderecoFields}
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
                            ${this.generateTimeOptions()}
                        </select>
                    </div>
                    <div class="horario-field">
                        <label>Horário-Fim*</label>
                        <select name="horario_fim[]" required>
                            <option value="">Selecione o horário</option>
                            ${this.generateTimeOptions()}
                        </select>
                    </div>
                </div>
                <label>Dias de aula*</label>
                <div class="checkbox-group dias-aula">
                    ${this.generateDaysCheckboxes()}
                </div>
            </fieldset>
        `;
    }
    
    generateTimeOptions() {
        const times = ['06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', 
                      '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', 
                      '20:00', '21:00', '22:00', '23:00'];
        
        return times.map(time => `<option value="${time}">${time}</option>`).join('');
    }
    
    generateDaysCheckboxes() {
        const days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 
                     'Sexta-feira', 'Sábado', 'Domingo'];
        
        return days.map(day => `
            <label class="checkbox-label">
                <input type="checkbox" name="dias_aula_presencial[]" value="${day}">
                <span>${day}</span>
            </label>
        `).join('');
    }
    
    removeUnidade(button) {
        if (!button) return;
        
        const unidadesList = document.getElementById('unidades_list');
        const unidades = unidadesList.querySelectorAll('.unidade-item');
        
        // Não permitir remover se só há uma unidade
        if (unidades.length <= 1) {
            return;
        }
        
        const unidadeItem = button.closest('.unidade-item');
        if (unidadeItem) {
            unidadeItem.remove();
            this.renumberUnits();
        }
    }
    
    renumberUnits() {
        const unidades = document.querySelectorAll('.unidade-item');
        const modalidadeSelect = document.getElementById('modalidade');
        const modalidade = modalidadeSelect ? modalidadeSelect.value : 'Presencial';
        const isOnline = modalidade === 'Online';
        
        unidades.forEach((unidade, index) => {
            const legend = unidade.querySelector('legend');
            if (legend) {
                const legendText = isOnline ? `Informações do Curso ${index + 1}` : `Informações da Unidade ou Turma ${index + 1}`;
                legend.innerHTML = `${legendText} <button type="button" class="remove-unidade-btn" onclick="removeUnidade(this)" style="display:none;">×</button>`;
            }
            unidade.setAttribute('data-unidade', index);
        });
        
        // Atualizar visibilidade dos botões após renumerar
        this.updateRemoveButtonsVisibility();
    }
    
    updateRemoveButtonsVisibility() {
        const unidades = document.querySelectorAll('#unidades_list .unidade-item');
        const removeButtons = document.querySelectorAll('.remove-unidade-btn');
        
        // Mostrar botão de remover apenas se há mais de uma unidade
        removeButtons.forEach(button => {
            button.style.display = unidades.length > 1 ? 'inline-block' : 'none';
        });
    }
    
    addPlataforma() {
        const plataformaContainer = document.getElementById('plataforma_list');
        if (!plataformaContainer) return;
        
        const plataformaCount = plataformaContainer.children.length + 1;
        
        const plataformaDiv = document.createElement('div');
        plataformaDiv.className = 'plataforma-item';
        plataformaDiv.setAttribute('data-plataforma', plataformaCount - 1);
        
        plataformaDiv.innerHTML = this.generatePlataformaHTML(plataformaCount);
        
        plataformaContainer.appendChild(plataformaDiv);
        
        // Atualizar visibilidade dos botões de remover
        this.updateRemovePlataformaButtonsVisibility();
        
        // Scroll suave para a nova plataforma
        plataformaDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    generatePlataformaHTML(count) {
        return `
            <fieldset class="plataforma-fieldset">
                <legend>Informações da Plataforma ${count} <button type="button" class="remove-plataforma-btn" onclick="removePlataforma(this)" style="display:none;">×</button></legend>
                <label>Plataforma Digital</label>
                <input type="text" name="plataforma_digital[]" placeholder="Ex: Zoom, Google Meet, etc.">
                <label>Número de vagas*</label>
                <input type="number" name="vagas_unidade[]" min="1" required>
                <label>Carga Horária*</label>
                <input type="text" name="carga_horaria[]" required>
                <small style="color: red; font-size: 0.9em; margin-top: 5px; display: block;">(Dê preferência a carga horária no formato de horas)</small>
                
                <label class="required">Aulas Assíncronas?</label>
                <div class="radio-group">
                    <label class="radio-label">
                        <input type="radio" name="aulas_assincronas" value="sim" required checked onclick="toggleAulasAssincronas(true)"> SIM
                    </label>
                    <label class="radio-label">
                        <input type="radio" name="aulas_assincronas" value="nao" required onclick="toggleAulasAssincronas(false)"> NÃO
                    </label>
                </div>
                
                <div id="horarios_detalhados_online_container_${count}" class="horarios-detalhados-container" style="display: none;">
                    <div class="data-group">
                        <div class="data-field">
                            <label>Início das aulas</label>
                            <input type="date" name="inicio_aulas_data[]">
                        </div>
                        <div class="data-field">
                            <label>Fim das aulas</label>
                            <input type="date" name="fim_aulas_data[]">
                        </div>
                    </div>
                    
                    <div id="horarios_online_container_${count}" class="horarios-online-container" style="display: none;">
                        <div class="horario-group">
                            <div class="horario-field">
                                <label>Horário-Início</label>
                                <select name="horario_inicio[]">
                                    <option value="">Selecione o horário</option>
                                    ${this.generateTimeOptions()}
                                </select>
                            </div>
                            <div class="horario-field">
                                <label>Horário-Fim</label>
                                <select name="horario_fim[]">
                                    <option value="">Selecione o horário</option>
                                    ${this.generateTimeOptions()}
                                </select>
                            </div>
                        </div>
                        <label>Dias de aula</label>
                        <div class="checkbox-group dias-aula">
                            ${this.generateDaysCheckboxes()}
                        </div>
                    </div>
                </div>
            </fieldset>
        `;
    }
    
    removePlataforma(button) {
        if (!button) return;
        
        const plataformaList = document.getElementById('plataforma_list');
        const plataformas = plataformaList.querySelectorAll('.plataforma-item');
        
        // Não permitir remover se só há uma plataforma
        if (plataformas.length <= 1) {
            return;
        }
        
        const plataformaItem = button.closest('.plataforma-item');
        if (plataformaItem) {
            plataformaItem.remove();
            this.renumberPlataformas();
        }
    }
    
    renumberPlataformas() {
        const plataformas = document.querySelectorAll('.plataforma-item');
        plataformas.forEach((plataforma, index) => {
            const legend = plataforma.querySelector('legend');
            if (legend) {
                legend.innerHTML = `Informações da Plataforma ${index + 1} <button type="button" class="remove-plataforma-btn" onclick="removePlataforma(this)" style="display:none;">×</button>`;
            }
            plataforma.setAttribute('data-plataforma', index);
        });
        
        // Atualizar visibilidade dos botões após renumerar
        this.updateRemovePlataformaButtonsVisibility();
    }
    
    updateRemovePlataformaButtonsVisibility() {
        const plataformas = document.querySelectorAll('#plataforma_list .plataforma-item');
        const removeButtons = document.querySelectorAll('.remove-plataforma-btn');
        
        // Mostrar botão de remover apenas se há mais de uma plataforma
        removeButtons.forEach(button => {
            button.style.display = plataformas.length > 1 ? 'inline-block' : 'none';
        });
    }
}

// Exportar para uso global
window.FormManager = FormManager;

