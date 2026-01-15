# scripts/__init__.py
# Este arquivo marca o diretório como um pacote Python

# Importar funções principais para facilitar o acesso
from .csv_generator import generate_csv
from .pdf_generator import generate_pdf
from .csv_reader import read_csv_files, get_course_by_id
from .id_manager import get_next_id, get_current_id