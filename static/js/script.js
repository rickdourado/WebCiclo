// script.js - Arquivo principal JavaScript refatorado
// Agora usa módulos separados para melhor organização

let formValidator;
let formManager;

// Funções para máscara e validação de horário
function formatarHorario(input) {
    // Remove todos os caracteres não numéricos
    let valor = input.value.replace(/\D/g, '');

    // Limita a 4 dígitos (HHMM)
    if (valor.length > 4) {
        valor = valor.substring(0, 4);
    }

    // Adiciona os dois pontos após os dois primeiros dígitos
    if (valor.length >= 3) {
        valor = valor.substring(0, 2) + ':' + valor.substring(2);
    }

    input.value = valor;
}

function validarHorario(input) {
    const valor = input.value;

    // Verifica se está no formato XX:XX
    const regex = /^([0-1][0-9]|2[0-3]):([0-5][0-9])$/;

    if (valor && !regex.test(valor)) {
        input.setCustomValidity('Formato inválido. Use HH:MM (ex: 10:30)');
        input.classList.add('campo-erro');
    } else {
        input.setCustomValidity('');
        input.classList.remove('campo-erro');
    }
}

// Funções globais mantidas para compatibilidade com templates
function toggleAulasAssincronas(isAsync) {
    if (formManager) {
        formManager.toggleAulasAssincronas(isAsync);
    }
}

function toggleUnidades() {
    if (formManager) {
        formManager.toggleUnidades();
    }
}

function addUnidade() {
    if (formManager) {
        formManager.addUnidade();
    }
}

function removeUnidade(button) {
    if (formManager) {
        formManager.removeUnidade(button);
    }
}

// Função addPlataforma removida - agora gerenciada exclusivamente pelo FormManager via event listener

