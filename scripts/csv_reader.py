# csv_reader.py
# Módulo para leitura de arquivos CSV dos cursos

import csv
import os
import glob
from datetime import datetime

def read_csv_files():
    """
    Lê todos os arquivos CSV na pasta CSV e retorna uma lista de cursos.
    
    Returns:
        list: Lista de dicionários contendo os dados dos cursos.
    """
    # Diretório onde os arquivos CSV estão armazenados
    csv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CSV')
    
    if not os.path.exists(csv_dir):
        print(f"Diretório CSV não encontrado: {csv_dir}")
        return []
    
    courses = []
    csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
    
    # Ignorar arquivos de teste
    csv_files = [f for f in csv_files if not os.path.basename(f).startswith('teste')]
    
    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Adicionar o nome do arquivo como referência
                    # O ID agora está no conteúdo do CSV, não no nome do arquivo
                    row['file_id'] = row.get('id', '')
                    courses.append(row)
        except Exception as e:
            print(f"Erro ao ler arquivo {csv_file}: {str(e)}")
    
    # Ordenar por data de criação (mais recente primeiro)
    courses.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return courses

def get_course_by_id(course_id):
    """
    Busca um curso específico pelo ID.
    
    Args:
        course_id (int): ID do curso a ser buscado.
        
    Returns:
        dict: Dados do curso encontrado ou None se não encontrado.
    """
    courses = read_csv_files()
    
    for course in courses:
        if course.get('id') == str(course_id) or course.get('file_id') == str(course_id):
            return course
    
    return None