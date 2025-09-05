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
            const field = form.querySelector(`[name="${key}"]`);
            if (field && !field.value) {
                field.value = data[key];
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
    
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validar se fim das inscrições é posterior ao início
        const inicioData = document.getElementById('inicio_inscricoes_data');
        const inicioHora = document.getElementById('inicio_inscricoes_hora');
        const fimData = document.getElementById('fim_inscricoes_data');
        const fimHora = document.getElementById('fim_inscricoes_hora');
        
        if (inicioData.value && fimData.value) {
            const inicioDateTime = new Date(`${inicioData.value}T${inicioHora.value}`);
            const fimDateTime = new Date(`${fimData.value}T${fimHora.value}`);
            
            if (fimDateTime <= inicioDateTime) {
                alert('O fim das inscrições deve ser posterior ao início das inscrições.');
                isValid = false;
            }
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    setupRealTimeValidation();
    setupCharacterCounters();
    setupAutoSave();
    setupPageLeaveConfirmation();
    setupSubmitButton();
    setupFormFeatures();
    setupCustomValidation();
    
    console.log('WebApp v3 - Formulário inicializado com sucesso!');
});