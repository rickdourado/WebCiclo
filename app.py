from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from datetime import datetime
import os
import functools
import logging

# Importar configurações e serviços
from config import Config, config
from services.course_service import CourseService
from services.validation_service import ValidationError
from services.course_status_service import CourseStatusService

# Configurar aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Validar configurações obrigatórias
try:
    Config.validate_required_config()
except ValueError as e:
    print(f"ERRO DE CONFIGURAÇÃO: {e}")
    exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar serviços
course_service = CourseService()
course_status_service = CourseStatusService()

# Configuração do template folder
app.template_folder = 'templates'
app.static_folder = 'static'



# Simulação de banco de dados para cursos
COURSES_DB = []

# Lista de órgãos carregada do arquivo Listadecursos.txt
ORGAOS = [
    'Secretaria Municipal da Casa Civil - CVL',
    'Secretaria Municipal de Coordenação Governamental - SMCG',
    'Secretaria Municipal de Fazenda - SMF',
    'Secretaria Municipal de Integridade, Transparência e Proteção de Dados - SMIT',
    'Secretaria Municipal de Desenvolvimento Urbano e Licenciamento - SMDU',
    'Secretaria Municipal de Desenvolvimento Econômico – SMDE',
    'Secretaria Municipal de Infraestrutura - SMI',
    'Secretaria Municipal de Transportes - SMTR',
    'Secretaria Municipal de Conservação - SECONSERVA',
    'Secretaria Municipal de Educação - SME',
    'Secretaria Municipal de Assistência Social - SMAS',
    'Secretaria Municipal de Saúde - SMS',
    'Secretaria Municipalk de Administração - SMA',
    'Secretaria Municipal de Trabalho e Renda - SMTE',
    'Secretaria Municipal de Cultura - SMC',
    'Secretaria Municipal da Pessoa com Deficiência - SMPD',
    'Secretaria Municipal do Ambiente e Clima - SMAC',
    'Secretaria de Esportes - SMEL',
    'Secretaria Municipal de Habitação - SMH',
    'Secretaria Municipal de Ciência, Tecnologia e Inovação - SMCT',
    'Secretaria Mun. do Envelhecimento Saudável e Qualidade de Vida - SEMESQV',
    'Secretaria Municipal de Ordem Pública - SEOP',
    'Secretaria Municipal de Proteção e Defesa dos Animais - SMPDA',
    'Secretaria Municipal de Turismo - SMTUR-RIO',
    'Secretaria Especial de Proteção e Defesa do Consumidor - SEDECON',
    'Secretaria Especial de Políticas para Mulheres e  Cuidados - SPM-RIO',
    'Secretaria Especial da Juventude Carioca - JUV-RIO',
    'Secretaria Especial de Ação Comunitária - SEAC-RIO',
    'Secretaria Especial de Cidadania e Família - SECID',
    'Secretaria Especial de Integração Metropolitana - SEIM',
    'Secretaria Especial de Economia Solidária - SES-RIO',
    'Secretaria Especial de Direitos HUmanos e Igualdade Racial - SEDHIR',
    'Secretaria Especial de Inclusão - SINC-RIO',
    'Arquivo Geral da Cidade do Rio de Janeiro - C/ARQ',
    'Controladoria Geral do Município - CGM-RIO',
    'Procuradoria Geral do Município - PGM',
    'Instituto de Previdência e Assistência - PREVI-RIO',
    'Instituto Fundação João Goulart - CVL/FJG',
    'Instituto Municipal de Urbanismo Pereira Passos - IPP',
    'Instituto Municipal de Vigilância Sanitária, Vigilância de Zoonoses e de Inspeção Agropecuária - S/IVISA-RIO',
    'Guarda Municipal do Rio de Janeiro - GM-RIO',
    'Fundação Instituto de Geotécnica do Município do Rio de Janeiro – GEO-RIO',
    'Fundação Instituto das Águas do Município do Rio de Janeiro - RIO-ÁGUAS',
    'Fundação Parques e Jardins - FPJ',
    'Fundação Planetário da Cidade do Rio de Janeiro - PLANETÁRIO',
    'Fundação Jardim Zoológico da Cidade do Rio de Janeiro - RIO-ZOO',
    'Fundação Cidade das Artes - CIDADE DAS ARTES',
    'Empresa Municipal de Multimeios S.A. - MULTIRIO',
    'Distribuidora de Filmes S.A. - RIOFILME',
    'Empresa Municipal de Informática - IPLANRIO',
    'Empresa Municipal de Artes Gráficas - IMPRENSA DA CIDADE',
    'Companhia Carioca de Parcerias e Investimentos - CCPAR',
    'Empresa Municipal de Urbanização - RIO-URBE',
    'Empresa de Turismo do Município do Rio de Janeiro - RIOTUR',
    'Empresa Pública de Saúde do Rio de Janeiro – RIOSAÚDE',
    'Companhia Municipal de Energia e Iluminação - RIOLUZ',
    'Companhia Municipal de Limpeza Urbana – COMLURB',
    'Companhia de Engenharia de Tráfego do RJ - CET-RIO',
    'Companhia Municipal de Transportes Coletivos - CMTC-RIO',
    'Riocentro S.A. - Centro de Feiras, Exposições e Congressos do Rio de Janeiro - RIOCENTRO',
    'Agência de Fomento do Município do Rio de Janeiro S.A. - INVEST.RIO',
    'Empresa de Eventos do Município do Rio de Janeiro - RIOEVENTOS',
    'Instituto Rio Patrimônio da Humanidade - IRPH'
]

