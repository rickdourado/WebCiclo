# services/course_status_service.py
# Serviço para gerenciar o status de inserção dos cursos no sistema

from typing import Set
from repositories.course_repository_mysql import CourseRepositoryMySQL
import logging

logger = logging.getLogger(__name__)

class CourseStatusService:
    """Serviço para gerenciar quais cursos já foram inseridos no sistema"""
    
    def __init__(self):
        """Inicializa o serviço com o repository MySQL"""
        self.repository = CourseRepositoryMySQL()
        logger.info("CourseStatusService inicializado com MySQL repository")
    
    def mark_as_inserted(self, course_id: int) -> bool:
        """
        Marca um curso como inserido no sistema
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se marcado com sucesso
        """
        return self.repository.mark_as_inserted(course_id)
    
    def unmark_as_inserted(self, course_id: int) -> bool:
        """
        Desmarca um curso como inserido no sistema
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se desmarcado com sucesso
        """
        return self.repository.unmark_as_inserted(course_id)
    
    def is_course_inserted(self, course_id: int) -> bool:
        """
        Verifica se um curso está marcado como inserido
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se o curso está marcado como inserido
        """
        return self.repository.is_course_inserted(course_id)
    
    def get_inserted_courses(self) -> Set[int]:
        """
        Retorna o conjunto de IDs dos cursos marcados como inseridos
        
        Returns:
            Set[int]: Conjunto de IDs dos cursos inseridos
        """
        return self.repository.get_inserted_courses()
    
    def toggle_course_status(self, course_id: int) -> bool:
        """
        Alterna o status de inserção de um curso
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: Novo status do curso (True = inserido, False = não inserido)
        """
        if self.is_course_inserted(course_id):
            self.unmark_as_inserted(course_id)
            return False
        else:
            self.mark_as_inserted(course_id)
            return True
    
    def get_status_summary(self) -> dict:
        """
        Retorna um resumo do status dos cursos
        
        Returns:
            dict: Resumo com total de cursos inseridos
        """
        inserted_courses = self.get_inserted_courses()
        return {
            'total_inserted': len(inserted_courses),
            'inserted_ids': list(inserted_courses)
        }