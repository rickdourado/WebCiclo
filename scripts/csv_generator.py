# csv_generator.py
# Módulo para geração de arquivos CSV a partir dos dados do curso

import csv
import os
from datetime import datetime

def generate_csv(course_data):
    """
    Gera um arquivo CSV com os dados do curso.
    
    Args:
        course_data (dict): Dicionário contendo os dados do curso.
        
    Returns:
        str: Caminho do arquivo CSV gerado.
    """
    # Criar diretório CSV se não existir
    csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'CSV')
    print(f"Diretório CSV: {csv_dir}")
    if not os.path.exists(csv_dir):
        print(f"Criando diretório CSV: {csv_dir}")
        os.makedirs(csv_dir)
    
    # Gerar nome do arquivo baseado no ID do curso e timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"curso_{course_data['id']}_{timestamp}.csv"
    filepath = os.path.join(csv_dir, filename)
    print(f"Caminho completo do arquivo CSV: {filepath}")
    
    # Escrever dados no arquivo CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = course_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow(course_data)
    
    return filepath