@app.route('/')
def index():
    """Página inicial com formulário de criação de curso"""
    # Limpar apenas mensagens de sucesso ao acessar a página inicial
    # Isso evita que mensagens de sucesso apareçam quando o usuário volta da página de sucesso
    # Mas mantém mensagens de erro de validação para serem exibidas
    if '_flashes' in session:
        flashes = session['_flashes']
        # Manter apenas mensagens de erro e warning, remover sucesso
        session['_flashes'] = [flash for flash in flashes if flash[0] in ['error', 'warning']]
    
    # Data atual para preenchimento automático dos campos de data
    from datetime import datetime
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('index.html', 
                         orgaos=ORGAOS,
                         today_date=today_date)

@app.route('/create_course', methods=['POST'])
def create_course():
    """Cria um novo curso usando o serviço de cursos"""
    try:
        logger.info("Iniciando criação de curso")
        logger.info(f"Dados recebidos: {dict(request.form)}")
        
        # Log específico para campos de horário
        logger.info("=== DEBUG CAMPOS DE HORÁRIO ===")
        logger.info(f"horario_inicio[]: {request.form.getlist('horario_inicio[]')}")
        logger.info(f"horario_fim[]: {request.form.getlist('horario_fim[]')}")
        logger.info(f"aulas_assincronas: {request.form.get('aulas_assincronas')}")
        logger.info(f"modalidade: {request.form.get('modalidade')}")
        logger.info("===============================")
        
        # Usar o serviço de cursos para criar o curso
        success, course_data, messages = course_service.create_course(request.form, request.files)
        
        if success:
            logger.info(f"Curso criado com sucesso: ID {course_data['id']}")
            
            # Exibir avisos se houver
            for warning in messages:
                flash(warning, 'warning')
            
            flash('Curso criado com sucesso!', 'success')
            return redirect(url_for('course_success', course_id=course_data['id']))
        else:
            # Exibir erros de validação
            logger.warning(f"Falha na criação do curso: {messages}")
            for error in messages:
                flash(error, 'error')
                logger.warning(f"Erro de validação: {error}")
            
            # Log detalhado para debug
            logger.info("Dados do formulário que falharam na validação:")
            for key, value in request.form.items():
                logger.info(f"  {key}: {value}")
            
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"Erro interno ao criar curso: {str(e)}")
        logger.error(f"Tipo do erro: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        flash(f'Erro interno ao criar curso: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/course/<int:course_id>')
def course_success(course_id):
    """Página de sucesso após criação do curso"""
    try:
        logger.info(f"🎉 Acessando página de sucesso para curso ID: {course_id}")
        course = course_service.get_course(course_id)
        if not course:
            logger.warning(f"❌ Curso {course_id} não encontrado na página de sucesso")
            flash('Curso não encontrado', 'error')
            return redirect(url_for('index'))
        
        # Obter arquivos gerados
        csv_file = course.get('csv_file')
        pdf_file = course.get('pdf_file')
        
        logger.info(f"✅ Renderizando página de sucesso para: {course.get('titulo', 'Curso sem título')}")
        logger.info(f"📄 Arquivos: CSV={csv_file}, PDF={pdf_file}")
        
        return render_template('course_success.html', 
                               course=course, 
                               csv_file=csv_file, 
                               pdf_file=pdf_file)
    except Exception as e:
        logger.error(f"Erro ao buscar curso {course_id}: {str(e)}")
        flash('Erro ao carregar curso', 'error')
        return redirect(url_for('index'))

@app.route('/courses/public')
def public_courses():
    """Lista pública de cursos - apenas visualização e duplicação"""
    try:
        # Log para debug no PythonAnywhere
        if 'pythonanywhere' in request.host:
            logger.info("Acessando lista pública de cursos via PythonAnywhere")
        
        # Usar o serviço para listar cursos
        courses = course_service.list_courses()
        
        return render_template('course_list_public.html', courses=courses)
    except Exception as e:
        logger.error(f"Erro ao listar cursos públicos: {str(e)}")
        flash('Erro ao carregar lista de cursos', 'error')
        return redirect(url_for('index'))

# -----------------------------
# Decorator de autenticação
# -----------------------------

def login_required(view_func):
    """Decorator para proteger rotas que exigem login de admin"""
    @functools.wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('admin_login'))
        return view_func(*args, **kwargs)
    return wrapped_view

