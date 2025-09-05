# id_manager.py
# Módulo para gerenciamento de IDs dos arquivos CSV e PDF

import os
import json

# Arquivo para armazenar o último ID utilizado
ID_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'last_id.json')

def get_next_id():
    """
    Obtém o próximo ID disponível para arquivos CSV e PDF.
    
    Returns:
        int: O próximo ID disponível.
    """
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
    
    next_id = last_id + 1
    
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