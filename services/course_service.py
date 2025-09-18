# services/course_service.py
# Serviço de negócio para cursos

from typing import Dict, List, Optional, Tuple
from repositories.course_repository import CourseRepository
from services.validation_service import CourseValidator, ValidationError
from services.ai_service import AIService
from services.file_service import FileService

class CourseService:
    """Serviço de negócio para operações com cursos"""
    
    def __init__(self):
        self.repository = CourseRepository()
        self.validator = CourseValidator()
        self.ai_service = AIService()
        self.file_service = FileService()
    
    def create_course(self, form_data: Dict, files: Dict = None) -> Tuple[bool, Dict, List[str]]:
        """
        Cria um novo curso
        
        Args:
            form_data: Dados do formulário
            files: Arquivos enviados (logos, etc.)
            
        Returns:
            Tuple[bool, Dict, List[str]]: (sucesso, dados_curso, erros)
        """
        try:
            # Validar dados
            is_valid, errors, warnings = self.validator.validate_course_data(form_data)
            if not is_valid:
                return False, {}, errors
            
            # Processar dados do formulário
            course_data = self._process_form_data(form_data)
            
            # Processar arquivos se fornecidos
            if files:
                self._process_uploaded_files(course_data, files)
            
            # Melhorar descrição com IA
            course_data = self._enhance_description(course_data)
            
            # Salvar curso
            saved_course = self.repository.save_course(course_data)
            
            return True, saved_course, warnings
            
        except Exception as e:
            return False, {}, [f"Erro interno: {str(e)}"]
    
    def update_course(self, course_id: int, form_data: Dict, files: Dict = None) -> Tuple[bool, Dict, List[str]]:
        """
        Atualiza um curso existente
        
        Args:
            course_id: ID do curso
            form_data: Novos dados do formulário
            files: Novos arquivos enviados
            
        Returns:
            Tuple[bool, Dict, List[str]]: (sucesso, dados_curso, erros)
        """
        try:
            # Verificar se curso existe
            existing_course = self.repository.find_by_id(course_id)
            if not existing_course:
                return False, {}, ["Curso não encontrado"]
            
            # Validar dados
            is_valid, errors, warnings = self.validator.validate_course_data(form_data)
            if not is_valid:
                return False, {}, errors
            
            # Processar dados do formulário
            course_data = self._process_form_data(form_data)
            
            # Processar arquivos se fornecidos
            if files:
                self._process_uploaded_files(course_data, files)
            else:
                # Manter arquivos existentes
                course_data['parceiro_logo'] = existing_course.get('parceiro_logo', '')
            
            # Melhorar descrição se foi alterada
            if course_data.get('descricao_original') != existing_course.get('descricao_original'):
                course_data = self._enhance_description(course_data)
            else:
                course_data['descricao'] = existing_course.get('descricao', course_data.get('descricao_original'))
            
            # Atualizar curso
            updated_course = self.repository.update_course(course_id, course_data)
            
            return True, updated_course, warnings
            
        except Exception as e:
            return False, {}, [f"Erro interno: {str(e)}"]
    
    def get_course(self, course_id: int) -> Optional[Dict]:
        """Busca um curso pelo ID"""
        return self.repository.find_by_id(course_id)
    
    def list_courses(self, search_query: str = None, modality: str = None, orgao: str = None) -> List[Dict]:
        """
        Lista cursos com filtros opcionais
        
        Args:
            search_query: Texto de busca
            modality: Modalidade do curso
            orgao: Órgão responsável
            
        Returns:
            List[Dict]: Lista de cursos filtrados
        """
        if search_query:
            return self.repository.search_courses(search_query)
        elif modality:
            return self.repository.get_courses_by_modality(modality)
        elif orgao:
            return self.repository.get_courses_by_orgao(orgao)
        else:
            return self.repository.find_all()
    
    def delete_course(self, course_id: int) -> Tuple[bool, str]:
        """
        Exclui um curso
        
        Args:
            course_id: ID do curso
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            success = self.repository.delete_course(course_id)
            if success:
                return True, "Curso excluído com sucesso"
            else:
                return False, "Curso não encontrado"
        except Exception as e:
            return False, f"Erro ao excluir curso: {str(e)}"
    
    def _process_form_data(self, form_data: Dict) -> Dict:
        """Processa e transforma dados do formulário"""
        # Converter datas
        inicio_data = form_data.get('inicio_inscricoes_data')
        fim_data = form_data.get('fim_inscricoes_data')
        
        # Processar campos de array
        course_data = {
            'titulo': form_data.get('titulo', '').strip(),
            'descricao_original': form_data.get('descricao', '').strip(),
            'inicio_inscricoes': f'{inicio_data.replace("-", "/")}' if inicio_data else '',
            'fim_inscricoes': f'{fim_data.replace("-", "/")}' if fim_data else '',
            'orgao': form_data.get('orgao', ''),
            'tema': form_data.get('tema', ''),
            'modalidade': form_data.get('modalidade', ''),
            'plataforma_digital': form_data.get('plataforma_digital') if form_data.get('modalidade') == 'Online' else '',
            'carga_horaria': form_data.get('carga_horaria', ''),
            'aulas_assincronas': form_data.get('aulas_assincronas') if form_data.get('modalidade') == 'Online' else '',
            'dias_aula': '|'.join(form_data.getlist('dias_aula[]')) if hasattr(form_data, 'getlist') else form_data.get('dias_aula[]', ''),
            'endereco_unidade': '|'.join(form_data.getlist('endereco_unidade[]')) if hasattr(form_data, 'getlist') else form_data.get('endereco_unidade[]', ''),
            'bairro_unidade': '|'.join(form_data.getlist('bairro_unidade[]')) if hasattr(form_data, 'getlist') else form_data.get('bairro_unidade[]', ''),
            'vagas_unidade': '|'.join(form_data.getlist('vagas_unidade[]')) if hasattr(form_data, 'getlist') else form_data.get('vagas_unidade[]', ''),
            'inicio_aulas_data': '|'.join(form_data.getlist('inicio_aulas_data[]')) if hasattr(form_data, 'getlist') else form_data.get('inicio_aulas_data[]', ''),
            'fim_aulas_data': '|'.join(form_data.getlist('fim_aulas_data[]')) if hasattr(form_data, 'getlist') else form_data.get('fim_aulas_data[]', ''),
            'horario_inicio': '|'.join([h for h in form_data.getlist('horario_inicio[]') if h.strip()]) if hasattr(form_data, 'getlist') else form_data.get('horario_inicio[]', ''),
            'horario_fim': '|'.join([h for h in form_data.getlist('horario_fim[]') if h.strip()]) if hasattr(form_data, 'getlist') else form_data.get('horario_fim[]', ''),
            'curso_gratuito': form_data.get('curso_gratuito', ''),
            'valor_curso': form_data.get('valor_curso') if form_data.get('curso_gratuito') == 'nao' else '',
            'valor_curso_inteira': form_data.get('valor_curso_inteira') if form_data.get('curso_gratuito') == 'nao' else '',
            'valor_curso_meia': form_data.get('valor_curso_meia') if form_data.get('curso_gratuito') == 'nao' else '',
            'requisitos_meia': form_data.get('requisitos_meia') if form_data.get('curso_gratuito') == 'nao' else '',
            'oferece_bolsa': form_data.get('oferece_bolsa', ''),
            'valor_bolsa': form_data.get('valor_bolsa') if form_data.get('oferece_bolsa') == 'sim' else '',
            'requisitos_bolsa': form_data.get('requisitos_bolsa') if form_data.get('oferece_bolsa') == 'sim' else '',
            'publico_alvo': form_data.get('publico_alvo', ''),
            'acessibilidade': form_data.get('acessibilidade', ''),
            'recursos_acessibilidade': form_data.get('recursos_acessibilidade') if form_data.get('acessibilidade') in ['acessivel', 'exclusivo'] else '',
            'oferece_certificado': form_data.get('oferece_certificado', ''),
            'pre_requisitos': form_data.get('pre_requisitos') if form_data.get('oferece_certificado') == 'sim' else '',
            'info_complementares': form_data.get('info_complementares', ''),
            'parceiro_externo': form_data.get('parceiro_externo', ''),
            'parceiro_nome': form_data.get('parceiro_nome') if form_data.get('parceiro_externo') == 'sim' else '',
            'parceiro_link': form_data.get('parceiro_link') if form_data.get('parceiro_externo') == 'sim' else '',
            'parceiro_logo': ''
        }
        
        return course_data
    
    def _process_uploaded_files(self, course_data: Dict, files: Dict):
        """Processa arquivos enviados"""
        if course_data.get('parceiro_externo') == 'sim':
            partner_name = course_data.get('parceiro_nome', '')
            logo_file = files.get('parceiro_logo')
            
            if logo_file and partner_name:
                logo_filename = self.file_service.save_partner_logo(logo_file, partner_name)
                if logo_filename:
                    course_data['parceiro_logo'] = logo_filename
    
    def _enhance_description(self, course_data: Dict) -> Dict:
        """Melhora a descrição usando IA"""
        try:
            original_description = course_data.get('descricao_original', '')
            if original_description:
                enhanced_description = self.ai_service.enhance_description(original_description)
                course_data['descricao'] = enhanced_description
            else:
                course_data['descricao'] = original_description
        except Exception as e:
            print(f"Erro ao melhorar descrição: {str(e)}")
            course_data['descricao'] = course_data.get('descricao_original', '')
        
        return course_data