function removePlataforma(button) {
    if (formManager) {
        formManager.removePlataforma(button);
    }
}

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

            textarea.addEventListener('input', function () {
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
        input.addEventListener('input', function () {
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

    form.addEventListener('submit', function () {
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Criando Curso...';
        submitBtn.disabled = true;
    });
}

// Configurar funcionalidades específicas do formulário
function setupFormFeatures() {
    // Configurar máscaras para campos de horário
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(input => {
        input.addEventListener('focus', function () {
            this.style.backgroundColor = '#333';
        });

        input.addEventListener('blur', function () {
            this.style.backgroundColor = '#2a2a2a';
        });
    });

    // Sincronizar datas quando necessário
    const inicioData = document.getElementById('inicio_inscricoes_data');
    const fimData = document.getElementById('fim_inscricoes_data');

    if (inicioData && fimData) {
        inicioData.addEventListener('change', function () {
            if (fimData.value < this.value) {
                fimData.value = this.value;
            }
        });
    }

    // GARANTIR QUE O FORMULÁRIO SEJA ENVIADO
    const form = document.querySelector('.course-form');
    if (form) {
        // Remover qualquer listener de submit que possa estar impedindo o envio
        form.addEventListener('submit', function (e) {
            console.log('Formulário sendo enviado...');
            // NÃO prevenir o comportamento padrão - deixar o formulário ser enviado
        });
    }
}

// Validações customizadas - SIMPLIFICADA
function setupCustomValidation() {
    const form = document.querySelector('.course-form');
    const submitBtn = form.querySelector('button[type="submit"]');

    // REMOVER VALIDAÇÃO CUSTOMIZADA QUE PODE ESTAR IMPEDINDO O ENVIO
    // Deixar apenas a validação HTML5 nativa funcionar

    form.addEventListener('submit', function (e) {
        console.log('Formulário sendo enviado via validação customizada...');
        // NÃO fazer validação customizada - deixar HTML5 validar
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
                    const diasCheckboxes = unidade.querySelectorAll('input[name="dias_aula_presencial[]"]');
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
                alert('O fim das inscrições deve ser posterior ou igual ao início das inscrições.');
                isValid = false;
            }
        }

        // Validar datas das aulas em relação às datas de inscrições
        if (!validateAulasDates()) {
            isValid = false;
        }

        // SEMPRE PERMITIR O ENVIO - remover validação que impede
        // if (!isValid) {
        //     e.preventDefault();
        //     // Restaurar o botão de submit se a validação falhar
        //     submitBtn.innerHTML = '<i class="fas fa-save"></i> Criar Curso';
        //     submitBtn.disabled = false;
        // }
    });
}

// Função para configurar validação de datas em tempo real
function setupDateValidation() {
    // Validar quando a data de fim das inscrições mudar
    const fimInscricoesData = document.getElementById('fim_inscricoes_data');
    if (fimInscricoesData) {
        fimInscricoesData.addEventListener('change', function () {
            validateAulasDatesRealTime();
        });
    }

    // Validar quando as datas das aulas mudarem
    document.addEventListener('change', function (e) {
        if (e.target.name === 'inicio_aulas_data[]' || e.target.name === 'fim_aulas_data[]') {
            validateAulasDatesRealTime();
        }
    });
}

// Função para validar datas das aulas em tempo real (sem alertas)
function validateAulasDatesRealTime() {
    const fimInscricoesData = document.getElementById('fim_inscricoes_data');
    if (!fimInscricoesData || !fimInscricoesData.value) {
        return;
    }

    const fimInscricoes = new Date(fimInscricoesData.value);

    // Validar datas das unidades
    const inicioAulasInputs = document.querySelectorAll('input[name="inicio_aulas_data[]"]');
    const fimAulasInputs = document.querySelectorAll('input[name="fim_aulas_data[]"]');

    inicioAulasInputs.forEach((input) => {
        if (input.value) {
            const inicioAulas = new Date(input.value);
            if (inicioAulas < fimInscricoes) {
                input.style.borderColor = '#e53e3e';
                input.style.backgroundColor = 'rgba(229, 62, 62, 0.05)';
            } else {
                input.style.borderColor = '';
                input.style.backgroundColor = '';
            }
        }
    });

    fimAulasInputs.forEach((input) => {
        if (input.value) {
            const fimAulas = new Date(input.value);
            if (fimAulas < fimInscricoes) {
                input.style.borderColor = '#e53e3e';
                input.style.backgroundColor = 'rgba(229, 62, 62, 0.05)';
            } else {
                input.style.borderColor = '';
                input.style.backgroundColor = '';
            }
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

    submitBtn.addEventListener('click', function (e) {
        // NÃO PREVENIR O COMPORTAMENTO PADRÃO - deixar o formulário ser enviado

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
                    const diasCheckboxes = unidade.querySelectorAll('input[name="dias_aula_presencial[]"]');
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
                alert('O fim das inscrições deve ser posterior ou igual ao início das inscrições.');
                isValid = false;
            }
        }

        // Validar datas das aulas em relação às datas de inscrições
        if (!validateAulasDates()) {
            isValid = false;
        }

        console.log('Validação concluída. Válido:', isValid);

        if (isValid) {
            // Se o formulário for válido, mostrar animação de loading
            console.log('Formulário válido, enviando...');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Criando Curso...';
            submitBtn.disabled = true;

            // Debug: verificar dados do formulário
            const formData = new FormData(form);
            console.log('Dados do formulário:');
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }

            // NÃO CHAMAR form.submit() - deixar o comportamento padrão do botão funcionar
        } else {
            // Prevenir envio se inválido
            e.preventDefault();
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

// Função para validar datas das aulas em relação às datas de inscrições
function validateAulasDates() {
    const fimInscricoesData = document.getElementById('fim_inscricoes_data');
    if (!fimInscricoesData || !fimInscricoesData.value) {
        return true; // Se não há data de fim das inscrições, não validar
    }

    const fimInscricoes = new Date(fimInscricoesData.value);
    let isValid = true;

    // Validar datas das unidades (modalidade Presencial/Híbrida)
    const inicioAulasInputs = document.querySelectorAll('input[name="inicio_aulas_data[]"]');
    const fimAulasInputs = document.querySelectorAll('input[name="fim_aulas_data[]"]');

    inicioAulasInputs.forEach((input, index) => {
        if (input.value) {
            const inicioAulas = new Date(input.value);
            if (inicioAulas < fimInscricoes) {
                const fimInscricoesFormatado = fimInscricoes.toLocaleDateString('pt-BR');
                alert(`Início das aulas da unidade ${index + 1} deve ser posterior ou igual ao fim das inscrições (${fimInscricoesFormatado}).`);
                isValid = false;
            }
        }
    });

    fimAulasInputs.forEach((input, index) => {
        if (input.value) {
            const fimAulas = new Date(input.value);
            if (fimAulas < fimInscricoes) {
                const fimInscricoesFormatado = fimInscricoes.toLocaleDateString('pt-BR');
                alert(`Fim das aulas da unidade ${index + 1} deve ser posterior ou igual ao fim das inscrições (${fimInscricoesFormatado}).`);
                isValid = false;
            }
        }
    });

    return isValid;
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
document.addEventListener('DOMContentLoaded', function () {
    const camposValor = document.querySelectorAll('#valor_curso, #valor_bolsa');

    camposValor.forEach(campo => {
        campo.addEventListener('blur', function () {
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

// Função toggleUnidades() removida - agora é gerenciada pelo FormManager

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

// Função addUnidade removida - agora gerenciada exclusivamente pelo FormManager via event listener

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function () {
    // Inicializar gerenciador de formulários
    formManager = new FormManager();

    // Inicializar validador de formulários
    const form = document.querySelector('.course-form');
    if (form) {
        formValidator = new FormValidator(form);
    }

    // Inicializar validação de datas
    setupDateValidation();

    // Inicializar campos condicionais
    if (formManager) {
        formManager.initializeAsyncFields();
    }

    console.log('WebApp v4 - Formulário inicializado com sucesso!');
    console.log('Módulos carregados: FormManager, FormValidator');
});
