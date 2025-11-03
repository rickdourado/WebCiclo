// Script para detectar e aplicar fallback de ícones Font Awesome
(function() {
    'use strict';
    
    function checkFontAwesome() {
        // Criar elemento de teste
        const testElement = document.createElement('i');
        testElement.className = 'fas fa-home';
        testElement.style.position = 'absolute';
        testElement.style.left = '-9999px';
        testElement.style.fontSize = '16px';
        document.body.appendChild(testElement);
        
        // Verificar se Font Awesome carregou
        const computedStyle = window.getComputedStyle(testElement, ':before');
        const fontFamily = computedStyle.getPropertyValue('font-family');
        
        let fontAwesomeLoaded = false;
        
        // Verificar diferentes variações do nome da fonte
        if (fontFamily.includes('Font Awesome') || 
            fontFamily.includes('FontAwesome') ||
            fontFamily.includes('"Font Awesome 6 Free"')) {
            fontAwesomeLoaded = true;
        }
        
        // Verificar também pelo conteúdo do pseudo-elemento
        const content = computedStyle.getPropertyValue('content');
        if (content && content !== 'none' && content !== '""' && !content.includes('🏠')) {
            fontAwesomeLoaded = true;
        }
        
        // Limpar elemento de teste
        document.body.removeChild(testElement);
        
        if (fontAwesomeLoaded) {
            console.log('✅ Font Awesome carregado com sucesso');
            document.documentElement.classList.add('fa-loaded');
        } else {
            console.warn('⚠️ Font Awesome não carregou, usando fallback');
            document.documentElement.classList.add('fa-fallback');
            
            // Carregar CSS de fallback se não estiver carregado
            if (!document.querySelector('link[href*="icon-fallback.css"]')) {
                const fallbackCSS = document.createElement('link');
                fallbackCSS.rel = 'stylesheet';
                fallbackCSS.href = '/static/css/icon-fallback.css';
                document.head.appendChild(fallbackCSS);
            }
        }
        
        return fontAwesomeLoaded;
    }
    
    function initIconFallback() {
        // Verificar imediatamente
        const loaded = checkFontAwesome();
        
        if (!loaded) {
            // Tentar novamente após um delay (caso o CDN esteja lento)
            setTimeout(() => {
                const retryLoaded = checkFontAwesome();
                if (!retryLoaded) {
                    console.log('ℹ️ Usando ícones emoji como fallback');
                }
            }, 2000);
        }
    }
    
    // Executar quando o DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initIconFallback);
    } else {
        initIconFallback();
    }
    
    // Executar também quando a página terminar de carregar completamente
    window.addEventListener('load', () => {
        setTimeout(initIconFallback, 500);
    });
})();