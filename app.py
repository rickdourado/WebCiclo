from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from datetime import datetime
import os
import functools
import logging

# Importar configurações e serviços
from config import Config, config
from services.course_service import CourseService
from services.validation_service import ValidationError

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

# Configuração do template folder
app.template_folder = 'templates'
app.static_folder = 'static'



# Simulação de banco de dados para cursos
COURSES_DB = []

# Lista de órgãos carregada do arquivo Listadecursos.txt
ORGAOS = [
    'Secretaria Municipal da Casa Civil',
    'Secretaria Municipal de Coordenação Governamental - SMCG',
    'Controladoria Geral do Município - CGM',
    'Procuradoria Geral do Município - PGM',
    'Secretaria Municipal de Fazenda - SMF',
    'Secretaria Municipal de Integridade, Transparência e Proteção de Dados - SMIT',
    'Secretaria Municipal de Desenvolvimento Urbano e Licenciamento - SMDU',
    'Secretaria Municipal de Desenvolvimento Econômico – SMDE',
    'Secretaria Municipal de Infraestrutura - SMI',
    'Secretaria Municipal de Ordem Pública - SEOP',
    'Secretaria Municipal de Conservação - SECONSERVA',
    'Secretaria Municipal de Educação - SME',
    'Secretaria Municipal de Assistência Social - SMAS',
    'Secretaria Municipal de Transportes - SMTR',
    'Secretaria Municipal de Saúde - SMS',
    'Secretaria Mun. do Envelhecimento Saudável e Qualidade de Vida - SEMESQV',
    'Secretaria de Esportes - SMEL',
    'Secretaria Especial da Juventude Carioca - JUV-RIO',
    'Secretaria Especial de Ação Comunitária - SEAC-RIO',
    'Secretaria Especial de Integração Metropolitana - SEIM',
    'Secretaria Especial de Políticas para Mulheres e  Cuidados - SPM-RIO',
    'Secretaria Municipal da Pessoa com Deficiência - SMPD',
    'Secretaria Municipal de Ciência, Tecnologia e Inovação - SMCT',
    'Secretaria Municipal de Cultura - SMC',
    'Secretaria Municipal de Habitação - SMH',
    'Secretaria Municipal do Ambiente e Clima - SMAC',
    'Secretaria Municipal de Proteção e Defesa dos Animais - SMPDA',
    'Secretaria Municipal de Trabalho e Renda - SMTE',
    'Secretaria Especial de Economia Solidária - SES-RIO',
    'Secretaria Municipal de Turismo - SMTUR-RIO',
    'Secretaria Especial de Cidadania e Família - SECID',
    'Empresa de Eventos do Município do Rio de Janeiro - RIOEVENTOS',
    'Companhia de Engenharia de Tráfego do RJ - CET-Rio',
    'Companhia Municipal de Energia e Iluminação - RIOLUZ',
    'Companhia Municipal de Limpeza Urbana – COMLURB',
    'Empresa de Turismo do Município do Rio de Janeiro - RIOTUR',
    'Empresa Distribuidora de Filmes S.A. - RIOFILME',
    'Empresa Municipal de Artes Gráficas - Imprensa da Cidade - IC',
    'Empresa Municipal de Informática - IPLANRIO',
    'Empresa Municipal de Multimeios Ltda. - MULTIRIO',
    'Empresa Municipal de Urbanização - RIO-URBE',
    'Empresa Pública de Saúde do Rio de Janeiro – RioSaúde',
    'Guarda Municipal do Rio de Janeiro - GM-Rio',
    'Instituto de Previdência e Assistência - PREVI-RIO',
    'Instituto Municipal de Urbanismo Pereira Passos - IPP',
    'Instituto Rio Patrimônio da Humanidade - IRPH',
    'Fundação Cidade das Artes',
    'Fundação Instituto das Águas do Município do Rio de Janeiro - RIO-ÁGUAS',
    'Fundação Instituto de Geotécnica do Município do Rio de Janeiro – GEO-RIO',
    'Fundação Parques e Jardins - FPJ',
    'Fundação Planetário da Cidade do Rio de Janeiro'
]

@app.route('/')
def index():
    """Página inicial com formulário de criação de curso"""
    # Limpar todas as mensagens flash ao acessar a página inicial
    session.pop('_flashes', None)
    
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
            for error in messages:
                flash(error, 'error')
            
            logger.warning(f"Falha na criação do curso: {messages}")
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"Erro interno ao criar curso: {str(e)}")
        flash(f'Erro interno ao criar curso: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/course/<int:course_id>')
def course_success(course_id):
    """Página de sucesso após criação do curso"""
    try:
        course = course_service.get_course(course_id)
        if not course:
            flash('Curso não encontrado', 'error')
            return redirect(url_for('index'))
        
        # Obter arquivos gerados
        csv_file = course.get('csv_file')
        pdf_file = course.get('pdf_file')
        
        return render_template('course_success.html', 
                               course=course, 
                               csv_file=csv_file, 
                               pdf_file=pdf_file)
    except Exception as e:
        logger.error(f"Erro ao buscar curso {course_id}: {str(e)}")
        flash('Erro ao carregar curso', 'error')
        return redirect(url_for('index'))

@app.route('/courses')
def list_courses():
    """Listar todos os cursos criados"""
    try:
        # Limpar mensagens flash ao acessar a lista de cursos
        if 'pythonanywhere' in request.host:
            session.pop('_flashes', None)
        
        # Usar o serviço para listar cursos
        courses = course_service.list_courses()
        
        return render_template('course_list.html', courses=courses)
    except Exception as e:
        logger.error(f"Erro ao listar cursos: {str(e)}")
        flash('Erro ao carregar lista de cursos', 'error')
        return redirect(url_for('index'))

# -----------------------------
# Rotas e helpers de autenticação admin
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
@login_required
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
                # Exibir erros de validação
                for error in messages:
                    flash(error, 'error')
                return redirect(url_for('edit_course', course_id=course_id))
        
        # Preparar dados para o formulário de edição
        course = _prepare_course_for_edit_form(course)
        return render_template('course_edit.html', course=course, orgaos=ORGAOS)
        
    except Exception as e:
        logger.error(f"Erro ao editar curso {course_id}: {str(e)}")
        flash(f'Erro ao editar curso: {str(e)}', 'error')
        return redirect(url_for('list_courses'))

def _prepare_course_for_edit_form(course):
    """Prepara dados do curso para o formulário de edição"""
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

# Middleware para verificar e limpar mensagens flash no CicloCarioca.pythonanywhere.com
@app.before_request
def check_pythonanywhere():
    """Verificar se estamos no CicloCarioca.pythonanywhere.com e limpar mensagens flash"""
    if request.host and 'pythonanywhere' in request.host:
        # Limpar mensagens flash em todas as requisições no PythonAnywhere
        if '_flashes' in session:
            session.pop('_flashes', None)