# id_manager.py
# Módulo para gerenciamento de IDs dos arquivos CSV e PDF

import os
import json
import glob

# Arquivo para armazenar o último ID utilizado
ID_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'last_id.json')

def get_existing_ids():
    """
    Obtém todos os IDs existentes nos arquivos CSV.
    
    Returns:
        set: Conjunto de IDs existentes.
    """
    existing_ids = set()
    csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'CSV')
    
    if os.path.exists(csv_dir):
        csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
        for csv_file in csv_files:
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) > 1:  # Se há pelo menos uma linha de dados
                        # Pegar o ID da segunda linha (primeira linha de dados)
                        data_line = lines[1].strip()
                        if data_line:
                            # Dividir por vírgula e pegar o penúltimo campo (ID)
                            fields = data_line.split(',')
                            if len(fields) >= 2:
                                try:
                                    course_id = int(fields[-2])  # Penúltimo campo
                                    existing_ids.add(course_id)
                                except (ValueError, IndexError):
                                    pass
            except Exception as e:
                print(f"Erro ao ler arquivo {csv_file}: {str(e)}")
    
    return existing_ids

def get_next_id():
    """
    Obtém o próximo ID disponível para arquivos CSV e PDF.
    Verifica se o ID já existe para evitar duplicatas.
    
    Returns:
        int: O próximo ID disponível.
    """
    # Obter IDs existentes
    existing_ids = get_existing_ids()
    
    # Começar com o último ID salvo
    last_id = 0
    try:
        if os.path.exists(ID_FILE):
            with open(ID_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    last_id = data.get('last_id', 0)
                except json.JSONDecodeError:
                    pass
    except FileNotFoundError:
        pass
    
    # Encontrar o próximo ID disponível
    next_id = last_id + 1
    while next_id in existing_ids:
        next_id += 1
    
    # Salvar o novo ID
    with open(ID_FILE, 'w') as f:
        json.dump({'last_id': next_id}, f)
    
    return next_id

def get_current_id():
    """
    Obtém o ID atual sem incrementá-lo.
    
    Returns:
        int: O ID atual.
    """
    try:
        if os.path.exists(ID_FILE):
            with open(ID_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    return data.get('last_id', 0)
                except json.JSONDecodeError:
                    return 0
    except FileNotFoundError:
        return 0
    
    return 0