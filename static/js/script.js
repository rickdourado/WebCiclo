// Funções de interatividade do formulário simplificado

// Validação em tempo real
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

// Confirmação ao sair da página
function setupPageLeaveConfirmation() {
    let formChanged = false;
    const form = document.querySelector('.course-form');
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            formChanged = true;
        });
    });
    
    window.addEventListener('beforeunload', function(e) {
        if (formChanged) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
    
    // Limpar flag ao submeter
    form.addEventListener('submit', function() {
        formChanged = false;
        localStorage.removeItem('course_form_draft');
    });
}

// Função para mostrar/esconder o campo de valor do curso
function toggleValorCurso(mostrar) {
    const valorCursoContainer = document.getElementById('valor_curso_container');
    const valorCursoInput = document.getElementById('valor_curso');
    
    if (mostrar) {
        valorCursoContainer.style.display = 'block';
        valorCursoInput.required = true;
    } else {
        valorCursoContainer.style.display = 'none';
        valorCursoInput.required = false;
        valorCursoInput.value = '';
    }
}

// Função para mostrar/esconder o campo de valor da bolsa
function toggleValorBolsa(mostrar) {
    const valorBolsaContainer = document.getElementById('valor_bolsa_container');
    const requisitosContainer = document.getElementById('requisitos_bolsa_container');
    const valorBolsaInput = document.getElementById('valor_bolsa');
    const requisitosInput = document.getElementById('requisitos_bolsa');
    
    if (mostrar) {
        valorBolsaContainer.style.display = 'block';
        requisitosContainer.style.display = 'block';
        valorBolsaInput.required = true;
        requisitosInput.required = true;
    } else {
        valorBolsaContainer.style.display = 'none';
        requisitosContainer.style.display = 'none';
        valorBolsaInput.required = false;
        requisitosInput.required = false;
        valorBolsaInput.value = '';
        requisitosInput.value = '';
    }
}

// Função para mostrar/esconder informações adicionais do curso
function toggleInfoAdicionais(mostrar) {
    const container = document.getElementById('info_adicionais_container');
    const campo = document.getElementById('info_adicionais');

    if (mostrar) {
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
        if (campo) {
            campo.value = '';
        }
    }
}

// Função para mostrar/esconder campos de unidades conforme modalidade selecionada
function toggleUnidades() {
    const modalidadeSelect = document.getElementById('modalidade');
    const unidadesContainer = document.getElementById('unidades_container');
    if (!modalidadeSelect || !unidadesContainer) return;

    const shouldShow = ['Presencial', 'Híbrido'].includes(modalidadeSelect.value);
    if (shouldShow) {
        unidadesContainer.style.display = 'block';
        unidadesContainer.querySelectorAll('input').forEach(el => el.setAttribute('required', ''));
    } else {
        unidadesContainer.style.display = 'none';
        unidadesContainer.querySelectorAll('input').forEach(el => {
            el.removeAttribute('required');
            el.value = '';
        });
    }
}

// Função para adicionar dinamicamente outra unidade
function addUnidade() {
    const unidadesContainer = document.getElementById('unidades_container');
    if (!unidadesContainer) return;

    const firstFieldset = unidadesContainer.querySelector('.unidade-fieldset');
    if (!firstFieldset) return;

    const clone = firstFieldset.cloneNode(true);
    clone.querySelectorAll('input').forEach(input => input.value = '');
    unidadesContainer.insertBefore(clone, unidadesContainer.querySelector('.add-unidade-btn'));
}

// Animação de loading no botão de submit
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
        requiredFields.forEach(field => {
            if (field.value.trim() === '') {
                field.classList.add('error');
                isValid = false;
            }
        });
        
        // Validar se fim das inscrições é posterior ao início
        const inicioData = document.getElementById('inicio_inscricoes_data');
        const inicioHora = document.getElementById('inicio_inscricoes_hora');
        const fimData = document.getElementById('fim_inscricoes_data');
        const fimHora = document.getElementById('fim_inscricoes_hora');
        
        if (inicioData && fimData) {
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

// Função para formatar valores monetários
function formatarValor(input) {
    // Remove qualquer caractere que não seja número ou vírgula
    let valor = input.value.replace(/[^0-9,]/g, '');
    
    // Atualiza o valor do campo apenas removendo caracteres inválidos
    input.value = valor;
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

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    setupRealTimeValidation();
    setupCharacterCounters();
    setupAutoSave();
    setupPageLeaveConfirmation();
    setupSubmitButton();
    setupFormFeatures();
    setupCustomValidation();
    // Configurar exibição dinâmica das unidades
    const modalidadeSelect = document.getElementById('modalidade');
    if (modalidadeSelect) {
        toggleUnidades();
        modalidadeSelect.addEventListener('change', toggleUnidades);
    }
    
    console.log('WebApp v3 - Formulário inicializado com sucesso!');
});