@app.route('/courses')
@login_required
def list_courses():
    """Listar todos os cursos criados - área administrativa"""
    try:
        # Log para debug no PythonAnywhere
        if 'pythonanywhere' in request.host:
            logger.info("Acessando lista de cursos via PythonAnywhere")
        
        # Usar o serviço para listar cursos
        courses = course_service.list_courses()
        
        # Obter status dos cursos inseridos
        inserted_courses = course_status_service.get_inserted_courses()
        logger.info(f"📊 Cursos inseridos carregados: {inserted_courses}")
        
        # Adicionar status aos cursos
        for course in courses:
            # Converter ID do curso para int para comparação correta
            course_id = course.get('id')
            if isinstance(course_id, str) and course_id.isdigit():
                course_id = int(course_id)
            course['is_inserted'] = course_id in inserted_courses
            if course.get('is_inserted'):
                logger.info(f"✅ Curso {course.get('id')} marcado como inserido na interface")
        
        return render_template('course_list.html', courses=courses, inserted_courses=inserted_courses)
    except Exception as e:
        logger.error(f"Erro ao listar cursos: {str(e)}")
        flash('Erro ao carregar lista de cursos', 'error')
        return redirect(url_for('index'))

@app.route('/duplicate/<int:course_id>', methods=['GET', 'POST'])
def duplicate_course(course_id):
    """Carrega formulário de duplicação ou processa a criação do curso duplicado"""
    try:
        if request.method == 'POST':
            # Processar criação do curso duplicado
            logger.info(f"Processando duplicação do curso {course_id}")
            logger.info(f"Dados recebidos: {dict(request.form)}")
            
            # Usar o serviço de cursos para criar o curso duplicado
            success, course_data, messages = course_service.create_course(request.form, request.files)
            
            if success:
                logger.info(f"Curso duplicado com sucesso: ID {course_data['id']}")
                
                # Exibir avisos se houver
                for warning in messages:
                    flash(warning, 'warning')
                
                flash('Curso duplicado com sucesso!', 'success')
                return redirect(url_for('course_success', course_id=course_data['id']))
            else:
                # Exibir erros de validação e manter na página de duplicação
                logger.warning(f"Falha na duplicação do curso: {messages}")
                for error in messages:
                    flash(error, 'error')
                    logger.warning(f"Erro de validação: {error}")
                
                # Buscar dados originais do curso para duplicação
                original_course_data = course_service.get_course(course_id)
                if original_course_data:
                    # Preparar dados para duplicação
                    original_course_data = _prepare_course_for_edit_form(original_course_data)
                    duplicate_data = original_course_data.copy()
                    
                    # Limpar campos que não devem ser copiados
                    fields_to_clear = ['id', 'created_at', 'csv_file', 'pdf_file', 'capa_curso']
                    for field in fields_to_clear:
                        duplicate_data[field] = ''
                    
                    # Sobrescrever com dados do formulário para preservar o que o usuário digitou
                    for key, value in request.form.items():
                        if key.endswith('[]'):
                            duplicate_data[key.replace('[]', '')] = request.form.getlist(key)
                        else:
                            duplicate_data[key] = value
                    
                    # Preparar título para duplicação se não foi alterado pelo usuário
                    if not duplicate_data.get('titulo') or duplicate_data.get('titulo') == f"Cópia de {original_course_data.get('titulo', '')}":
                        original_title = original_course_data.get('titulo', '')
                        if original_title:
                            duplicate_data['titulo_original'] = f"Cópia de {original_title}"
                            duplicate_data['titulo'] = f"Cópia de {original_title}"
                            duplicate_data['descricao_original'] = original_course_data.get('descricao', '')
                    
                    # Renderizar formulário com dados preservados e mensagens de erro
                    today_date = datetime.now().strftime('%Y-%m-%d')
                    return render_template('course_duplicate.html', 
                                         orgaos=ORGAOS,
                                         duplicate_data=duplicate_data,
                                         original_course_id=course_id,
                                         today_date=today_date)
                
                # Se não conseguir buscar dados originais, redirecionar
                return redirect(url_for('duplicate_course', course_id=course_id))
        
        # GET - Carregar formulário de duplicação
        # Buscar o curso a ser duplicado
        course_data = course_service.get_course(course_id)
        if not course_data:
            flash('Curso não encontrado para duplicação', 'error')
            return redirect(url_for('public_courses'))
        
        # Preparar dados igual ao formulário de edição
        course_data = _prepare_course_for_edit_form(course_data)
        
        # Preparar dados para duplicação
        duplicate_data = course_data.copy()
        
        # Limpar campos que não devem ser copiados na duplicação
        fields_to_clear = [
            'id', 'created_at', 'csv_file', 'pdf_file', 'capa_curso'
        ]
        
        for field in fields_to_clear:
            duplicate_data[field] = ''
        
        # Preparar título para duplicação
        original_title = course_data.get('titulo', '')
        if original_title:
            duplicate_data['titulo_original'] = f"Cópia de {original_title}"
            duplicate_data['titulo'] = f"Cópia de {original_title}"  # Para preencher o campo
            duplicate_data['descricao_original'] = course_data.get('descricao', '')  # Para exibir na interface
        
        # Renderizar formulário com dados pré-preenchidos
        today_date = datetime.now().strftime('%Y-%m-%d')
        return render_template('course_duplicate.html', 
                             orgaos=ORGAOS,
                             duplicate_data=duplicate_data,
                             original_course_id=course_id,
                             today_date=today_date)
    except Exception as e:
        logger.error(f"Erro ao duplicar curso {course_id}: {str(e)}")
        flash('Erro ao carregar dados para duplicação', 'error')
        return redirect(url_for('public_courses'))

