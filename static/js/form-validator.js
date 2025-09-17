// form-validator.js
// Validador centralizado para formulários

class FormValidator {
    constructor(form) {
        this.form = form;
        this.errors = [];
        this.warnings = [];
        this.setupValidation();
    }
    
    setupValidation() {
        this.setupRealTimeValidation();
        this.setupCharacterCounters();
        this.setupAutoSave();
        this.setupFormFeatures();
        this.setupCustomValidation();
    }
    
    setupRealTimeValidation() {
        const requiredFields = this.form.querySelectorAll('input[required], select[required], textarea[required]');
        
        requiredFields.forEach(field => {
            field.addEventListener('blur', () => {
                if (field.value.trim() === '') {
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            field.addEventListener('input', () => {
                if (field.classList.contains('error') && field.value.trim() !== '') {
                    field.classList.remove('error');
                }
            });
        });
    }
    
    setupCharacterCounters() {
        const textareas = this.form.querySelectorAll('textarea');
        
        textareas.forEach(textarea => {
            const maxLength = textarea.getAttribute('maxlength');
            if (maxLength) {
                const counter = document.createElement('div');
                counter.className = 'character-counter';
                counter.textContent = `0/${maxLength}`;
                textarea.parentNode.appendChild(counter);
                
                textarea.addEventListener('input', () => {
                    const currentLength = textarea.value.length;
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
    
    setupAutoSave() {
        const inputs = this.form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                const formData = new FormData(this.form);
                const data = Object.fromEntries(formData.entries());
                localStorage.setItem('course_form_draft', JSON.stringify(data));
            });
        });
        
        // Carregar dados salvos
        const savedData = localStorage.getItem('course_form_draft');
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                if (key !== 'valor_curso' && key !== 'valor_bolsa') {
                    const field = this.form.querySelector(`[name="${key}"]`);
                    if (field && !field.value && field.type !== 'file') {
                        field.value = data[key];
                    }
                }
            });
        }
    }
    
    setupFormFeatures() {
        // Configurar máscaras para campos de horário
        const timeInputs = this.form.querySelectorAll('input[type="time"]');
        timeInputs.forEach(input => {
            input.addEventListener('focus', () => {
                input.style.backgroundColor = '#333';
            });
            
            input.addEventListener('blur', () => {
                input.style.backgroundColor = '#2a2a2a';
            });
        });
        
        // Sincronizar datas quando necessário
        const inicioData = document.getElementById('inicio_inscricoes_data');
        const fimData = document.getElementById('fim_inscricoes_data');
        
        if (inicioData && fimData) {
            inicioData.addEventListener('change', () => {
                if (fimData.value < inicioData.value) {
                    fimData.value = inicioData.value;
                }
            });
        }
    }
    
    setupCustomValidation() {
        const submitBtn = this.form.querySelector('button[type="submit"]');
        
        this.form.addEventListener('submit', (e) => {
            const isValid = this.validateForm();
            
            if (!isValid) {
                e.preventDefault();
                this.showValidationErrors();
                submitBtn.innerHTML = '<i class="fas fa-save"></i> Criar Curso';
                submitBtn.disabled = false;
            }
        });
    }
    
    validateForm() {
        this.errors = [];
        this.warnings = [];
        
        console.log('=== INICIANDO VALIDAÇÃO DETALHADA ===');
        
        // Validar campos básicos
        this.validateBasicFields();
        
        // Validar campos condicionais
        this.validateConditionalFields();
        
        // Validar modalidade específica
        this.validateModalityFields();
        
        // Validar datas
        this.validateDates();
        
        // Validar parceiro externo
        this.validateExternalPartner();
        
        console.log('Validação concluída. Válido:', this.errors.length === 0);
        return this.errors.length === 0;
    }
    
    validateBasicFields() {
        const requiredFields = {
            'titulo': 'Nome do Curso',
            'descricao': 'Descrição',
            'orgao': 'Órgão Responsável',
            'tema': 'Tema/Categoria',
            'modalidade': 'Modalidade',
            'carga_horaria': 'Carga Horária',
            'curso_gratuito': 'Curso Gratuito',
            'oferece_bolsa': 'Oferece Bolsa',
            'oferece_certificado': 'Oferece Certificado',
            'parceiro_externo': 'Parceiro Externo',
            'publico_alvo': 'Público Alvo'
        };
        
        Object.entries(requiredFields).forEach(([fieldName, label]) => {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            console.log(`Verificando campo: ${fieldName}`);
            
            if (field && field.hasAttribute('required')) {
                if (field.value.trim() === '') {
                    this.errors.push(`${label} é obrigatório`);
                    console.log(`❌ ERRO: ${fieldName} vazio`);
                } else {
                    console.log(`✅ OK: ${fieldName} = ${field.value}`);
                }
            }
        });
    }
    
    validateConditionalFields() {
        // Validar campos de curso pago
        const cursoGratuito = this.form.querySelector('input[name="curso_gratuito"]:checked');
        if (cursoGratuito && cursoGratuito.value === 'nao') {
            const valorInteira = this.form.querySelector('[name="valor_curso_inteira"]');
            if (!valorInteira || !valorInteira.value.trim()) {
                this.errors.push("Valor inteira é obrigatório para cursos pagos");
            }
            
            const valorMeia = this.form.querySelector('[name="valor_curso_meia"]');
            const requisitosMeia = this.form.querySelector('[name="requisitos_meia"]');
            if (valorMeia && valorMeia.value.trim() && (!requisitosMeia || !requisitosMeia.value.trim())) {
                this.errors.push("Condições para meia-entrada são obrigatórias quando valor meia é informado");
            }
        }
        
        // Validar campos de bolsa
        const ofereceBolsa = this.form.querySelector('input[name="oferece_bolsa"]:checked');
        if (ofereceBolsa && ofereceBolsa.value === 'sim') {
            const valorBolsa = this.form.querySelector('[name="valor_bolsa"]');
            const requisitosBolsa = this.form.querySelector('[name="requisitos_bolsa"]');
            
            if (!valorBolsa || !valorBolsa.value.trim()) {
                this.errors.push("Valor da bolsa é obrigatório quando oferece bolsa");
            }
            if (!requisitosBolsa || !requisitosBolsa.value.trim()) {
                this.errors.push("Requisitos para bolsa são obrigatórios quando oferece bolsa");
            }
        }
        
        // Validar campos de certificado
        const ofereceCertificado = this.form.querySelector('input[name="oferece_certificado"]:checked');
        if (ofereceCertificado && ofereceCertificado.value === 'sim') {
            const preRequisitos = this.form.querySelector('[name="pre_requisitos"]');
            if (!preRequisitos || !preRequisitos.value.trim()) {
                this.errors.push("Pré-requisitos para certificado são obrigatórios quando oferece certificado");
            }
        }
    }
    
    validateModalityFields() {
        const modalidade = this.form.querySelector('#modalidade')?.value;
        console.log(`Modalidade selecionada: ${modalidade}`);
        
        const unidadesContainer = document.getElementById('unidades_container');
        
        if (modalidade && unidadesContainer && unidadesContainer.style.display !== 'none') {
            if (modalidade === 'Online') {
                console.log('✅ Modalidade Online: validando campos específicos...');
                this.validateOnlineFields();
            } else {
                console.log(`Modalidade ${modalidade}: validando campos de unidade...`);
                this.validateUnits();
            }
        }
    }
    
    validateOnlineFields() {
        // Verificar se aulas são síncronas (NÃO assíncronas)
        const aulasAssincronas = this.form.querySelector('input[name="aulas_assincronas"]:checked');
        
        if (aulasAssincronas && aulasAssincronas.value === 'nao') {
            // Para aulas síncronas, pelo menos um dia deve ser selecionado
            const diasCheckboxes = this.form.querySelectorAll('input[name="dias_aula[]"]');
            const algumDiaSelecionado = Array.from(diasCheckboxes).some(cb => cb.checked);
            
            if (!algumDiaSelecionado) {
                this.errors.push('Pelo menos um dia da semana é obrigatório para aulas síncronas online');
                console.log('❌ ERRO: Nenhum dia selecionado para aulas síncronas online');
            } else {
                const diasSelecionados = Array.from(diasCheckboxes)
                    .filter(cb => cb.checked)
                    .map(cb => cb.value);
                console.log(`✅ Dias selecionados: ${diasSelecionados.join(', ')}`);
            }
        } else {
            console.log('✅ Aulas assíncronas: dias não são obrigatórios');
        }
    }
    
    validateUnits() {
        // Validar apenas unidades presenciais (que têm data-unidade, não data-plataforma)
        const unidades = document.querySelectorAll('.unidade-item[data-unidade]');
        console.log(`Encontradas ${unidades.length} unidades presenciais`);
        
        unidades.forEach((unidade, index) => {
            console.log(`Validando unidade ${index + 1}...`);
            const diasCheckboxes = unidade.querySelectorAll('input[name="dias_aula[]"]');
            console.log(`Encontrados ${diasCheckboxes.length} checkboxes de dias`);
            
            const algumDiaSelecionado = Array.from(diasCheckboxes).some(cb => cb.checked);
            console.log(`Algum dia selecionado: ${algumDiaSelecionado}`);
            
            if (!algumDiaSelecionado) {
                this.errors.push(`Unidade ${index + 1} - Nenhum dia selecionado`);
                console.log(`❌ ERRO: Unidade ${index + 1} - Nenhum dia selecionado`);
            } else {
                const diasSelecionados = Array.from(diasCheckboxes)
                    .filter(cb => cb.checked)
                    .map(cb => cb.value);
                console.log(`✅ OK: Unidade ${index + 1} - Dias: ${diasSelecionados.join(', ')}`);
            }
        });
    }
    
    validateDates() {
        const inicioData = document.getElementById('inicio_inscricoes_data');
        const inicioHora = document.getElementById('inicio_inscricoes_hora');
        const fimData = document.getElementById('fim_inscricoes_data');
        const fimHora = document.getElementById('fim_inscricoes_hora');
        
        if (inicioData && fimData && inicioData.value && fimData.value) {
            const inicioDateTime = new Date(`${inicioData.value}T${inicioHora ? inicioHora.value : '00:00'}`);
            const fimDateTime = new Date(`${fimData.value}T${fimHora ? fimHora.value : '23:59'}`);
            
            if (fimDateTime < inicioDateTime) {
                this.errors.push('O fim das inscrições deve ser posterior ou igual ao início das inscrições.');
            }
        }
    }
    
    validateExternalPartner() {
        const parceiroExterno = this.form.querySelector('input[name="parceiro_externo"]:checked');
        console.log(`Parceiro externo selecionado: ${parceiroExterno ? parceiroExterno.value : 'nenhum'}`);
        
        if (parceiroExterno && parceiroExterno.value === 'sim') {
            console.log('Parceiro externo = SIM, validando campos...');
            const parceiroNome = document.getElementById('parceiro_nome');
            
            if (parceiroNome && parceiroNome.value.trim() === '') {
                this.errors.push('Nome do parceiro é obrigatório quando há parceiro externo');
                console.log('❌ ERRO: Nome do parceiro vazio quando parceiro externo = sim');
            } else {
                console.log(`✅ OK: parceiro_nome = ${parceiroNome?.value}`);
            }
        } else {
            console.log('Parceiro externo = NÃO, pulando validação');
        }
    }
    
    showValidationErrors() {
        console.log('Formulário inválido, não enviando...');
        alert('Por favor, preencha todos os campos obrigatórios visíveis.');
    }
    
    clearErrors() {
        this.errors = [];
        this.warnings = [];
    }
}

// Exportar para uso global
window.FormValidator = FormValidator;
