# services/validation_service.py
# Serviço de validação centralizada para o WebCiclo

import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from config import Config

class ValidationError(Exception):
    """Exceção personalizada para erros de validação"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class CourseValidator:
    """Validador centralizado para dados de cursos"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_course_data(self, form_data: Dict) -> Tuple[bool, List[str], List[str]]:
        """
        Valida todos os dados do curso
        
        Args:
            form_data: Dicionário com dados do formulário
            
        Returns:
            Tuple[bool, List[str], List[str]]: (é_válido, erros, avisos)
        """
        self.errors = []
        self.warnings = []
        
        # Validar campos básicos obrigatórios
        self._validate_basic_fields(form_data)
        
        # Validar campos condicionais
        self._validate_conditional_fields(form_data)
        
        # Validar modalidade específica
        self._validate_modality_fields(form_data)
        
        # Validar datas
        self._validate_dates(form_data)
        
        # Validar parceiro externo
        self._validate_external_partner(form_data)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_basic_fields(self, form_data: Dict):
        """Valida campos básicos obrigatórios"""
        required_fields = {
            'titulo': 'Nome do Curso',
            'descricao': 'Descrição',
            'orgao': 'Órgão Responsável',
            'tema': 'Tema/Categoria',
            'modalidade': 'Modalidade',
            'curso_gratuito': 'Curso Gratuito',
            'oferece_bolsa': 'Oferece Bolsa',
            'oferece_certificado': 'Oferece Certificado',
            'parceiro_externo': 'Parceiro Externo',
            'publico_alvo': 'Público Alvo',
            'acessibilidade': 'Acessibilidade'
        }
        
        for field, label in required_fields.items():
            value = form_data.get(field, '').strip()
            if not value:
                self.errors.append(f"{label} é obrigatório")
            elif field == 'titulo' and len(value) > Config.MAX_TITLE_LENGTH:
                self.errors.append(f"{label} deve ter no máximo {Config.MAX_TITLE_LENGTH} caracteres")
            elif field == 'descricao' and len(value) > Config.MAX_DESCRIPTION_LENGTH:
                self.errors.append(f"{label} deve ter no máximo {Config.MAX_DESCRIPTION_LENGTH} caracteres")
    
    def _validate_conditional_fields(self, form_data: Dict):
        """Valida campos condicionais baseados em outras seleções"""
        # Validar campos de curso pago
        if form_data.get('curso_gratuito') == 'nao':
            if not form_data.get('valor_curso_inteira'):
                self.errors.append("Valor inteira é obrigatório para cursos pagos")
            if form_data.get('valor_curso_meia') and not form_data.get('requisitos_meia'):
                self.errors.append("Condições para meia-entrada são obrigatórias quando valor meia é informado")
        
        # Validar campos de bolsa
        if form_data.get('oferece_bolsa') == 'sim':
            if not form_data.get('valor_bolsa'):
                self.errors.append("Valor da bolsa é obrigatório quando oferece bolsa")
            if not form_data.get('requisitos_bolsa'):
                self.errors.append("Requisitos para bolsa são obrigatórios quando oferece bolsa")
        
        # Validar campos de certificado
        if form_data.get('oferece_certificado') == 'sim':
            if not form_data.get('pre_requisitos'):
                self.errors.append("Pré-requisitos para certificado são obrigatórios quando oferece certificado")
        
        # Validar recursos de acessibilidade
        acessibilidade = form_data.get('acessibilidade')
        if acessibilidade in ['acessivel', 'exclusivo']:
            if not form_data.get('recursos_acessibilidade'):
                self.errors.append("Recursos de acessibilidade são obrigatórios quando o curso é acessível ou exclusivo para pessoas com deficiência")
    
    def _validate_modality_fields(self, form_data: Dict):
        """Valida campos específicos da modalidade"""
        modalidade = form_data.get('modalidade')
        
        if modalidade == 'Online':
            # Para Online, apenas vagas e carga horária são obrigatórios
            vagas_unidade = form_data.get('vagas_unidade[]') or form_data.get('vagas_unidade')
            if not vagas_unidade or (isinstance(vagas_unidade, list) and not any(vagas_unidade)):
                self.errors.append("Número de vagas é obrigatório para cursos online")
            
            carga_horaria = form_data.get('carga_horaria[]') or form_data.get('carga_horaria')
            if not carga_horaria or (isinstance(carga_horaria, list) and not any(carga_horaria)):
                self.errors.append("Carga horária é obrigatória para cursos online")
            
            # Verificar se aulas são síncronas (NÃO assíncronas)
            aulas_assincronas = form_data.get('aulas_assincronas')
            if aulas_assincronas == 'nao':
                # Para aulas síncronas, pelo menos um dia deve ser selecionado
                dias_aula = form_data.getlist('dias_aula[]') if hasattr(form_data, 'getlist') else form_data.get('dias_aula[]', [])
                if not dias_aula or len(dias_aula) == 0:
                    self.errors.append("Pelo menos um dia da semana é obrigatório para aulas síncronas online")
        else:
            # Para Presencial/Híbrido, validar unidades
            unidades_data = self._extract_units_data(form_data)
            if not unidades_data:
                self.errors.append("Pelo menos uma unidade é obrigatória para cursos presenciais/híbridos")
            else:
                self._validate_units(unidades_data)
    
    def _validate_units(self, unidades_data: List[Dict]):
        """Valida dados das unidades"""
        for i, unidade in enumerate(unidades_data, 1):
            if not unidade.get('endereco_unidade'):
                self.errors.append(f"Endereço da unidade {i} é obrigatório")
            if not unidade.get('bairro_unidade'):
                self.errors.append(f"Bairro da unidade {i} é obrigatório")
            if not unidade.get('vagas_unidade'):
                self.errors.append(f"Número de vagas da unidade {i} é obrigatório")
            if not unidade.get('dias_aula'):
                self.errors.append(f"Dias de aula da unidade {i} são obrigatórios")
    
    def _validate_dates(self, form_data: Dict):
        """Valida datas do formulário"""
        inicio_inscricoes = form_data.get('inicio_inscricoes_data')
        fim_inscricoes = form_data.get('fim_inscricoes_data')
        
        # Validar datas de inscrições
        if inicio_inscricoes and fim_inscricoes:
            try:
                inicio_insc = datetime.strptime(inicio_inscricoes, '%Y-%m-%d')
                fim_insc = datetime.strptime(fim_inscricoes, '%Y-%m-%d')
                
                if fim_insc < inicio_insc:
                    self.errors.append("O fim das inscrições deve ser posterior ou igual ao início das inscrições")
                
                # Verificar se as datas não são muito distantes no futuro
                hoje = datetime.now()
                if inicio_insc > datetime(hoje.year + 2, hoje.month, hoje.day):
                    self.warnings.append("Data de início das inscrições muito distante no futuro")
                    
            except ValueError:
                self.errors.append("Formato de data inválido")
        
        # Validar datas das aulas em relação às datas de inscrições
        self._validate_aulas_dates(form_data, inicio_inscricoes, fim_inscricoes)
    
    def _validate_aulas_dates(self, form_data: Dict, inicio_inscricoes: str, fim_inscricoes: str):
        """Valida datas das aulas em relação às datas de inscrições"""
        if not inicio_inscricoes or not fim_inscricoes:
            return
            
        try:
            inicio_insc = datetime.strptime(inicio_inscricoes, '%Y-%m-%d')
            fim_insc = datetime.strptime(fim_inscricoes, '%Y-%m-%d')
            
            # Verificar datas das unidades (modalidade Presencial/Híbrida)
            inicio_aulas_list = form_data.getlist('inicio_aulas_data[]') if hasattr(form_data, 'getlist') else [form_data.get('inicio_aulas_data[]', '')]
            fim_aulas_list = form_data.getlist('fim_aulas_data[]') if hasattr(form_data, 'getlist') else [form_data.get('fim_aulas_data[]', '')]
            
            for i, (inicio_aula, fim_aula) in enumerate(zip(inicio_aulas_list, fim_aulas_list), 1):
                if inicio_aula and fim_aula:
                    try:
                        inicio_aula_dt = datetime.strptime(inicio_aula.split(',')[0].strip(), '%Y-%m-%d')
                        fim_aula_dt = datetime.strptime(fim_aula.split(',')[0].strip(), '%Y-%m-%d')
                        
                        # Início das aulas deve ser >= fim das inscrições
                        if inicio_aula_dt < fim_insc:
                            fim_insc_formatado = fim_insc.strftime('%d/%m/%Y')
                            self.errors.append(f"Início das aulas da unidade {i} deve ser posterior ou igual ao fim das inscrições ({fim_insc_formatado})")
                        
                        # Fim das aulas deve ser >= fim das inscrições
                        if fim_aula_dt < fim_insc:
                            fim_insc_formatado = fim_insc.strftime('%d/%m/%Y')
                            self.errors.append(f"Fim das aulas da unidade {i} deve ser posterior ou igual ao fim das inscrições ({fim_insc_formatado})")
                            
                    except (ValueError, IndexError):
                        self.errors.append(f"Formato de data inválido para unidade {i}")
                        
        except ValueError:
            self.errors.append("Formato de data de inscrições inválido")
    
    def _validate_external_partner(self, form_data: Dict):
        """Valida dados do parceiro externo"""
        if form_data.get('parceiro_externo') == 'sim':
            partner_name = form_data.get('parceiro_nome', '').strip()
            if not partner_name:
                self.errors.append("Nome do parceiro é obrigatório quando há parceiro externo")
            elif len(partner_name) > Config.MAX_PARTNER_NAME_LENGTH:
                self.errors.append(f"Nome do parceiro deve ter no máximo {Config.MAX_PARTNER_NAME_LENGTH} caracteres")
    
    def _extract_units_data(self, form_data: Dict) -> List[Dict]:
        """Extrai dados das unidades do formulário (apenas unidades presenciais)"""
        unidades = []
        
        # Extrair dados de arrays
        enderecos = form_data.getlist('endereco_unidade[]') if hasattr(form_data, 'getlist') else form_data.get('endereco_unidade[]', [])
        bairros = form_data.getlist('bairro_unidade[]') if hasattr(form_data, 'getlist') else form_data.get('bairro_unidade[]', [])
        vagas = form_data.getlist('vagas_unidade[]') if hasattr(form_data, 'getlist') else form_data.get('vagas_unidade[]', [])
        dias = form_data.getlist('dias_aula[]') if hasattr(form_data, 'getlist') else form_data.get('dias_aula[]', [])
        
        # Determinar número de unidades presenciais
        # Usar apenas os campos que realmente pertencem às unidades presenciais
        max_units = max(len(enderecos), len(bairros), len(vagas)) if (enderecos or bairros or vagas) else 0
        
        # Filtrar apenas unidades que têm dados válidos (não vazios)
        for i in range(max_units):
            endereco = enderecos[i] if i < len(enderecos) else ''
            bairro = bairros[i] if i < len(bairros) else ''
            vaga = vagas[i] if i < len(vagas) else ''
            
            # Só incluir se pelo menos um campo principal não estiver vazio
            if endereco.strip() or bairro.strip() or vaga.strip():
                unidade = {
                    'endereco_unidade': endereco,
                    'bairro_unidade': bairro,
                    'vagas_unidade': vaga,
                    'dias_aula': dias[i] if i < len(dias) else ''
                }
                unidades.append(unidade)
        return unidades
    
    def validate_file_upload(self, file, allowed_extensions: set = None) -> Tuple[bool, str]:
        """
        Valida upload de arquivo
        
        Args:
            file: Arquivo enviado
            allowed_extensions: Extensões permitidas
            
        Returns:
            Tuple[bool, str]: (é_válido, mensagem_erro)
        """
        if allowed_extensions is None:
            allowed_extensions = Config.ALLOWED_EXTENSIONS
        
        if not file or not file.filename:
            return False, "Nenhum arquivo foi enviado"
        
        if not self._allowed_file(file.filename, allowed_extensions):
            return False, f"Tipo de arquivo não permitido. Extensões aceitas: {', '.join(allowed_extensions)}"
        
        # Verificar tamanho do arquivo (se disponível)
        if hasattr(file, 'content_length') and file.content_length > Config.MAX_FILE_SIZE:
            return False, f"Arquivo muito grande. Tamanho máximo: {Config.MAX_FILE_SIZE // (1024*1024)}MB"
        
        return True, ""
    
    def _allowed_file(self, filename: str, allowed_extensions: set) -> bool:
        """Verifica se a extensão do arquivo é permitida"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
