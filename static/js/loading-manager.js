// static/js/loading-manager.js
// Gerenciador de Loading Overlay com feedback visual

class LoadingManager {
    constructor() {
        this.overlay = document.getElementById('loadingOverlay');
        this.progressBar = document.getElementById('loadingProgressBar');
        this.steps = {
            step1: document.getElementById('step1'),
            step2: document.getElementById('step2'),
            step3: document.getElementById('step3'),
            step4: document.getElementById('step4'),
            step5: document.getElementById('step5')
        };
        this.currentStep = 0;
        this.progressInterval = null;
    }

    /**
     * Mostra o loading overlay
     */
    show() {
        if (this.overlay) {
            this.overlay.classList.add('active');
            this.reset();
            this.startProgressSimulation();

            // Adicionar botão de emergência após 20 segundos
            setTimeout(() => {
                this.addEmergencyCloseButton();
            }, 20000);
        }
    }

    /**
     * Adiciona botão de emergência para fechar loading
     */
    addEmergencyCloseButton() {
        if (this.overlay && this.overlay.classList.contains('active')) {
            const container = this.overlay.querySelector('.loading-container');
            if (container && !container.querySelector('.emergency-close')) {
                const emergencyBtn = document.createElement('button');
                emergencyBtn.className = 'emergency-close';
                emergencyBtn.innerHTML = '✕ Fechar';
                emergencyBtn.style.cssText = `
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: #e53e3e;
                    color: white;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                    z-index: 10001;
                `;
                emergencyBtn.onclick = () => {
                    console.log('🚨 Botão de emergência clicado, fechando loading...');
                    this.hide();
                };
                container.appendChild(emergencyBtn);
            }
        }
    }

    /**
     * Esconde o loading overlay
     */
    hide() {
        if (this.overlay) {
            // Completar todas as etapas antes de fechar
            this.completeAllSteps();

            // Aguardar animação de conclusão
            setTimeout(() => {
                this.overlay.classList.remove('active');
                this.reset();
            }, 800);
        }
    }

    /**
     * Reseta o estado do loading
     */
    reset() {
        this.currentStep = 0;
        if (this.progressBar) {
            this.progressBar.style.width = '0%';
        }

        // Resetar todos os steps
        Object.values(this.steps).forEach(step => {
            if (step) {
                step.classList.remove('active', 'completed');
            }
        });

        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    /**
     * Simula progresso automático
     */
    startProgressSimulation() {
        let progress = 0;
        const steps = [
            { time: 500, progress: 20, step: 1 },   // Validando informações
            { time: 1000, progress: 40, step: 2 },  // Processando imagens
            { time: 2500, progress: 60, step: 3 },  // IA (mais demorado)
            { time: 1500, progress: 80, step: 4 },  // Gerando arquivos
            { time: 1000, progress: 95, step: 5 }   // Finalizando
        ];

        let currentStepIndex = 0;

        const simulateProgress = () => {
            if (currentStepIndex < steps.length) {
                const currentStepData = steps[currentStepIndex];

                // Marcar step anterior como completo
                if (currentStepIndex > 0) {
                    this.completeStep(currentStepIndex);
                }

                // Ativar step atual
                this.activateStep(currentStepIndex + 1);

                // Atualizar barra de progresso
                progress = currentStepData.progress;
                if (this.progressBar) {
                    this.progressBar.style.width = `${progress}%`;
                }

                currentStepIndex++;

                // Agendar próximo step
                if (currentStepIndex < steps.length) {
                    setTimeout(simulateProgress, currentStepData.time);
                } else {
                    // Quando chegar ao último step, completar e fechar após um tempo
                    setTimeout(() => {
                        this.completeAllSteps();
                        // Auto-fechar após 15 segundos como segurança
                        setTimeout(() => {
                            console.log('⚠️ Loading auto-fechado por timeout de segurança');
                            this.hide();
                        }, 15000);
                    }, 1000);
                }
            }
        };

        // Iniciar simulação
        setTimeout(simulateProgress, 300);
    }

    /**
     * Ativa um step específico
     */
    activateStep(stepNumber) {
        const stepKey = `step${stepNumber}`;
        if (this.steps[stepKey]) {
            this.steps[stepKey].classList.add('active');
        }
    }

    /**
     * Completa um step específico
     */
    completeStep(stepNumber) {
        const stepKey = `step${stepNumber}`;
        if (this.steps[stepKey]) {
            this.steps[stepKey].classList.remove('active');
            this.steps[stepKey].classList.add('completed');

            // Adicionar ícone de check
            const icon = this.steps[stepKey].querySelector('.step-icon');
            if (icon) {
                icon.innerHTML = '✓';
            }
        }
    }

    /**
     * Completa todos os steps
     */
    completeAllSteps() {
        if (this.progressBar) {
            this.progressBar.style.width = '100%';
        }

        Object.keys(this.steps).forEach((stepKey, index) => {
            if (this.steps[stepKey]) {
                this.steps[stepKey].classList.remove('active');
                this.steps[stepKey].classList.add('completed');

                const icon = this.steps[stepKey].querySelector('.step-icon');
                if (icon) {
                    icon.innerHTML = '✓';
                }
            }
        });
    }

    /**
     * Atualiza o texto principal do loading
     */
    updateText(text) {
        const loadingText = document.querySelector('.loading-text');
        if (loadingText) {
            loadingText.textContent = text;
        }
    }

    /**
     * Atualiza a descrição do loading
     */
    updateDescription(description) {
        const loadingDescription = document.querySelector('.loading-description');
        if (loadingDescription) {
            loadingDescription.textContent = description;
        }
    }
}

// Instanciar globalmente
window.loadingManager = new LoadingManager();

// Interceptar submissão de formulários para mostrar loading
document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            // Verificar se não é um formulário de login ou busca
            if (!form.classList.contains('no-loading') &&
                !form.id.includes('search') &&
                !form.id.includes('login')) {

                console.log('Loading manager: Formulário sendo enviado, mostrando loading...');

                // Mostrar loading
                window.loadingManager.show();

                // IMPORTANTE: NÃO prevenir o comportamento padrão
                // O formulário continuará a ser enviado normalmente
                // O loading será fechado quando a página recarregar ou
                // quando o servidor retornar uma resposta
            }
        });
    });

    // Esconder loading ao carregar a página (caso tenha ficado ativo)
    window.addEventListener('load', function () {
        if (window.loadingManager) {
            console.log('🔄 Página carregada, fechando loading...');
            window.loadingManager.hide();
        }
    });

    // Esconder loading também no DOMContentLoaded como backup
    window.addEventListener('DOMContentLoaded', function () {
        // Aguardar um pouco para garantir que a página carregou completamente
        setTimeout(() => {
            if (window.loadingManager && window.loadingManager.overlay &&
                window.loadingManager.overlay.classList.contains('active')) {
                console.log('🔄 DOMContentLoaded: Fechando loading ativo...');
                window.loadingManager.hide();
            }
        }, 1000);
    });

    // Esconder loading quando a página fica visível (mudança de aba)
    document.addEventListener('visibilitychange', function () {
        if (!document.hidden && window.loadingManager &&
            window.loadingManager.overlay &&
            window.loadingManager.overlay.classList.contains('active')) {
            console.log('🔄 Página ficou visível, fechando loading...');
            window.loadingManager.hide();
        }
    });
});
