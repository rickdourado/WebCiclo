#!/usr/bin/env python3
# scripts/diagnose_icons.py
"""
Script para diagnosticar problemas com ícones Font Awesome.
Verifica templates, CSP, CDN e sintaxe HTML.
"""

import re
import os
from pathlib import Path

def check_font_awesome_cdn():
    """Verifica se o CDN do Font Awesome está nos templates"""
    print("🔍 Verificando CDN do Font Awesome...")
    
    templates_dir = Path("templates")
    font_awesome_pattern = r'font-awesome.*css'
    
    found_files = []
    for template_file in templates_dir.glob("*.html"):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(font_awesome_pattern, content):
                found_files.append(template_file.name)
    
    if found_files:
        print(f"✅ Font Awesome CDN encontrado em: {', '.join(found_files)}")
    else:
        print("❌ Font Awesome CDN não encontrado em nenhum template")
    
    return len(found_files) > 0

def check_icon_syntax():
    """Verifica sintaxe dos ícones nos templates"""
    print("\n🔍 Verificando sintaxe dos ícones...")
    
    templates_dir = Path("templates")
    icon_pattern = r'<i\s+class=["\']fas\s+fa-[^"\']*["\'][^>]*></i>'
    malformed_pattern = r'onclick=[^>]*<i\s+class='
    
    issues = []
    total_icons = 0
    
    for template_file in templates_dir.glob("*.html"):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Contar ícones válidos
            valid_icons = re.findall(icon_pattern, content)
            total_icons += len(valid_icons)
            
            # Procurar por sintaxe malformada
            malformed = re.findall(malformed_pattern, content)
            if malformed:
                issues.append(f"{template_file.name}: {len(malformed)} ícones malformados")
    
    print(f"✅ Total de ícones válidos encontrados: {total_icons}")
    
    if issues:
        print("❌ Problemas de sintaxe encontrados:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ Nenhum problema de sintaxe encontrado")
    
    return len(issues) == 0

def check_csp_policy():
    """Verifica a política CSP no app.py"""
    print("\n🔍 Verificando Content Security Policy...")
    
    try:
        with open("app.py", 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Procurar pela CSP
        csp_match = re.search(r'Content-Security-Policy["\'].*?=.*?\(\s*([^)]+)\)', content, re.DOTALL)
        
        if csp_match:
            csp_content = csp_match.group(1)
            
            # Verificar se permite cdnjs.cloudflare.com
            if 'cdnjs.cloudflare.com' in csp_content:
                print("✅ CSP permite cdnjs.cloudflare.com")
                
                # Verificar font-src especificamente
                if 'font-src' in csp_content and 'cdnjs.cloudflare.com' in csp_content:
                    print("✅ CSP permite fontes do cdnjs.cloudflare.com")
                else:
                    print("⚠️ CSP pode não permitir fontes do cdnjs.cloudflare.com")
                    
            else:
                print("❌ CSP não permite cdnjs.cloudflare.com")
                
        else:
            print("❌ CSP não encontrada no app.py")
            
    except Exception as e:
        print(f"❌ Erro ao verificar CSP: {e}")

def check_button_syntax():
    """Verifica sintaxe específica dos botões"""
    print("\n🔍 Verificando sintaxe dos botões...")
    
    templates_dir = Path("templates")
    button_issues = []
    
    for template_file in templates_dir.glob("*.html"):
        with open(template_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines, 1):
            # Procurar por botões malformados
            if 'onclick=' in line and '<i class=' in line:
                # Verificar se o onclick está fechado antes do ícone
                if re.search(r'onclick=[^>]*>\s*<i\s+class=', line):
                    continue  # Sintaxe correta
                elif re.search(r'onclick=[^>]*<i\s+class=', line):
                    button_issues.append(f"{template_file.name}:{i} - Botão malformado")
    
    if button_issues:
        print("❌ Problemas encontrados nos botões:")
        for issue in button_issues:
            print(f"  - {issue}")
    else:
        print("✅ Sintaxe dos botões está correta")
    
    return len(button_issues) == 0

def suggest_fixes():
    """Sugere correções para os problemas encontrados"""
    print("\n🔧 Sugestões de correção:")
    print("1. Verifique se o CDN do Font Awesome está carregando:")
    print("   - Abra o DevTools do navegador (F12)")
    print("   - Vá para a aba Network")
    print("   - Recarregue a página")
    print("   - Procure por 'font-awesome' nas requisições")
    
    print("\n2. Verifique a Console do navegador:")
    print("   - Procure por erros de CSP (Content Security Policy)")
    print("   - Procure por erros 404 do Font Awesome")
    
    print("\n3. Teste manual:")
    print("   - Inicie o servidor: python app.py")
    print("   - Acesse: http://localhost:5000")
    print("   - Verifique se os ícones aparecem")
    
    print("\n4. Se os ícones ainda não aparecerem:")
    print("   - Considere usar uma versão local do Font Awesome")
    print("   - Ou ajustar a CSP para ser menos restritiva")

def main():
    """Executa todos os diagnósticos"""
    print("🔍 DIAGNÓSTICO DE ÍCONES - WEBCICLO CARIOCA")
    print("=" * 50)
    
    cdn_ok = check_font_awesome_cdn()
    syntax_ok = check_icon_syntax()
    check_csp_policy()
    buttons_ok = check_button_syntax()
    
    print("\n" + "=" * 50)
    
    if cdn_ok and syntax_ok and buttons_ok:
        print("✅ Diagnóstico concluído - Nenhum problema óbvio encontrado")
        print("Se os ícones ainda não aparecem, o problema pode ser:")
        print("- Bloqueio de rede/firewall")
        print("- Problema com o CDN")
        print("- Cache do navegador")
    else:
        print("❌ Problemas encontrados - veja as sugestões abaixo")
    
    suggest_fixes()

if __name__ == "__main__":
    main()