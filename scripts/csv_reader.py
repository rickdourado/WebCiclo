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
                valid_rows = []
                for row in reader:
                    # Verificar se a linha tem todos os campos necessários
                    if row and 'id' in row and 'titulo' in row:
                        # Adicionar o nome do arquivo como referência
                        row['file_id'] = row.get('id', '')
                        row['source_file'] = os.path.basename(csv_file)
                        valid_rows.append(row)
                
                # Se houver linhas válidas, adicionar apenas a última (mais completa)
                if valid_rows:
                    courses.append(valid_rows[-1])
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
    
    # Converter course_id para string para comparação
    course_id_str = str(course_id)
    
    # Imprimir informações de debug
    print(f"Buscando curso com ID: {course_id_str}")
    print(f"Total de cursos encontrados: {len(courses)}")
    
    # Filtrar cursos com o ID correto
    matching_courses = []
    for course in courses:
        course_id_value = course.get('id')
        file_id_value = course.get('file_id')
        print(f"Verificando curso: ID={course_id_value}, file_id={file_id_value}, titulo={course.get('titulo')}")
        
        if course_id_value == course_id_str or file_id_value == course_id_str:
            matching_courses.append(course)
    
    if matching_courses:
        # Se encontrou mais de um curso com o mesmo ID, use o mais recente
        # (primeiro da lista, já que read_csv_files ordena por data de criação decrescente)
        selected_course = matching_courses[0]
        print(f"Curso encontrado: {selected_course.get('titulo')} (ID: {selected_course.get('id')})")
        return selected_course
    
    print(f"Nenhum curso encontrado com ID: {course_id_str}")
    return None