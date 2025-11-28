import os
import glob
import sys

# Adicionar diretório pai ao path para importar app e repositories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from repositories.course_repository_mysql import CourseRepositoryMySQL

def update_database_files():
    """
    Varre os diretórios CSV e PDF e atualiza o banco de dados com os nomes dos arquivos encontrados.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_dir = os.path.join(base_dir, 'CSV')
    pdf_dir = os.path.join(base_dir, 'PDF')
    
    print(f"📂 Diretório CSV: {csv_dir}")
    print(f"📂 Diretório PDF: {pdf_dir}")
    
    # Listar arquivos CSV e PDF
    csv_files = {os.path.basename(f): f for f in glob.glob(os.path.join(csv_dir, '*.csv'))}
    pdf_files = {os.path.basename(f): f for f in glob.glob(os.path.join(pdf_dir, '*.pdf'))}

    print(f"📄 Arquivos CSV encontrados: {len(csv_files)}")
    print(f"📄 Arquivos PDF encontrados: {len(pdf_files)}")
    print("-" * 50)

    # Extrair IDs dos nomes dos arquivos
    # Formato esperado: YYYYMMDD_ID_Titulo.ext
    csv_by_id = {}
    for filename in csv_files.keys():
        parts = filename.split('_')
        if len(parts) >= 2:
            try:
                # Tenta pegar o ID da segunda parte (índice 1)
                course_id = int(parts[1])
                csv_by_id[course_id] = filename
            except ValueError:
                pass

    pdf_by_id = {}
    for filename in pdf_files.keys():
        parts = filename.split('_')
        if len(parts) >= 2:
            try:
                course_id = int(parts[1])
                pdf_by_id[course_id] = filename
            except ValueError:
                pass

    # Atualizar banco de dados
    with app.app_context():
        try:
            repo = CourseRepositoryMySQL()
            print("🔌 Conectado ao banco de dados MySQL")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            return
        
        updated_count = 0
        all_course_ids = set(list(csv_by_id.keys()) + list(pdf_by_id.keys()))
        
        print(f"🔄 Processando {len(all_course_ids)} cursos identificados nos arquivos...")
        
        for course_id in sorted(all_course_ids):
            csv_file = csv_by_id.get(course_id)
            pdf_file = pdf_by_id.get(course_id)
            
            try:
                # Atualizar usando o método update_course_files
                success = repo.update_course_files(
                    course_id=course_id,
                    csv_file=csv_file,
                    pdf_file=pdf_file
                )
                
                if success:
                    print(f"✅ Curso ID {course_id} atualizado:")
                    if csv_file:
                        print(f"   CSV: {csv_file}")
                    if pdf_file:
                        print(f"   PDF: {pdf_file}")
                    updated_count += 1
                else:
                    print(f"⚠️ Curso ID {course_id} não encontrado no banco de dados")
            except Exception as e:
                print(f"❌ Erro ao atualizar curso ID {course_id}: {e}")
        
        print("-" * 50)
        print(f"🎉 Concluído! Total de cursos atualizados: {updated_count}")

if __name__ == "__main__":
    print("🚀 Iniciando atualização de arquivos no banco de dados...")
    update_database_files()
