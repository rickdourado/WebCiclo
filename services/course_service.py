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
        modalidade = form_data.get('modalidade', '')
        
        # Processar campos de array baseado na modalidade
        course_data = {
            'titulo': form_data.get('titulo', '').strip(),
            'descricao_original': form_data.get('descricao', '').strip(),
            'inicio_inscricoes': f'{inicio_data.replace("-", "/")}' if inicio_data else '',
            'fim_inscricoes': f'{fim_data.replace("-", "/")}' if fim_data else '',
            'orgao': form_data.get('orgao', ''),
            'tema': form_data.get('tema', ''),
            'modalidade': modalidade,
        }
        
        # Campos específicos por modalidade
        if modalidade == 'Online':
            # Verificar se aulas são síncronas (assíncronas = "não")
            aulas_assincronas = form_data.get('aulas_assincronas', '')
            aulas_sincronas = aulas_assincronas == 'nao'
            
            # Campos específicos para Online
            course_data.update({
                'plataforma_digital': form_data.get('plataforma_digital', ''),
                'carga_horaria': form_data.get('carga_horaria', ''),
                'aulas_assincronas': aulas_assincronas,
                'dias_aula': '|'.join(list(dict.fromkeys(form_data.getlist('dias_aula_online[]')))) if hasattr(form_data, 'getlist') else form_data.get('dias_aula_online[]', ''),
                # Para cursos online, vagas_unidade deve vir do formulário
                'vagas_unidade': '|'.join([v.strip() for v in form_data.getlist('vagas_unidade[]') if v.strip()]) if hasattr(form_data, 'getlist') else form_data.get('vagas_unidade[]', '').strip(),
                # Campos de Presencial/Híbrido devem estar vazios para Online
                'endereco_unidade': '',
                'bairro_unidade': ''
            })
            
            # Datas de aula baseadas no tipo de aula
            if aulas_sincronas:
                # Para aulas síncronas, incluir datas de início e fim
                course_data.update({
                    'inicio_aulas_data': '|'.join([d for d in form_data.getlist('inicio_aulas_data[]') if d.strip()]) if hasattr(form_data, 'getlist') else form_data.get('inicio_aulas_data[]', ''),
                    'fim_aulas_data': '|'.join([d for d in form_data.getlist('fim_aulas_data[]') if d.strip()]) if hasattr(form_data, 'getlist') else form_data.get('fim_aulas_data[]', '')
                })
            else:
                # Para aulas assíncronas, datas devem estar vazias
                course_data.update({
                    'inicio_aulas_data': '',
                    'fim_aulas_data': ''
                })
            
            # Horários baseados no tipo de aula
            if aulas_sincronas:
                # Para aulas síncronas, incluir horários
                course_data.update({
                    'horario_inicio': '|'.join([h for h in form_data.getlist('horario_inicio[]') if h.strip()]) if hasattr(form_data, 'getlist') else form_data.get('horario_inicio[]', ''),
                    'horario_fim': '|'.join([h for h in form_data.getlist('horario_fim[]') if h.strip()]) if hasattr(form_data, 'getlist') else form_data.get('horario_fim[]', '')
                })
            else:
                # Para aulas assíncronas, horários devem estar vazios
                course_data.update({
                    'horario_inicio': '',
                    'horario_fim': ''
                })
        else:
            # Campos específicos para Presencial/Híbrido
            course_data.update({
                'endereco_unidade': '|'.join(form_data.getlist('endereco_unidade[]')) if hasattr(form_data, 'getlist') else form_data.get('endereco_unidade[]', ''),
                'bairro_unidade': '|'.join(form_data.getlist('bairro_unidade[]')) if hasattr(form_data, 'getlist') else form_data.get('bairro_unidade[]', ''),
                'vagas_unidade': '|'.join([v.strip() for v in form_data.getlist('vagas_unidade[]') if v.strip()]) if hasattr(form_data, 'getlist') else form_data.get('vagas_unidade[]', '').strip(),
                'inicio_aulas_data': '|'.join(form_data.getlist('inicio_aulas_data[]')) if hasattr(form_data, 'getlist') else form_data.get('inicio_aulas_data[]', ''),
                'fim_aulas_data': '|'.join(form_data.getlist('fim_aulas_data[]')) if hasattr(form_data, 'getlist') else form_data.get('fim_aulas_data[]', ''),
                'horario_inicio': '|'.join([h for h in form_data.getlist('horario_inicio[]') if h.strip()]) if hasattr(form_data, 'getlist') else form_data.get('horario_inicio[]', ''),
                'horario_fim': '|'.join([h for h in form_data.getlist('horario_fim[]') if h.strip()]) if hasattr(form_data, 'getlist') else form_data.get('horario_fim[]', ''),
                'dias_aula': '|'.join(list(dict.fromkeys(form_data.getlist('dias_aula_presencial[]')))) if hasattr(form_data, 'getlist') else form_data.get('dias_aula_presencial[]', ''),
                'carga_horaria': form_data.get('carga_horaria', ''),
                # Campos de Online devem estar vazios para Presencial/Híbrido
                'plataforma_digital': '',
                'aulas_assincronas': ''
            })
        
        # Campos comuns a todas as modalidades
        course_data.update({
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
            'parceiro_logo': '',
            'capa_curso': ''
        })
        
        return course_data
    
    def _process_uploaded_files(self, course_data: Dict, files: Dict):
        """Processa arquivos enviados"""
        # Processar logo do parceiro
        if course_data.get('parceiro_externo') == 'sim':
            partner_name = course_data.get('parceiro_nome', '')
            logo_file = files.get('parceiro_logo')
            
            if logo_file and partner_name:
                logo_filename = self.file_service.save_partner_logo(logo_file, partner_name)
                if logo_filename:
                    course_data['parceiro_logo'] = logo_filename
        
        # Processar capa do curso (com redimensionamento)
        cover_file = files.get('capa_curso')
        if cover_file:
            course_title = course_data.get('titulo', '')
            if course_title:
                # Salvar e redimensionar imagem
                cover_filename = self.file_service.save_course_cover(cover_file, course_title)
                
                if cover_filename:
                    course_data['capa_curso'] = cover_filename
                    print(f"✅ Capa do curso salva: {cover_filename}")
                else:
                    print(f"❌ Erro ao salvar capa do curso")
    
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
    def get_course_by_id(self, course_id: int) -> Optional[Dict]:
        """
        Busca um curso pelo ID
        
        Args:
            course_id: ID do curso
            
        Returns:
            Dict ou None: Dados do curso se encontrado
        """
        try:
            return self.repository.find_by_id(course_id)
        except Exception as e:
            print(f"Erro ao buscar curso {course_id}: {str(e)}")
            return None
    
    def prepare_course_for_duplication(self, course_data: Dict) -> Dict:
        """
        Prepara dados de um curso para duplicação, removendo campos que não devem ser copiados
        
        Args:
            course_data: Dados do curso original
            
        Returns:
            Dict: Dados preparados para duplicação
        """
        if not course_data:
            return {}
        
        # Campos que NÃO devem ser copiados (ficarão em branco)
        fields_to_clear = [
            'id', 'titulo', 'descricao_original', 'descricao', 
            'created_at', 'csv_file', 'pdf_file',
            'capa_curso'  # Logo pode ser mantido se quiserem
        ]
        
        # Criar cópia dos dados
        duplicate_data = course_data.copy()
        
        # Limpar campos que não devem ser copiados
        for field in fields_to_clear:
            duplicate_data[field] = ''
        
        # Adicionar prefixo ao título para indicar que é uma cópia
        original_title = course_data.get('titulo', '')
        if original_title:
            duplicate_data['titulo_original'] = f"Cópia de: {original_title}"
        
        # Processar dados de múltiplas unidades (igual ao template de edição)
        modalidade = duplicate_data.get('modalidade', '').lower()
        if modalidade == 'presencial' or modalidade == 'híbrido':
            # Processar dados de múltiplas unidades separados por |
            enderecos = duplicate_data.get('endereco_unidade', '').split('|') if duplicate_data.get('endereco_unidade') else ['']
            bairros = duplicate_data.get('bairro_unidade', '').split('|') if duplicate_data.get('bairro_unidade') else ['']
            vagas = duplicate_data.get('vagas_unidade', '').split('|') if duplicate_data.get('vagas_unidade') else ['']
            inicio_aulas = duplicate_data.get('inicio_aulas_data', '').split('|') if duplicate_data.get('inicio_aulas_data') else ['']
            fim_aulas = duplicate_data.get('fim_aulas_data', '').split('|') if duplicate_data.get('fim_aulas_data') else ['']
            horario_inicio = duplicate_data.get('horario_inicio', '').split('|') if duplicate_data.get('horario_inicio') else ['']
            horario_fim = duplicate_data.get('horario_fim', '').split('|') if duplicate_data.get('horario_fim') else ['']
            dias_aula = duplicate_data.get('dias_aula', '').split('|') if duplicate_data.get('dias_aula') else ['']
            
            # Arrays para múltiplas unidades (usado pelo template)
            duplicate_data['enderecos_unidades'] = enderecos
            duplicate_data['bairros_unidades'] = bairros
            duplicate_data['vagas_unidades'] = vagas
            duplicate_data['inicio_aulas_unidades'] = inicio_aulas
            duplicate_data['fim_aulas_unidades'] = fim_aulas
            duplicate_data['horario_inicio_unidades'] = horario_inicio
            duplicate_data['horario_fim_unidades'] = horario_fim
            duplicate_data['dias_aula_unidades'] = dias_aula
            
            # Converter datas para formato HTML (YYYY-MM-DD)
            inicio_aulas_converted = []
            fim_aulas_converted = []
            
            for data in inicio_aulas:
                if data:
                    converted = self._convert_date_to_html_format(data)
                    inicio_aulas_converted.append(converted)
                else:
                    inicio_aulas_converted.append('')
            
            for data in fim_aulas:
                if data:
                    converted = self._convert_date_to_html_format(data)
                    fim_aulas_converted.append(converted)
                else:
                    fim_aulas_converted.append('')
            
            # Atualizar arrays com datas convertidas
            duplicate_data['inicio_aulas_unidades'] = inicio_aulas_converted
            duplicate_data['fim_aulas_unidades'] = fim_aulas_converted
            
            print(f"🔄 Preparando {len(enderecos)} unidades para duplicação:")
            for i, endereco in enumerate(enderecos):
                print(f"   Unidade {i+1}: {endereco} - {bairros[i] if i < len(bairros) else ''}")
                print(f"      Início: {inicio_aulas_converted[i] if i < len(inicio_aulas_converted) else ''}")
                print(f"      Fim: {fim_aulas_converted[i] if i < len(fim_aulas_converted) else ''}")
        
        return duplicate_data 
   
    def _convert_date_to_html_format(self, date_string: str) -> str:
        """
        Converte data para formato HTML (YYYY-MM-DD)
        
        Args:
            date_string: Data em formato DD/MM/YYYY ou YYYY-MM-DD
            
        Returns:
            str: Data no formato YYYY-MM-DD
        """
        if not date_string:
            return ''
        
        # Se já está no formato correto (YYYY-MM-DD)
        import re
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
            return date_string
        
        # Se está no formato DD/MM/YYYY
        if '/' in date_string:
            try:
                parts = date_string.split('/')
                if len(parts) == 3:
                    dia, mes, ano = parts
                    return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
            except:
                pass
        
        # Se está no formato DD-MM-YYYY
        if '-' in date_string and len(date_string.split('-')[0]) <= 2:
            try:
                parts = date_string.split('-')
                if len(parts) == 3:
                    dia, mes, ano = parts
                    return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
            except:
                pass
        
        return date_string