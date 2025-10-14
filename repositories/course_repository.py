# repositories/course_repository.py
# Repositório para gerenciamento de dados de cursos

import os
from typing import Dict, List, Optional
from datetime import datetime
from config import Config
from scripts.csv_generator import generate_csv
from scripts.pdf_generator import generate_pdf
from scripts.csv_reader import read_csv_files, get_course_by_id
from scripts.id_manager import get_next_id

class CourseRepository:
    """Repositório para operações com dados de cursos"""
    
    def __init__(self):
        self.csv_dir = Config.CSV_DIR
        self.pdf_dir = Config.PDF_DIR
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Garante que os diretórios necessários existam"""
        for directory in [self.csv_dir, self.pdf_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def save_course(self, course_data: Dict) -> Dict:
        """
        Salva um curso e gera os arquivos correspondentes
        
        Args:
            course_data: Dados do curso
            
        Returns:
            Dict: Dados do curso com ID e timestamps atualizados
        """
        # Obter próximo ID
        course_data['id'] = get_next_id()
        course_data['created_at'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        # Gerar arquivos CSV e PDF
        try:
            csv_path = generate_csv(course_data)
            pdf_path = generate_pdf(course_data)
            
            course_data['csv_file'] = os.path.basename(csv_path)
            course_data['pdf_file'] = os.path.basename(pdf_path)
            
            print(f"Arquivos gerados com sucesso para curso {course_data['id']}: CSV={csv_path}, PDF={pdf_path}")
            
        except Exception as e:
            # Log detalhado do erro
            print(f"ERRO ao gerar arquivos para curso {course_data['id']}: {str(e)}")
            print(f"Tipo do erro: {type(e).__name__}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
            # Tentar gerar apenas CSV se PDF falhar
            try:
                csv_path = generate_csv(course_data)
                course_data['csv_file'] = os.path.basename(csv_path)
                course_data['pdf_file'] = None
                print(f"CSV gerado com sucesso, PDF falhou: {csv_path}")
            except Exception as csv_error:
                print(f"ERRO ao gerar CSV também: {str(csv_error)}")
                course_data['csv_file'] = None
                course_data['pdf_file'] = None
        
        return course_data
    
    def update_course(self, course_id: int, course_data: Dict) -> Dict:
        """
        Atualiza um curso existente
        
        Args:
            course_id: ID do curso
            course_data: Novos dados do curso
            
        Returns:
            Dict: Dados atualizados do curso
        """
        # Buscar curso existente
        existing_course = self.find_by_id(course_id)
        if not existing_course:
            raise ValueError(f"Curso com ID {course_id} não encontrado")
        
        # Manter dados originais importantes
        course_data['id'] = course_id
        course_data['created_at'] = existing_course.get('created_at', datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        course_data['updated_at'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        # Remover arquivos antigos antes de gerar novos (para evitar arquivos órfãos)
        self._cleanup_old_course_files(course_id, existing_course)
        
        # Gerar novos arquivos
        try:
            csv_path = generate_csv(course_data)
            pdf_path = generate_pdf(course_data)
            
            course_data['csv_file'] = os.path.basename(csv_path)
            course_data['pdf_file'] = os.path.basename(pdf_path)
            
            print(f"Arquivos atualizados para curso {course_id}: CSV={csv_path}, PDF={pdf_path}")
            
        except Exception as e:
            print(f"Erro ao gerar arquivos para curso {course_id}: {str(e)}")
            course_data['csv_file'] = existing_course.get('csv_file')
            course_data['pdf_file'] = existing_course.get('pdf_file')
        
        return course_data
    
    def find_by_id(self, course_id: int) -> Optional[Dict]:
        """
        Busca um curso pelo ID
        
        Args:
            course_id: ID do curso
            
        Returns:
            Dict ou None: Dados do curso ou None se não encontrado
        """
        return get_course_by_id(course_id)
    
    def find_all(self) -> List[Dict]:
        """
        Lista todos os cursos
        
        Returns:
            List[Dict]: Lista de todos os cursos
        """
        return read_csv_files()
    
    def delete_course(self, course_id: int) -> bool:
        """
        Exclui um curso e seus arquivos
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se excluído com sucesso
        """
        course = self.find_by_id(course_id)
        if not course:
            return False
        
        # Excluir arquivos CSV e PDF usando o ID do curso para busca mais precisa
        course_id_str = str(course_id)
        
        # Excluir arquivos CSV (buscar por ID no nome do arquivo)
        csv_files = [f for f in os.listdir(self.csv_dir) if f"_{course_id_str}_" in f or f.startswith(f"{course_id_str}_")]
        for csv_file in csv_files:
            try:
                os.remove(os.path.join(self.csv_dir, csv_file))
                print(f"Arquivo CSV excluído: {csv_file}")
            except Exception as e:
                print(f"Erro ao excluir arquivo CSV {csv_file}: {str(e)}")
        
        # Excluir arquivos PDF (buscar por ID no nome do arquivo)
        pdf_files = [f for f in os.listdir(self.pdf_dir) if f"_{course_id_str}_" in f or f.startswith(f"{course_id_str}_")]
        for pdf_file in pdf_files:
            try:
                os.remove(os.path.join(self.pdf_dir, pdf_file))
                print(f"Arquivo PDF excluído: {pdf_file}")
            except Exception as e:
                print(f"Erro ao excluir arquivo PDF {pdf_file}: {str(e)}")
        
        # Fallback: tentar excluir por nome do arquivo também (para compatibilidade com arquivos antigos)
        titulo_formatado = course['titulo'].replace(' ', '_').replace('/', '_').replace('\\', '_')
        
        # Buscar arquivos antigos sem ID no nome
        old_csv_files = [f for f in os.listdir(self.csv_dir) if titulo_formatado in f and f"_{course_id_str}_" not in f]
        for csv_file in old_csv_files:
            try:
                os.remove(os.path.join(self.csv_dir, csv_file))
                print(f"Arquivo CSV antigo excluído: {csv_file}")
            except Exception as e:
                print(f"Erro ao excluir arquivo CSV antigo {csv_file}: {str(e)}")
        
        old_pdf_files = [f for f in os.listdir(self.pdf_dir) if titulo_formatado in f and f"_{course_id_str}_" not in f]
        for pdf_file in old_pdf_files:
            try:
                os.remove(os.path.join(self.pdf_dir, pdf_file))
                print(f"Arquivo PDF antigo excluído: {pdf_file}")
            except Exception as e:
                print(f"Erro ao excluir arquivo PDF antigo {pdf_file}: {str(e)}")
        
        return True
    
    def search_courses(self, query: str) -> List[Dict]:
        """
        Busca cursos por texto
        
        Args:
            query: Texto de busca
            
        Returns:
            List[Dict]: Lista de cursos que correspondem à busca
        """
        all_courses = self.find_all()
        query_lower = query.lower()
        
        matching_courses = []
        for course in all_courses:
            # Buscar no título, descrição e tema
            searchable_text = f"{course.get('titulo', '')} {course.get('descricao', '')} {course.get('tema', '')}".lower()
            if query_lower in searchable_text:
                matching_courses.append(course)
        
        return matching_courses
    
    def get_courses_by_modality(self, modality: str) -> List[Dict]:
        """
        Busca cursos por modalidade
        
        Args:
            modality: Modalidade do curso
            
        Returns:
            List[Dict]: Lista de cursos da modalidade especificada
        """
        all_courses = self.find_all()
        return [course for course in all_courses if course.get('modalidade') == modality]
    
    def get_courses_by_orgao(self, orgao: str) -> List[Dict]:
        """
        Busca cursos por órgão responsável
        
        Args:
            orgao: Órgão responsável
            
        Returns:
            List[Dict]: Lista de cursos do órgão especificado
        """
        all_courses = self.find_all()
        return [course for course in all_courses if course.get('orgao') == orgao]
    
    def find_by_id(self, course_id: int) -> Optional[Dict]:
        """
        Busca um curso pelo ID
        
        Args:
            course_id: ID do curso
            
        Returns:
            Dict ou None: Dados do curso se encontrado
        """
        try:
            from scripts.csv_reader import get_course_by_id
            return get_course_by_id(course_id)
        except Exception as e:
            print(f"Erro ao buscar curso por ID {course_id}: {str(e)}")
            return None
    
    def _cleanup_old_course_files(self, course_id: int, existing_course: Dict):
        """
        Remove arquivos antigos de um curso antes de gerar novos
        
        Args:
            course_id: ID do curso
            existing_course: Dados do curso existente
        """
        try:
            course_id_str = str(course_id)
            
            # Buscar e remover arquivos CSV antigos
            old_csv_files = []
            
            # Buscar por ID no nome do arquivo (formato novo)
            for f in os.listdir(self.csv_dir):
                if f"_{course_id_str}_" in f and f.endswith('.csv'):
                    old_csv_files.append(f)
            
            # Buscar por nome do título (formato antigo - compatibilidade)
            if existing_course.get('titulo'):
                titulo_formatado = existing_course['titulo'].replace(' ', '_').replace('/', '_').replace('\\', '_')
                for f in os.listdir(self.csv_dir):
                    if titulo_formatado in f and f.endswith('.csv') and f"_{course_id_str}_" not in f:
                        old_csv_files.append(f)
            
            # Remover arquivos CSV antigos
            for csv_file in old_csv_files:
                try:
                    os.remove(os.path.join(self.csv_dir, csv_file))
                    print(f"Arquivo CSV antigo removido: {csv_file}")
                except Exception as e:
                    print(f"Erro ao remover arquivo CSV antigo {csv_file}: {str(e)}")
            
            # Buscar e remover arquivos PDF antigos
            old_pdf_files = []
            
            # Buscar por ID no nome do arquivo (formato novo)
            for f in os.listdir(self.pdf_dir):
                if f"_{course_id_str}_" in f and f.endswith('.pdf'):
                    old_pdf_files.append(f)
            
            # Buscar por nome do título (formato antigo - compatibilidade)
            if existing_course.get('titulo'):
                titulo_formatado = existing_course['titulo'].replace(' ', '_').replace('/', '_').replace('\\', '_')
                for f in os.listdir(self.pdf_dir):
                    if titulo_formatado in f and f.endswith('.pdf') and f"_{course_id_str}_" not in f:
                        old_pdf_files.append(f)
            
            # Remover arquivos PDF antigos
            for pdf_file in old_pdf_files:
                try:
                    os.remove(os.path.join(self.pdf_dir, pdf_file))
                    print(f"Arquivo PDF antigo removido: {pdf_file}")
                except Exception as e:
                    print(f"Erro ao remover arquivo PDF antigo {pdf_file}: {str(e)}")
                    
        except Exception as e:
            print(f"Erro na limpeza de arquivos antigos para curso {course_id}: {str(e)}")