# -----------------------------
# Rotas de autenticação admin
# -----------------------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Credenciais inválidas.', 'error')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    """Dashboard administrativo"""
    try:
        courses = course_service.list_courses()
        return render_template('course_list.html', courses=courses)
    except Exception as e:
        logger.error(f"Erro no dashboard admin: {str(e)}")
        flash('Erro ao carregar dashboard', 'error')
        return redirect(url_for('index'))

# -----------------------------
# Fim da seção de autenticação admin
# -----------------------------

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    """Editar um curso existente"""
    try:
        course = course_service.get_course(course_id)
        if not course:
            flash('Curso não encontrado', 'error')
            return redirect(url_for('list_courses'))
        
        if request.method == 'POST':
            # Usar o serviço para atualizar o curso
            success, updated_course, messages = course_service.update_course(course_id, request.form, request.files)
            
            if success:
                # Exibir avisos se houver
                for warning in messages:
                    flash(warning, 'warning')
                
                flash('Curso atualizado com sucesso!', 'success')
                return redirect(url_for('course_edit_success', course_id=course_id))
            else:
                # Exibir erros de validação e manter na página de edição
                for error in messages:
                    flash(error, 'error')
                
                # Preparar dados do curso com os dados do formulário para preservar as alterações
                course = _prepare_course_for_edit_form(course)
                
                # Sobrescrever com dados do formulário para preservar o que o usuário digitou
                for key, value in request.form.items():
                    if key.endswith('[]'):
                        # Para campos de array, usar getlist
                        course[key.replace('[]', '')] = request.form.getlist(key)
                    else:
                        course[key] = value
                
                # Renderizar o formulário novamente com os dados preservados e mensagens de erro
                return render_template('course_edit.html', course=course, orgaos=ORGAOS)
        
        # Preparar dados para o formulário de edição
        course = _prepare_course_for_edit_form(course)
        return render_template('course_edit.html', course=course, orgaos=ORGAOS)
        
    except Exception as e:
        logger.error(f"Erro ao editar curso {course_id}: {str(e)}")
        flash(f'Erro ao editar curso: {str(e)}', 'error')
        return redirect(url_for('list_courses'))

