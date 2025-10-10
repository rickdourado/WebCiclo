// custom-select.js - Dropdown customizado para órgãos com siglas em negrito

class CustomSelect {
    constructor(selectElement) {
        this.select = selectElement;
        this.container = null;
        this.display = null;
        this.optionsContainer = null;
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        this.createCustomSelect();
        this.bindEvents();
    }
    
    createCustomSelect() {
        // Criar container
        this.container = document.createElement('div');
        this.container.className = 'custom-select-container';
        
        // Criar display
        this.display = document.createElement('div');
        this.display.className = 'custom-select-display';
        this.display.innerHTML = `
            <span class="selected-text">Selecione um órgão</span>
            <span class="arrow">▼</span>
        `;
        
        // Criar container de opções
        this.optionsContainer = document.createElement('div');
        this.optionsContainer.className = 'custom-select-options';
        
        // Adicionar opções
        this.populateOptions();
        
        // Montar estrutura
        this.container.appendChild(this.display);
        this.container.appendChild(this.optionsContainer);
        
        // Substituir select original
        this.select.parentNode.insertBefore(this.container, this.select);
        this.select.style.display = 'none';
    }
    
    populateOptions() {
        const options = this.select.querySelectorAll('option');
        
        options.forEach((option, index) => {
            if (index === 0) return; // Pular primeira opção (placeholder)
            
            const optionElement = document.createElement('div');
            optionElement.className = 'custom-select-option';
            optionElement.dataset.value = option.value;
            
            // Processar texto para destacar sigla
            const text = option.textContent;
            const parts = text.split(' - ');
            
            if (parts.length === 2) {
                const [nome, sigla] = parts;
                optionElement.innerHTML = `${nome} - <span class="sigla">${sigla}</span>`;
            } else {
                optionElement.textContent = text;
            }
            
            this.optionsContainer.appendChild(optionElement);
        });
    }
    
    bindEvents() {
        // Toggle dropdown
        this.display.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
        });
        
        // Selecionar opção
        this.optionsContainer.addEventListener('click', (e) => {
            if (e.target.closest('.custom-select-option')) {
                const option = e.target.closest('.custom-select-option');
                this.selectOption(option);
            }
        });
        
        // Fechar ao clicar fora
        document.addEventListener('click', () => {
            this.close();
        });
        
        // Fechar com ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.close();
            }
        });
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        this.isOpen = true;
        this.display.classList.add('active');
        this.optionsContainer.classList.add('active');
    }
    
    close() {
        this.isOpen = false;
        this.display.classList.remove('active');
        this.optionsContainer.classList.remove('active');
    }
    
    selectOption(optionElement) {
        const value = optionElement.dataset.value;
        const text = optionElement.textContent;
        
        // Atualizar select original
        this.select.value = value;
        
        // Atualizar display
        this.display.querySelector('.selected-text').innerHTML = optionElement.innerHTML;
        
        // Remover seleção anterior
        this.optionsContainer.querySelectorAll('.custom-select-option').forEach(opt => {
            opt.classList.remove('selected');
        });
        
        // Marcar como selecionado
        optionElement.classList.add('selected');
        
        // Fechar dropdown
        this.close();
        
        // Disparar evento change no select original
        this.select.dispatchEvent(new Event('change', { bubbles: true }));
        
        console.log('Órgão selecionado:', text);
    }
    
    setValue(value) {
        const option = this.optionsContainer.querySelector(`[data-value="${value}"]`);
        if (option) {
            this.selectOption(option);
        }
    }
}

// Inicializar custom selects quando DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    const orgaoSelects = document.querySelectorAll('select#orgao');
    
    orgaoSelects.forEach(select => {
        new CustomSelect(select);
        console.log('Custom select inicializado para órgão');
    });
});