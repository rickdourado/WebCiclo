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
            // Não carregar os campos de valor do curso e da bolsa
            if (key !== 'valor_curso' && key !== 'valor_bolsa') {
                const field = form.querySelector(`[name="${key}"]`);
                if (field && !field.value) {
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
        
        // Validar campos obrigatórios
        const requiredFields = form.querySelectorAll('[required]');
        const processedRadioNames = new Set();
        
        requiredFields.forEach(field => {
            // Verificar se o campo está em um container visível
            const isVisible = isFieldVisible(field);
            
            // Se o campo não estiver visível, não validar
            if (!isVisible) return;
            
            if (field.type === 'radio' || field.type === 'checkbox') {
                // Evita processar o mesmo grupo mais de uma vez
                if (processedRadioNames.has(field.name)) return;
                processedRadioNames.add(field.name);
                
                // Verifica se algum radio/checkbox do grupo está marcado
                const group = form.querySelectorAll(`input[name="${field.name}"]`);
                const algumMarcado = Array.from(group).some(radio => radio.checked);
                
                if (!algumMarcado) {
                    group.forEach(radio => radio.classList.add('error'));
                    isValid = false;
                } else {
                    group.forEach(radio => radio.classList.remove('error'));
                }
            } else {
                // Para outros tipos de campo, verifica se está vazio
                if (field.value.trim() === '') {
                    field.classList.add('error');
                    isValid = false;
                } else {
                    field.classList.remove('error');
                }
            }
        });
        
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
        
        // Validar campos obrigatórios
        const requiredFields = form.querySelectorAll('[required]');
        const processedRadioNames = new Set();
        
        requiredFields.forEach(field => {
            // Verificar se o campo está em um container visível
            const isVisible = isFieldVisible(field);
            
            // Se o campo não estiver visível, não validar
            if (!isVisible) return;
            
            if (field.type === 'radio' || field.type === 'checkbox') {
                // Evita processar o mesmo grupo mais de uma vez
                if (processedRadioNames.has(field.name)) return;
                processedRadioNames.add(field.name);
                
                // Verifica se algum radio/checkbox do grupo está marcado
                const group = form.querySelectorAll(`input[name="${field.name}"]`);
                const algumMarcado = Array.from(group).some(radio => radio.checked);
                
                if (!algumMarcado) {
                    group.forEach(radio => radio.classList.add('error'));
                    isValid = false;
                } else {
                    group.forEach(radio => radio.classList.remove('error'));
                }
            } else {
                // Para outros tipos de campo, verifica se está vazio
                if (field.value.trim() === '') {
                    field.classList.add('error');
                    isValid = false;
                } else {
                    field.classList.remove('error');
                }
            }
        });
        
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
        
        if (isValid) {
            // Se o formulário for válido, mostrar animação de loading e enviar
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Criando Curso...';
            submitBtn.disabled = true;
            form.submit();
        } else {
            // Exibir mensagem de erro
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
    const legendaUnidade = document.querySelector('#unidades_container fieldset legend');
    
    if (modalidade === 'Presencial' || modalidade === 'Híbrido' || modalidade === 'Online') {
        unidadesContainer.style.display = 'block';
        
        // Tratamento específico para modalidade Online
        if (modalidade === 'Online') {
            // Altera o título para "Informações do Curso"
            if (legendaUnidade) {
                legendaUnidade.textContent = 'Informações do Curso';
                legendaUnidade.style.fontSize = '1.2em'; // Aumenta o tamanho da fonte
            }
            
            // Oculta campos de endereço e bairro para modalidade Online
            document.querySelectorAll('#unidades_container input[name="endereco_unidade[]"], #unidades_container input[name="bairro_unidade[]"]').forEach(field => {
                field.style.display = 'none';
                field.previousElementSibling.style.display = 'none'; // Oculta também as labels
                field.removeAttribute('required');
            });
            
            // Mantém visíveis e obrigatórios os outros campos
            document.querySelectorAll('#unidades_container input:not([name="endereco_unidade[]"]):not([name="bairro_unidade[]"]), #unidades_container select').forEach(field => {
                if (field.hasAttribute('required')) {
                    field.setAttribute('required', 'required');
                }
            });
        } else {
            // Para Presencial e Híbrido, mostra todos os campos e restaura o título original
            if (legendaUnidade) {
                legendaUnidade.textContent = 'Informações da Unidade';
                legendaUnidade.style.fontSize = '1.2em'; // Usa o mesmo tamanho de fonte que a modalidade Online
            }
            document.querySelectorAll('#unidades_container input, #unidades_container label').forEach(field => {
                field.style.display = '';
            });
            
            // Restaura o required para todos os campos que tinham originalmente
            document.querySelectorAll('#unidades_container input[required], #unidades_container select[required]').forEach(field => {
                field.setAttribute('required', 'required');
            });
        }
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
    
    unidadeDiv.innerHTML = `
        <h4>Unidade ${unidadeCount}</h4>
        <div class="form-group">
            <label for="unidade_${unidadeCount}">Nome da Unidade:</label>
            <input type="text" id="unidade_${unidadeCount}" name="unidade_${unidadeCount}" class="unidade-field" required>
        </div>
        <div class="form-group">
            <label for="endereco_${unidadeCount}">Endereço:</label>
            <input type="text" id="endereco_${unidadeCount}" name="endereco_${unidadeCount}" class="unidade-field" required>
        </div>
    `;
    
    unidadesContainer.appendChild(unidadeDiv);
    
    // Atualizar o contador de unidades
    document.getElementById('unidade_count').value = unidadeCount;
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