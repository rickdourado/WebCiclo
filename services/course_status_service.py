# services/course_status_service.py
# Serviço para gerenciar o status de inserção dos cursos no sistema

import json
import os
from typing import Dict, Set
from config import Config

class CourseStatusService:
    """Serviço para gerenciar quais cursos já foram inseridos no sistema"""
    
    def __init__(self):
        self.status_file = os.path.join(os.path.dirname(Config.CSV_DIR), 'course_status.json')
        self._ensure_status_file()
    
    def _ensure_status_file(self):
        """Garante que o arquivo de status existe"""
        if not os.path.exists(self.status_file):
            self._save_status({})
    
    def _load_status(self) -> Dict[str, bool]:
        """Carrega o status dos cursos do arquivo JSON"""
        try:
            with open(self.status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_status(self, status_data: Dict[str, bool]):
        """Salva o status dos cursos no arquivo JSON"""
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar status dos cursos: {str(e)}")
    
    def mark_course_as_inserted(self, course_id: int) -> bool:
        """
        Marca um curso como inserido no sistema
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se marcado com sucesso
        """
        try:
            status_data = self._load_status()
            status_data[str(course_id)] = True
            self._save_status(status_data)
            return True
        except Exception as e:
            print(f"Erro ao marcar curso {course_id} como inserido: {str(e)}")
            return False
    
    def unmark_course_as_inserted(self, course_id: int) -> bool:
        """
        Desmarca um curso como inserido no sistema
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se desmarcado com sucesso
        """
        try:
            status_data = self._load_status()
            if str(course_id) in status_data:
                del status_data[str(course_id)]
                self._save_status(status_data)
            return True
        except Exception as e:
            print(f"Erro ao desmarcar curso {course_id}: {str(e)}")
            return False
    
    def is_course_inserted(self, course_id: int) -> bool:
        """
        Verifica se um curso está marcado como inserido
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se o curso está marcado como inserido
        """
        status_data = self._load_status()
        return status_data.get(str(course_id), False)
    
    def get_inserted_courses(self) -> Set[int]:
        """
        Retorna o conjunto de IDs dos cursos marcados como inseridos
        
        Returns:
            Set[int]: Conjunto de IDs dos cursos inseridos
        """
        status_data = self._load_status()
        return {int(course_id) for course_id in status_data.keys() if status_data[course_id]}
    
    def toggle_course_status(self, course_id: int) -> bool:
        """
        Alterna o status de inserção de um curso
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: Novo status do curso (True = inserido, False = não inserido)
        """
        if self.is_course_inserted(course_id):
            self.unmark_course_as_inserted(course_id)
            return False
        else:
            self.mark_course_as_inserted(course_id)
            return True
    
    def get_status_summary(self) -> Dict[str, int]:
        """
        Retorna um resumo do status dos cursos
        
        Returns:
            Dict[str, int]: Resumo com total de cursos inseridos
        """
        inserted_courses = self.get_inserted_courses()
        return {
            'total_inserted': len(inserted_courses),
            'inserted_ids': list(inserted_courses)
        }