def _prepare_course_for_edit_form(course):
    """Prepara dados do curso para o formulário de edição"""
    # Garantir que temos a descrição original para edição
    if not course.get('descricao_original') and course.get('descricao'):
        # Se não temos descricao_original, usar a descricao atual como original
        course['descricao_original'] = course['descricao']
    
    # Converter datas para o formato HTML (YYYY-MM-DD)
    if 'inicio_inscricoes' in course and course['inicio_inscricoes']:
        try:
            # Tentar primeiro com separador '-'
            if '-' in course['inicio_inscricoes']:
                parts = course['inicio_inscricoes'].split('-')
            # Tentar com separador '/' se não encontrar '-'
            else:
                parts = course['inicio_inscricoes'].split('/')
                
            if len(parts) == 3:
                # Se estiver no formato DD-MM-AAAA ou DD/MM/AAAA
                if len(parts[2]) == 4:  # Ano tem 4 dígitos
                    course['inicio_inscricoes_data'] = f'{parts[2]}-{parts[1]}-{parts[0]}'
                # Se estiver no formato AAAA-MM-DD ou AAAA/MM/DD
                elif len(parts[0]) == 4:  # Ano tem 4 dígitos
                    course['inicio_inscricoes_data'] = f'{parts[0]}-{parts[1]}-{parts[2]}'
        except Exception as e:
            logger.warning(f"Erro ao converter data de início: {e}")
            course['inicio_inscricoes_data'] = ''
    else:
        course['inicio_inscricoes_data'] = ''
    
    if 'fim_inscricoes' in course and course['fim_inscricoes']:
        try:
            # Tentar primeiro com separador '-'
            if '-' in course['fim_inscricoes']:
                parts = course['fim_inscricoes'].split('-')
            # Tentar com separador '/' se não encontrar '-'
            else:
                parts = course['fim_inscricoes'].split('/')
                
            if len(parts) == 3:
                # Se estiver no formato DD-MM-AAAA ou DD/MM/AAAA
                if len(parts[2]) == 4:  # Ano tem 4 dígitos
                    course['fim_inscricoes_data'] = f'{parts[2]}-{parts[1]}-{parts[0]}'
                # Se estiver no formato AAAA-MM-DD ou AAAA/MM/DD
                elif len(parts[0]) == 4:  # Ano tem 4 dígitos
                    course['fim_inscricoes_data'] = f'{parts[0]}-{parts[1]}-{parts[2]}'
        except Exception as e:
            logger.warning(f"Erro ao converter data de fim: {e}")
            course['fim_inscricoes_data'] = ''
    else:
        course['fim_inscricoes_data'] = ''
    
    # Mapear campos de modalidade e unidades
    if course.get('modalidade') == 'Presencial' or course.get('modalidade') == 'Híbrido':
        # Processar dados de múltiplas unidades separados por |
        enderecos = course.get('endereco_unidade', '').split('|') if course.get('endereco_unidade') else ['']
        bairros = course.get('bairro_unidade', '').split('|') if course.get('bairro_unidade') else ['']
        vagas = course.get('vagas_unidade', '').split('|') if course.get('vagas_unidade') else ['']
        inicio_aulas = course.get('inicio_aulas_data', '').split('|') if course.get('inicio_aulas_data') else ['']
        fim_aulas = course.get('fim_aulas_data', '').split('|') if course.get('fim_aulas_data') else ['']
        horario_inicio = course.get('horario_inicio', '').split('|') if course.get('horario_inicio') else ['']
        horario_fim = course.get('horario_fim', '').split('|') if course.get('horario_fim') else ['']
        dias_aula = course.get('dias_aula', '').split('|') if course.get('dias_aula') else ['']
        
        # Campos de unidade presencial (primeira unidade para compatibilidade)
        course['endereco_unidade'] = enderecos[0] if enderecos else ''
        course['bairro_unidade'] = bairros[0] if bairros else ''
        course['vagas_unidade'] = vagas[0] if vagas else ''
        course['inicio_aulas_data'] = inicio_aulas[0] if inicio_aulas else ''
        course['fim_aulas_data'] = fim_aulas[0] if fim_aulas else ''
        course['horario_inicio'] = horario_inicio[0] if horario_inicio else ''
        course['horario_fim'] = horario_fim[0] if horario_fim else ''
        course['dias_aula'] = dias_aula[0] if dias_aula else ''
        
        # Arrays para múltiplas unidades
        course['enderecos_unidades'] = enderecos
        course['bairros_unidades'] = bairros
        course['vagas_unidades'] = vagas
        course['inicio_aulas_unidades'] = inicio_aulas
        course['fim_aulas_unidades'] = fim_aulas
        course['horario_inicio_unidades'] = horario_inicio
        course['horario_fim_unidades'] = horario_fim
        course['dias_aula_unidades'] = dias_aula
    elif course.get('modalidade') == 'Online':
        # Campos de plataforma online
        course['plataforma_digital'] = course.get('plataforma_digital', '')
        course['aulas_assincronas'] = course.get('aulas_assincronas', 'sim')
        course['vagas_online'] = course.get('vagas_unidade', '')
        course['inicio_aulas_online'] = course.get('inicio_aulas_data', '')
        course['fim_aulas_online'] = course.get('fim_aulas_data', '')
        course['horario_inicio_online'] = course.get('horario_inicio', '')
        course['horario_fim_online'] = course.get('horario_fim', '')
    
    # Mapear campos de valores e certificado
    course['curso_gratuito'] = course.get('curso_gratuito', 'sim')
    course['valor_curso_inteira'] = course.get('valor_curso_inteira', '')
    course['valor_curso_meia'] = course.get('valor_curso_meia', '')
    course['requisitos_meia'] = course.get('requisitos_meia', '')
    course['oferece_certificado'] = course.get('oferece_certificado', 'nao')
    course['pre_requisitos'] = course.get('pre_requisitos', '')
    
    # Mapear campos de bolsa
    course['oferece_bolsa'] = course.get('oferece_bolsa', 'nao')
    course['valor_bolsa'] = course.get('valor_bolsa', '')
    course['requisitos_bolsa'] = course.get('requisitos_bolsa', '')
    
    # Mapear campos de acessibilidade
    course['acessibilidade'] = course.get('acessibilidade', 'nao_acessivel')
    course['recursos_acessibilidade'] = course.get('recursos_acessibilidade', '')
    
    # Mapear campos de parceiro externo
    course['parceiro_externo'] = course.get('parceiro_externo', 'nao')
    course['parceiro_nome'] = course.get('parceiro_nome', '')
    course['parceiro_link'] = course.get('parceiro_link', '')
    course['parceiro_logo'] = course.get('parceiro_logo', '')
    
    # Mapear informações adicionais
    course['info_adicionais_opcao'] = 'nao'  # Padrão para não mostrar campo adicional
    if course.get('info_complementares') and course.get('info_complementares').strip():
        course['info_adicionais_opcao'] = 'sim'
    
    return course

