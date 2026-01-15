// image-resizer.js
// Módulo para redimensionamento automático de imagens para 1080x1080

class ImageResizer {
    constructor() {
        this.targetSize = 1080;
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/bmp'];
    }

    /**
     * Inicializa o redimensionador para o campo de upload
     */
    init() {
        const fileInput = document.getElementById('capa_curso');
        if (!fileInput) return;

        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    }

    /**
     * Manipula a seleção de arquivo
     */
    async handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Validar tipo de arquivo
        if (!this.allowedTypes.includes(file.type)) {
            this.showError('Formato de arquivo não suportado. Use JPEG, PNG, JPG ou BMP.');
            event.target.value = '';
            return;
        }

        // Validar tamanho do arquivo
        if (file.size > this.maxFileSize) {
            this.showError('Arquivo muito grande. Tamanho máximo: 5MB');
            event.target.value = '';
            return;
        }

        try {
            // Mostrar loading
            this.showLoading('Processando imagem...');

            // Redimensionar imagem
            const resizedBlob = await this.resizeImage(file);

            // Criar novo arquivo com o blob redimensionado
            const resizedFile = new File([resizedBlob], file.name, {
                type: file.type,
                lastModified: Date.now()
            });

            // Substituir o arquivo original pelo redimensionado
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(resizedFile);
            event.target.files = dataTransfer.files;

            // Mostrar preview
            this.showPreview(resizedBlob);

            // Esconder loading
            this.hideLoading();

            // Mostrar mensagem de sucesso
            this.showSuccess(`Imagem redimensionada para ${this.targetSize}x${this.targetSize}px com sucesso!`);

        } catch (error) {
            console.error('Erro ao processar imagem:', error);
            this.showError('Erro ao processar imagem. Tente novamente.');
            event.target.value = '';
            this.hideLoading();
        }
    }

    /**
     * Redimensiona a imagem para 1080x1080
     */
    resizeImage(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = (e) => {
                const img = new Image();

                img.onload = () => {
                    try {
                        // Criar canvas
                        const canvas = document.createElement('canvas');
                        const ctx = canvas.getContext('2d');

                        // Definir dimensões do canvas
                        canvas.width = this.targetSize;
                        canvas.height = this.targetSize;

                        // Calcular dimensões para manter proporção e cobrir todo o canvas
                        const scale = Math.max(
                            this.targetSize / img.width,
                            this.targetSize / img.height
                        );

                        const scaledWidth = img.width * scale;
                        const scaledHeight = img.height * scale;

                        // Centralizar imagem no canvas
                        const x = (this.targetSize - scaledWidth) / 2;
                        const y = (this.targetSize - scaledHeight) / 2;

                        // Preencher fundo branco (caso a imagem tenha transparência)
                        ctx.fillStyle = '#FFFFFF';
                        ctx.fillRect(0, 0, this.targetSize, this.targetSize);

                        // Desenhar imagem redimensionada
                        ctx.drawImage(img, x, y, scaledWidth, scaledHeight);

                        // Converter canvas para blob
                        canvas.toBlob(
                            (blob) => {
                                if (blob) {
                                    resolve(blob);
                                } else {
                                    reject(new Error('Falha ao converter imagem'));
                                }
                            },
                            'image/jpeg',
                            0.92 // Qualidade JPEG (92%)
                        );
                    } catch (error) {
                        reject(error);
                    }
                };

                img.onerror = () => {
                    reject(new Error('Erro ao carregar imagem'));
                };

                img.src = e.target.result;
            };

            reader.onerror = () => {
                reject(new Error('Erro ao ler arquivo'));
            };

            reader.readAsDataURL(file);
        });
    }

    /**
     * Mostra preview da imagem
     */
    showPreview(blob) {
        const fileDisplay = document.querySelector('.file-upload-display');
        if (!fileDisplay) return;

        // Remover preview anterior
        const existingPreview = fileDisplay.querySelector('.image-preview');
        if (existingPreview) {
            existingPreview.remove();
        }

        // Criar novo preview
        const preview = document.createElement('img');
        preview.className = 'image-preview';
        preview.src = URL.createObjectURL(blob);
        preview.alt = 'Preview da imagem';

        fileDisplay.appendChild(preview);
        fileDisplay.classList.add('has-file');

        // Atualizar texto
        const fileText = fileDisplay.querySelector('.file-upload-text');
        if (fileText) {
            fileText.textContent = `Imagem redimensionada para ${this.targetSize}x${this.targetSize}px`;
        }
    }

    /**
     * Mostra mensagem de loading
     */
    showLoading(message) {
        const fileDisplay = document.querySelector('.file-upload-display');
        if (!fileDisplay) return;

        // Remover loading anterior
        const existingLoading = fileDisplay.querySelector('.upload-loading');
        if (existingLoading) {
            existingLoading.remove();
        }

        const loading = document.createElement('div');
        loading.className = 'upload-loading';
        loading.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            <span>${message}</span>
        `;

        fileDisplay.appendChild(loading);
    }

    /**
     * Esconde mensagem de loading
     */
    hideLoading() {
        const loading = document.querySelector('.upload-loading');
        if (loading) {
            loading.remove();
        }
    }

    /**
     * Mostra mensagem de erro
     */
    showError(message) {
        this.showNotification(message, 'error');
    }

    /**
     * Mostra mensagem de sucesso
     */
    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    /**
     * Mostra notificação
     */
    showNotification(message, type = 'info') {
        // Remover notificações anteriores
        const existingNotifications = document.querySelectorAll('.upload-notification');
        existingNotifications.forEach(n => n.remove());

        const notification = document.createElement('div');
        notification.className = `upload-notification upload-notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;

        const fileGroup = document.querySelector('.form-group.full-width:has(#capa_curso)');
        if (fileGroup) {
            fileGroup.appendChild(notification);

            // Remover após 5 segundos
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => notification.remove(), 300);
            }, 5000);
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    const imageResizer = new ImageResizer();
    imageResizer.init();
});
