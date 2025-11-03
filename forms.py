# forms.py
"""
Formulários WTF com proteção CSRF para o WebCiclo.
Implementa validação de formulários e proteção contra ataques CSRF.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, SelectField, IntegerField, 
    DateField, TimeField, BooleanField, PasswordField,
    FieldList, FormField, HiddenField
)
from wtforms.validators import (
    DataRequired, Length, Optional, NumberRange, 
    Email, URL, ValidationError
)
from config import Config

class LoginForm(FlaskForm):
    """Formulário de login com proteção CSRF"""
    username = StringField(
        'Usuário',
        validators=[
            DataRequired(message='Usuário é obrigatório'),
            Length(min=3, max=50, message='Usuário deve ter entre 3 e 50 caracteres')
        ],
        render_kw={'placeholder': 'Digite seu usuário'}
    )
    
    password = PasswordField(
        'Senha',
        validators=[
            DataRequired(message='Senha é obrigatória'),
            Length(min=6, message='Senha deve ter pelo menos 6 caracteres')
        ],
        render_kw={'placeholder': '********'}
    )

class UnidadeForm(FlaskForm):
    """Subformulário para dados de uma unidade presencial"""
    endereco = StringField(
        'Endereço',
        validators=[Optional(), Length(max=200)],
        render_kw={'placeholder': 'Rua, número, complemento'}
    )
    
    bairro = StringField(
        'Bairro',
        validators=[Optional(), Length(max=100)],
        render_kw={'placeholder': 'Nome do bairro'}
    )
    
    vagas = IntegerField(
        'Vagas',
        validators=[Optional(), NumberRange(min=1, max=1000)],
        render_kw={'placeholder': '30'}
    )
    
    inicio_aulas = DateField(
        'Início das Aulas',
        validators=[Optional()]
    )
    
    fim_aulas = DateField(
        'Fim das Aulas',
        validators=[Optional()]
    )
    
    horario_inicio = TimeField(
        'Horário de Início',
        validators=[Optional()]
    )
    
    horario_fim = TimeField(
        'Horário de Fim',
        validators=[Optional()]
    )
    
    dias_aula = StringField(
        'Dias da Semana',
        validators=[Optional(), Length(max=100)],
        render_kw={'placeholder': 'Segunda a Sexta'}
    )

class CourseForm(FlaskForm):
    """Formulário principal de criação/edição de curso com proteção CSRF"""
    
    # Informações básicas
    titulo = StringField(
        'Título do Curso',
        validators=[
            DataRequired(message='Título é obrigatório'),
            Length(max=Config.MAX_TITLE_LENGTH, message=f'Título deve ter no máximo {Config.MAX_TITLE_LENGTH} caracteres')
        ],
        render_kw={'placeholder': 'Digite o título do curso'}
    )
    
    descricao = TextAreaField(
        'Descrição',
        validators=[
            DataRequired(message='Descrição é obrigatória'),
            Length(max=Config.MAX_DESCRIPTION_LENGTH, message=f'Descrição deve ter no máximo {Config.MAX_DESCRIPTION_LENGTH} caracteres')
        ],
        render_kw={'placeholder': 'Descreva o curso, objetivos e conteúdo', 'rows': 5}
    )
    
    orgao_responsavel = SelectField(
        'Órgão Responsável',
        validators=[DataRequired(message='Órgão responsável é obrigatório')],
        choices=[]  # Será preenchido dinamicamente
    )
    
    modalidade = SelectField(
        'Modalidade',
        validators=[DataRequired(message='Modalidade é obrigatória')],
        choices=[
            ('', 'Selecione a modalidade'),
            ('Presencial', 'Presencial'),
            ('Online', 'Online'),
            ('Híbrido', 'Híbrido')
        ]
    )
    
    # Datas de inscrição
    inicio_inscricoes = DateField(
        'Início das Inscrições',
        validators=[DataRequired(message='Data de início das inscrições é obrigatória')]
    )
    
    fim_inscricoes = DateField(
        'Fim das Inscrições',
        validators=[DataRequired(message='Data de fim das inscrições é obrigatória')]
    )
    
    # Campos condicionais para modalidade online
    plataforma_digital = StringField(
        'Plataforma Digital',
        validators=[Optional(), Length(max=100)],
        render_kw={'placeholder': 'Ex: Zoom, Teams, Google Meet'}
    )
    
    aulas_assincronas = SelectField(
        'Aulas Assíncronas',
        choices=[
            ('sim', 'Sim'),
            ('nao', 'Não')
        ],
        default='sim'
    )
    
    # Campos de valores
    curso_gratuito = SelectField(
        'Curso Gratuito',
        choices=[
            ('sim', 'Sim'),
            ('nao', 'Não')
        ],
        default='sim'
    )
    
    valor_curso_inteira = StringField(
        'Valor Inteira',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': 'R$ 0,00'}
    )
    
    valor_curso_meia = StringField(
        'Valor Meia Entrada',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': 'R$ 0,00'}
    )
    
    requisitos_meia = TextAreaField(
        'Requisitos Meia Entrada',
        validators=[Optional(), Length(max=500)],
        render_kw={'placeholder': 'Descreva os requisitos para meia entrada', 'rows': 3}
    )
    
    # Certificado
    oferece_certificado = SelectField(
        'Oferece Certificado',
        choices=[
            ('nao', 'Não'),
            ('sim', 'Sim')
        ],
        default='nao'
    )
    
    pre_requisitos = TextAreaField(
        'Pré-requisitos',
        validators=[Optional(), Length(max=500)],
        render_kw={'placeholder': 'Descreva os pré-requisitos do curso', 'rows': 3}
    )
    
    # Bolsa
    oferece_bolsa = SelectField(
        'Oferece Bolsa',
        choices=[
            ('nao', 'Não'),
            ('sim', 'Sim')
        ],
        default='nao'
    )
    
    valor_bolsa = StringField(
        'Valor da Bolsa',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': 'R$ 0,00'}
    )
    
    requisitos_bolsa = TextAreaField(
        'Requisitos da Bolsa',
        validators=[Optional(), Length(max=500)],
        render_kw={'placeholder': 'Descreva os requisitos para a bolsa', 'rows': 3}
    )
    
    # Acessibilidade
    acessibilidade = SelectField(
        'Acessibilidade',
        choices=[
            ('nao_acessivel', 'Não Acessível'),
            ('parcialmente_acessivel', 'Parcialmente Acessível'),
            ('totalmente_acessivel', 'Totalmente Acessível')
        ],
        default='nao_acessivel'
    )
    
    recursos_acessibilidade = TextAreaField(
        'Recursos de Acessibilidade',
        validators=[Optional(), Length(max=500)],
        render_kw={'placeholder': 'Descreva os recursos de acessibilidade disponíveis', 'rows': 3}
    )
    
    # Parceiro externo
    parceiro_externo = SelectField(
        'Parceiro Externo',
        choices=[
            ('nao', 'Não'),
            ('sim', 'Sim')
        ],
        default='nao'
    )
    
    parceiro_nome = StringField(
        'Nome do Parceiro',
        validators=[Optional(), Length(max=Config.MAX_PARTNER_NAME_LENGTH)],
        render_kw={'placeholder': 'Nome da instituição parceira'}
    )
    
    parceiro_link = StringField(
        'Link do Parceiro',
        validators=[Optional(), URL(message='URL inválida'), Length(max=200)],
        render_kw={'placeholder': 'https://www.parceiro.com.br'}
    )
    
    # Arquivos
    capa_curso = FileField(
        'Capa do Curso',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'bmp'], 'Apenas imagens são permitidas')
        ]
    )
    
    parceiro_logo = FileField(
        'Logo do Parceiro',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'bmp'], 'Apenas imagens são permitidas')
        ]
    )
    
    # Informações complementares
    info_complementares = TextAreaField(
        'Informações Complementares',
        validators=[Optional(), Length(max=1000)],
        render_kw={'placeholder': 'Informações adicionais sobre o curso', 'rows': 4}
    )
    
    def validate_fim_inscricoes(self, field):
        """Valida se a data de fim é posterior ao início"""
        if self.inicio_inscricoes.data and field.data:
            if field.data <= self.inicio_inscricoes.data:
                raise ValidationError('Data de fim deve ser posterior à data de início')
    
    def validate_modalidade_fields(self):
        """Valida campos específicos baseados na modalidade"""
        errors = []
        
        if self.modalidade.data == 'Online':
            if not self.plataforma_digital.data:
                errors.append('Plataforma digital é obrigatória para cursos online')
        
        return errors

class CourseStatusForm(FlaskForm):
    """Formulário para marcar status de curso como inserido"""
    course_id = HiddenField('Course ID', validators=[DataRequired()])
    action = HiddenField('Action', validators=[DataRequired()])

class DeleteCourseForm(FlaskForm):
    """Formulário para exclusão de curso com proteção CSRF"""
    course_id = HiddenField('Course ID', validators=[DataRequired()])
    confirm_delete = HiddenField('Confirm Delete', default='true')