@app.route('/course_edit_success/<int:course_id>')
@login_required
def course_edit_success(course_id):
    """Exibir página de sucesso após edição do curso"""
    try:
        course = course_service.get_course(course_id)
        if not course:
            flash('Curso não encontrado', 'error')
            return redirect(url_for('list_courses'))
        return render_template('course_edit_success.html', course=course)
    except Exception as e:
        logger.error(f"Erro ao carregar curso editado {course_id}: {str(e)}")
        flash('Erro ao carregar curso', 'error')
        return redirect(url_for('list_courses'))

@app.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    """Excluir um curso existente e seus arquivos"""
    try:
        success, message = course_service.delete_course(course_id)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        return redirect(url_for('list_courses'))
        
    except Exception as e:
        logger.error(f"Erro ao excluir curso {course_id}: {str(e)}")
        flash(f'Erro ao excluir curso: {str(e)}', 'error')
        return redirect(url_for('list_courses'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """Rota para download de arquivos CSV e PDF"""
    try:
        if filename.endswith('.csv'):
            directory = Config.CSV_DIR
        elif filename.endswith('.pdf'):
            directory = Config.PDF_DIR
        else:
            flash('Tipo de arquivo não suportado', 'error')
            return redirect(url_for('index'))
        
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Erro ao baixar arquivo {filename}: {str(e)}")
        flash(f'Erro ao baixar arquivo: {str(e)}', 'error')
        return redirect(url_for('index'))

# -----------------------------
# Rotas para gerenciar status dos cursos
# -----------------------------

@app.route('/api/course/<int:course_id>/toggle-status', methods=['POST'])
@login_required
def toggle_course_status(course_id):
    """Alterna o status de inserção de um curso"""
    try:
        logger.info(f"🔄 API: Alternando status do curso {course_id}")
        new_status = course_status_service.toggle_course_status(course_id)
        logger.info(f"✅ API: Novo status do curso {course_id}: {new_status}")
        return {
            'success': True,
            'course_id': course_id,
            'inserted': new_status,
            'message': 'Curso marcado como inserido' if new_status else 'Curso desmarcado'
        }
    except Exception as e:
        logger.error(f"❌ API: Erro ao alterar status do curso {course_id}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }, 500

@app.route('/api/courses/status')
@login_required
def get_courses_status():
    """Retorna o status de todos os cursos"""
    try:
        inserted_courses = course_status_service.get_inserted_courses()
        return {
            'success': True,
            'inserted_courses': list(inserted_courses)
        }
    except Exception as e:
        logger.error(f"Erro ao buscar status dos cursos: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }, 500



if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎓 WebApp v4 - Ciclo Carioca (CicloCarioca.pythonanywhere.com)")
    print("📋 Formulário de Criação de Cursos")
    print("🌐 Rodando em modo de produção")
    print("="*50 + "\n")
    
    # Configuração para desenvolvimento local
    app.run(debug=False, host='0.0.0.0', port=5001)

# Configuração para CicloCarioca.pythonanywhere.com
# Esta aplicação será importada pelo arquivo WSGI
application = app

# Middleware para verificar se estamos no PythonAnywhere (sem limpar flash messages)
@app.before_request
def check_pythonanywhere():
    """Verificar se estamos no CicloCarioca.pythonanywhere.com"""
    if request.host and 'pythonanywhere' in request.host:
        # Apenas log para debug - NÃO limpar flash messages
        logger.info(f"Acessando via PythonAnywhere: {request.host}")
        # Removido: session.pop('_flashes', None) - estava impedindo exibição de erros