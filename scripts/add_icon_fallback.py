#!/usr/bin/env python3
# scripts/add_icon_fallback.py
"""
Script para adicionar sistema de fallback de ícones em todos os templates.
"""

import os
import re
from pathlib import Path

def add_fallback_to_template(template_path):
    """Adiciona sistema de fallback a um template específico"""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já tem o fallback
    if 'icon-fallback.css' in content:
        return False, "Fallback já presente"
    
    # Procurar pela linha do Font Awesome CDN
    fa_pattern = r'(<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]*">)'
    
    match = re.search(fa_pattern, content)
    if not match:
        return False, "Font Awesome CDN não encontrado"
    
    # Adicionar fallback após o Font Awesome
    fallback_lines = '''
    <link rel="stylesheet" href="{{ url_for('static', filename='css/icon-fallback.css') }}">
    <script src="{{ url_for('static', filename='js/icon-fallback.js') }}"></script>'''
    
    new_content = content.replace(
        match.group(1),
        match.group(1) + fallback_lines
    )
    
    # Salvar arquivo atualizado
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Fallback adicionado"

def main():
    """Adiciona fallback a todos os templates"""
    print("🔧 Adicionando sistema de fallback de ícones...")
    
    templates_dir = Path("templates")
    updated_files = []
    skipped_files = []
    
    for template_file in templates_dir.glob("*.html"):
        # Pular o template de teste
        if template_file.name == 'test_icons.html':
            continue
            
        success, message = add_fallback_to_template(template_file)
        
        if success:
            updated_files.append(template_file.name)
            print(f"✅ {template_file.name}: {message}")
        else:
            skipped_files.append((template_file.name, message))
            print(f"⚠️ {template_file.name}: {message}")
    
    print(f"\n📊 Resumo:")
    print(f"✅ Arquivos atualizados: {len(updated_files)}")
    print(f"⚠️ Arquivos ignorados: {len(skipped_files)}")
    
    if updated_files:
        print(f"\nArquivos atualizados:")
        for file in updated_files:
            print(f"  - {file}")
    
    if skipped_files:
        print(f"\nArquivos ignorados:")
        for file, reason in skipped_files:
            print(f"  - {file}: {reason}")

if __name__ == "__main__":
    main()