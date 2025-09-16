from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from datetime import datetime
import os
import functools
from dotenv import load_dotenv
import google.generativeai as genai

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Importar módulos para geração de arquivos
from scripts.csv_generator import generate_csv
from scripts.pdf_generator import generate_pdf
from scripts.csv_reader import read_csv_files, get_course_by_id
from scripts.id_manager import get_next_id, get_current_id

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ciclo_carioca_v4_pythonanywhere_2025')

# Configuração do Gemini
gemini_api_key = os.environ.get('GEMINI_API_KEY')
print(f"GEMINI_API_KEY configurada: {'Sim' if gemini_api_key else 'Não'}")
if gemini_api_key:
    print(f"GEMINI_API_KEY (primeiros 10 chars): {gemini_api_key[:10]}...")
    genai.configure(api_key=gemini_api_key)
else:
    print("AVISO: GEMINI_API_KEY não configurada. A função de melhoria de descrição não estará disponível.")

# Função para melhorar a descrição usando Gemini
def enhance_description(description):
    print(f"\nTentando melhorar descrição com Gemini...")
    print(f"Descrição original: {description}")
    
    # Verificar se a API key está configurada
    if not os.environ.get('GEMINI_API_KEY'):
        print("API key do Gemini não configurada. Retornando descrição original.")
        return description
    
    try:
        print("Configurando modelo Gemini...")
        model = genai.GenerativeModel(model_name='gemini-1.5-pro')
        
        prompt = f"""Explique de forma simples o que o curso ensina em no máximo 3 linhas. Mantenha em português, seja direto e objetivo:

{description}"""
        print("Enviando prompt para o Gemini...")
        
        response = model.generate_content(prompt)
        enhanced = response.text.strip()
        
        print(f"Descrição melhorada: {enhanced}")
        return enhanced
    except Exception as e:
        print(f"\nERRO ao melhorar descrição com Gemini: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")
        import traceback
        print(f"Traceback completo:\n{traceback.format_exc()}")
        return description

# Configuração do template folder
app.template_folder = 'templates'
app.static_folder = 'static'

# Configuração para upload de imagens
UPLOAD_FOLDER = os.path.join('static', 'images', 'uploads')
LOGO_PARCEIROS_FOLDER = os.path.join('static', 'images', 'LOGOPARCEIROS')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['LOGO_PARCEIROS_FOLDER'] = LOGO_PARCEIROS_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_partner_logo(file, partner_name):
    """Salva a logo do parceiro no diretório LOGOPARCEIROS com o nome do parceiro"""
    print(f"\n=== SALVANDO LOGO DO PARCEIRO ===")
    print(f"File: {file}")
    print(f"Partner name: {partner_name}")
    print(f"File filename: {file.filename if file else 'None'}")
    
    if file and file.filename and file.filename != '' and allowed_file(file.filename):
        try:
            # Criar diretório se não existir
            logo_dir = app.config['LOGO_PARCEIROS_FOLDER']
            print(f"Logo directory: {logo_dir}")
            
            if not os.path.exists(logo_dir):
                print(f"Criando diretório: {logo_dir}")
                os.makedirs(logo_dir)
            else:
                print(f"Diretório já existe: {logo_dir}")
            
            # Obter extensão do arquivo
            extension = file.filename.rsplit('.', 1)[1].lower()
            print(f"Extension: {extension}")
            
            # Criar nome do arquivo: nome_do_parceiro.extensão
            # Limpar caracteres especiais do nome do parceiro
            clean_name = "".join(c for c in partner_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_name = clean_name.replace(' ', '_')
            filename = f"{clean_name}.{extension}"
            print(f"Clean name: {clean_name}")
            print(f"Final filename: {filename}")
            
            # Caminho completo do arquivo
            file_path = os.path.join(logo_dir, filename)
            print(f"Full file path: {file_path}")
            
            # Verificar se arquivo já existe
            if os.path.exists(file_path):
                print(f"AVISO: Arquivo já existe e será sobrescrito: {file_path}")
            else:
                print(f"Arquivo novo será criado: {file_path}")
            
            # Salvar arquivo (sobrescreve se já existir)
            file.save(file_path)
            print(f"Arquivo salvo com sucesso: {file_path}")
            
            # Verificar se arquivo foi salvo
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"Confirmação: Arquivo existe com {file_size} bytes")
            else:
                print(f"ERRO: Arquivo não foi salvo corretamente")
            
            return filename
        except Exception as e:
            print(f"ERRO ao salvar logo do parceiro: {str(e)}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            return None
    else:
        print(f"Arquivo inválido ou não permitido")
        if file:
            print(f"File filename: {file.filename}")
            print(f"Allowed file: {allowed_file(file.filename)}")
        return None



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

# Remover função de verificação de extensões de arquivo
@app.route('/create_course', methods=['POST'])
def create_course():
    try:
        print("\n=== INICIANDO CRIAÇÃO DE CURSO ===")
        print(f"Método: {request.method}")
        print(f"Form data keys: {list(request.form.keys())}")
        print(f"Files keys: {list(request.files.keys())}")
        
        # Log detalhado de todos os campos do formulário
        print("\n=== DADOS DO FORMULÁRIO ===")
        for key, value in request.form.items():
            print(f"{key}: {value}")
        
        # Log específico para campos problemáticos
        print(f"\n=== CAMPOS ESPECÍFICOS ===")
        print(f"dias_aula[]: {request.form.getlist('dias_aula[]')}")
        print(f"parceiro_externo: {request.form.get('parceiro_externo')}")
        print(f"parceiro_nome: {request.form.get('parceiro_nome')}")
        print(f"modalidade: {request.form.get('modalidade')}")
        print(f"endereco_unidade[]: {request.form.getlist('endereco_unidade[]')}")
        print(f"horario_inicio[]: {request.form.getlist('horario_inicio[]')}")
        print(f"horario_fim[]: {request.form.getlist('horario_fim[]')}")
        
        # Capturar dados do formulário
        inicio_data = request.form.get('inicio_inscricoes_data')
        fim_data = request.form.get('fim_inscricoes_data')
        
        # Obter próximo ID disponível
        next_id = get_next_id()
        
        # Melhorar a descrição usando Gemini
        original_description = request.form.get('descricao')
        print(f"\n=== PROCESSANDO DESCRIÇÃO ===")
        print(f"Descrição original: {original_description}")
        print("Chamando enhance_description...")
        
        try:
            enhanced_description = enhance_description(original_description)
            print(f"Descrição melhorada: {enhanced_description}")
        except Exception as desc_error:
            print(f"ERRO ao processar descrição: {str(desc_error)}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            enhanced_description = original_description
            print("Usando descrição original devido ao erro.")
        
        # Processar logo do parceiro se fornecido
        partner_logo_filename = None
        print(f"\n=== PROCESSANDO PARCEIRO EXTERNO ===")
        print(f"parceiro_externo: {request.form.get('parceiro_externo')}")
        print(f"parceiro_nome: {request.form.get('parceiro_nome')}")
        print(f"parceiro_logo file: {request.files.get('parceiro_logo')}")
        
        if request.form.get('parceiro_externo') == 'sim':
            partner_name = request.form.get('parceiro_nome', '')
            logo_file = request.files.get('parceiro_logo')
            print(f"Partner name: {partner_name}")
            print(f"Logo file: {logo_file}")
            print(f"Logo file filename: {logo_file.filename if logo_file else 'None'}")
            
            if logo_file and partner_name:
                print("Chamando save_partner_logo...")
                try:
                    partner_logo_filename = save_partner_logo(logo_file, partner_name)
                    print(f"Logo salva com filename: {partner_logo_filename}")
                except Exception as logo_error:
                    print(f"ERRO ao salvar logo: {str(logo_error)}")
                    import traceback
                    print(f"Traceback logo:\n{traceback.format_exc()}")
                    partner_logo_filename = None
            else:
                print("Logo não será salva (arquivo ou nome do parceiro em branco)")
        else:
            print("Parceiro externo = 'nao', não processando logo")
        
        course_data = {
                'id': next_id,
                'titulo': request.form.get('titulo'),
                'descricao': enhanced_description,
                'descricao_original': original_description,
                'inicio_inscricoes': f'{inicio_data.replace("-", "/")}' if inicio_data else '',
                'fim_inscricoes': f'{fim_data.replace("-", "/")}' if fim_data else '',
                'orgao': request.form.get('orgao'),
                'tema': request.form.get('tema'),
                'modalidade': request.form.get('modalidade'),
                'plataforma_digital': request.form.get('plataforma_digital') if request.form.get('modalidade') == 'Online' else '',
                'carga_horaria': request.form.get('carga_horaria'),
                'dias_aula': ', '.join(request.form.getlist('dias_aula[]')) if request.form.getlist('dias_aula[]') else '',
                'endereco_unidade': ', '.join(request.form.getlist('endereco_unidade[]')) if request.form.getlist('endereco_unidade[]') else '',
                'bairro_unidade': ', '.join(request.form.getlist('bairro_unidade[]')) if request.form.getlist('bairro_unidade[]') else '',
                'vagas_unidade': ', '.join(request.form.getlist('vagas_unidade[]')) if request.form.getlist('vagas_unidade[]') else '',
                'inicio_aulas_data': ', '.join(request.form.getlist('inicio_aulas_data[]')) if request.form.getlist('inicio_aulas_data[]') else '',
                'fim_aulas_data': ', '.join(request.form.getlist('fim_aulas_data[]')) if request.form.getlist('fim_aulas_data[]') else '',
                'horario_inicio': ', '.join([h for h in request.form.getlist('horario_inicio[]') if h.strip()]) if request.form.getlist('horario_inicio[]') else '',
                'horario_fim': ', '.join([h for h in request.form.getlist('horario_fim[]') if h.strip()]) if request.form.getlist('horario_fim[]') else '',
            'curso_gratuito': request.form.get('curso_gratuito'),
            'valor_curso': request.form.get('valor_curso') if request.form.get('curso_gratuito') == 'nao' else '',
            'oferece_bolsa': request.form.get('oferece_bolsa'),
            'valor_bolsa': request.form.get('valor_bolsa') if request.form.get('oferece_bolsa') == 'sim' else '',
            'requisitos_bolsa': request.form.get('requisitos_bolsa') if request.form.get('oferece_bolsa') == 'sim' else '',
            'publico_alvo': request.form.get('publico_alvo'),
            'oferece_certificado': request.form.get('oferece_certificado'),
            'pre_requisitos': request.form.get('pre_requisitos') if request.form.get('oferece_certificado') == 'sim' else '',
            'info_complementares': request.form.get('info_complementares'),
            'parceiro_externo': request.form.get('parceiro_externo'),
            'parceiro_nome': request.form.get('parceiro_nome') if request.form.get('parceiro_externo') == 'sim' else '',
            'parceiro_link': request.form.get('parceiro_link') if request.form.get('parceiro_externo') == 'sim' else '',
            'parceiro_logo': partner_logo_filename if partner_logo_filename else '',
            'created_at': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        }
        
        # Adicionar ao "banco de dados"
        COURSES_DB.append(course_data)
        
        # Garantir que os diretórios existam
        csv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CSV')
        pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PDF')
        
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
            
        # Gerar arquivos CSV e PDF
        try:
            print(f"Tentando gerar arquivo CSV para o curso {course_data['id']}")
            print(f"Diretório de trabalho atual: {os.getcwd()}")
            print(f"Diretório CSV: {csv_dir}")
            print(f"Diretório PDF: {pdf_dir}")
            print(f"Verificando se os diretórios existem: CSV={os.path.exists(csv_dir)}, PDF={os.path.exists(pdf_dir)}")
            
            csv_path = generate_csv(course_data)
            print(f"CSV gerado com sucesso: {csv_path}")
            print(f"Arquivo CSV existe? {os.path.exists(csv_path)}")
            
            print(f"Tentando gerar arquivo PDF para o curso {course_data['id']}")
            pdf_path = generate_pdf(course_data)
            print(f"PDF gerado com sucesso: {pdf_path}")
            print(f"Arquivo PDF existe? {os.path.exists(pdf_path)}")
            
            flash(f'Arquivos gerados: CSV e PDF', 'info')
        except Exception as file_error:
            print(f"ERRO ao gerar arquivos: {str(file_error)}")
            import traceback
            print(traceback.format_exc())
            flash(f'Erro ao gerar arquivos: {str(file_error)}', 'warning')
        
        print(f"\n=== CURSO CRIADO COM SUCESSO ===")
        print(f"ID do curso: {course_data['id']}")
        print(f"Total de cursos no banco: {len(COURSES_DB)}")
        print(f"Redirecionando para: course_success/{course_data['id']}")
        
        flash('Curso criado com sucesso!', 'success')
        return redirect(url_for('course_success', course_id=course_data['id']))
        
    except Exception as e:
        print(f"\n=== ERRO AO CRIAR CURSO ===")
        print(f"Erro: {str(e)}")
        import traceback
        print(f"Traceback completo:\n{traceback.format_exc()}")
        flash(f'Erro ao criar curso: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/course/<int:course_id>')
def course_success(course_id):
    """Página de sucesso após criação do curso"""
    # Buscar curso pelo ID nos arquivos CSV
    course = get_course_by_id(course_id)
    if not course:
        # Tentar buscar no banco de dados em memória
        course = next((c for c in COURSES_DB if c['id'] == course_id), None)
        if not course:
            flash('Curso não encontrado', 'error')
            return redirect(url_for('index'))
    
    # Verificar se existem arquivos gerados para este curso
    csv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CSV')
    pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PDF')
    
    # Garantir que os diretórios existam
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        
    # Buscar arquivos pelo título do curso em vez do ID
    if course:
        titulo_formatado = course['titulo'].replace(' ', '_')
        csv_files = [f for f in os.listdir(csv_dir) if titulo_formatado in f]
        pdf_files = [f for f in os.listdir(pdf_dir) if titulo_formatado in f]
    else:
        csv_files = []
        pdf_files = []
    
    # Obter os arquivos mais recentes (se existirem)
    latest_csv = csv_files[-1] if csv_files else None
    latest_pdf = pdf_files[-1] if pdf_files else None
    
    return render_template('course_success.html', 
                           course=course, 
                           csv_file=latest_csv, 
                           pdf_file=latest_pdf)

@app.route('/courses')
def list_courses():
    """Listar todos os cursos criados"""
    # Limpar mensagens flash ao acessar a lista de cursos
    # Isso evita que mensagens antigas apareçam no PythonAnywhere
    if 'pythonanywhere' in request.host:
        session.pop('_flashes', None)
    
    # Ler todos os cursos dos arquivos CSV
    courses = read_csv_files()
    
    # Não é necessário recodificar os dados, pois já estão em UTF-8
    # Os arquivos CSV são lidos com encoding='utf-8' no csv_reader.py
    
    return render_template('course_list.html', courses=courses)

# -----------------------------
# Rotas e helpers de autenticação admin
# -----------------------------
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

# Verificar se as credenciais foram configuradas
if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise ValueError('As credenciais de admin (ADMIN_USERNAME e ADMIN_PASSWORD) precisam ser configuradas nas variáveis de ambiente.')

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
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
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
    # Reutiliza leitura de cursos já existente
    courses = read_csv_files()
    return render_template('course_list.html', courses=courses)

# -----------------------------
# Fim da seção de autenticação admin
# -----------------------------

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    """Editar um curso existente"""
    # Buscar curso pelo ID
    course = get_course_by_id(course_id)
    
    if not course:
        flash('Curso não encontrado', 'error')
        return redirect(url_for('list_courses'))
    
    if request.method == 'POST':
        try:
            # Capturar dados do formulário
            inicio_data = request.form.get('inicio_inscricoes_data')
            fim_data = request.form.get('fim_inscricoes_data')
            
            # Converter datas do formato YYYY-MM-DD para DD-MM-AAAA
            inicio_inscricoes = ''
            if inicio_data:
                try:
                    ano, mes, dia = inicio_data.split('-')
                    inicio_inscricoes = f'{dia}-{mes}-{ano}'
                except:
                    inicio_inscricoes = course.get('inicio_inscricoes', '')
            else:
                inicio_inscricoes = course.get('inicio_inscricoes', '')
                
            fim_inscricoes = ''
            if fim_data:
                try:
                    ano, mes, dia = fim_data.split('-')
                    fim_inscricoes = f'{dia}-{mes}-{ano}'
                except:
                    fim_inscricoes = course.get('fim_inscricoes', '')
            else:
                fim_inscricoes = course.get('fim_inscricoes', '')
            
            # Atualizar dados do curso
            # Capturar a descrição original do formulário
            original_description = request.form.get('original_description')
            
            # Melhorar a descrição usando Gemini se foi alterada
            if original_description != course.get('descricao_original', ''):
                enhanced_description = enhance_description(original_description)
            else:
                enhanced_description = course.get('descricao', original_description)
            
            # Processar logo do parceiro se fornecido
            partner_logo_filename = None
            if request.form.get('parceiro_externo') == 'sim':
                partner_name = request.form.get('parceiro_nome', '')
                logo_file = request.files.get('parceiro_logo')
                if logo_file and partner_name:
                    partner_logo_filename = save_partner_logo(logo_file, partner_name)
                elif course.get('parceiro_logo'):
                    # Manter logo existente se não foi enviada nova
                    partner_logo_filename = course.get('parceiro_logo')
                
            course_data = {
                'id': course_id,
                'titulo': request.form.get('titulo'),
                'descricao': enhanced_description,
                'descricao_original': original_description,
                'inicio_inscricoes': inicio_inscricoes,
                'fim_inscricoes': fim_inscricoes,
                'orgao': request.form.get('orgao'),
                'tema': request.form.get('tema'),
                'modalidade': request.form.get('modalidade'),
                'plataforma_digital': request.form.get('plataforma_digital') if request.form.get('modalidade') == 'Online' else '',
                'carga_horaria': request.form.get('carga_horaria'),
                'dias_aula': ', '.join(request.form.getlist('dias_aula[]')) if request.form.getlist('dias_aula[]') else '',
                'endereco_unidade': ', '.join(request.form.getlist('endereco_unidade[]')) if request.form.getlist('endereco_unidade[]') else '',
                'bairro_unidade': ', '.join(request.form.getlist('bairro_unidade[]')) if request.form.getlist('bairro_unidade[]') else '',
                'vagas_unidade': ', '.join(request.form.getlist('vagas_unidade[]')) if request.form.getlist('vagas_unidade[]') else '',
                'inicio_aulas_data': ', '.join(request.form.getlist('inicio_aulas_data[]')) if request.form.getlist('inicio_aulas_data[]') else '',
                'fim_aulas_data': ', '.join(request.form.getlist('fim_aulas_data[]')) if request.form.getlist('fim_aulas_data[]') else '',
                'horario_inicio': ', '.join([h for h in request.form.getlist('horario_inicio[]') if h.strip()]) if request.form.getlist('horario_inicio[]') else '',
                'horario_fim': ', '.join([h for h in request.form.getlist('horario_fim[]') if h.strip()]) if request.form.getlist('horario_fim[]') else '',
                'curso_gratuito': request.form.get('curso_gratuito'),
                'valor_curso': request.form.get('valor_curso') if request.form.get('curso_gratuito') == 'nao' else '',
                'oferece_bolsa': request.form.get('oferece_bolsa'),
                'valor_bolsa': request.form.get('valor_bolsa') if request.form.get('oferece_bolsa') == 'sim' else '',
                'requisitos_bolsa': request.form.get('requisitos_bolsa') if request.form.get('oferece_bolsa') == 'sim' else '',
                'publico_alvo': request.form.get('publico_alvo'),
                'oferece_certificado': request.form.get('oferece_certificado'),
                'pre_requisitos': request.form.get('pre_requisitos') if request.form.get('oferece_certificado') == 'sim' else '',
                'info_complementares': request.form.get('info_complementares'),
                'parceiro_externo': request.form.get('parceiro_externo'),
                'parceiro_nome': request.form.get('parceiro_nome') if request.form.get('parceiro_externo') == 'sim' else '',
                'parceiro_link': request.form.get('parceiro_link') if request.form.get('parceiro_externo') == 'sim' else '',
                'parceiro_logo': partner_logo_filename if partner_logo_filename else '',
                'created_at': course.get('created_at', datetime.now().strftime('%d-%m-%Y %H:%M:%S')),
                'updated_at': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            }
            
            # Gerar novos arquivos CSV e PDF
            try:
                csv_path = generate_csv(course_data)
                pdf_path = generate_pdf(course_data)
                flash(f'Arquivos atualizados: CSV e PDF', 'info')
            except Exception as file_error:
                flash(f'Erro ao gerar arquivos: {str(file_error)}', 'warning')
            
            flash('Curso atualizado com sucesso!', 'success')
            return redirect(url_for('course_edit_success', course_id=course_id))
            
        except Exception as e:
            flash(f'Erro ao atualizar curso: {str(e)}', 'error')
            return redirect(url_for('edit_course', course_id=course_id))
    
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
            print(f"Erro ao converter data de início: {e}")
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
            print(f"Erro ao converter data de fim: {e}")
            course['fim_inscricoes_data'] = ''
    else:
        course['fim_inscricoes_data'] = ''
    
    return render_template('course_edit.html', course=course, orgaos=ORGAOS)

@app.route('/course_edit_success/<int:course_id>')
@login_required
def course_edit_success(course_id):
    """Exibir página de sucesso após edição do curso"""
    course = get_course_by_id(course_id)
    if not course:
        flash('Curso não encontrado', 'error')
        return redirect(url_for('list_courses'))
    return render_template('course_edit_success.html', course=course)

@app.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    """Excluir um curso existente e seus arquivos"""
    try:
        # Buscar curso pelo ID
        course = get_course_by_id(course_id)
        
        if not course:
            flash('Curso não encontrado', 'error')
            return redirect(url_for('list_courses'))
        
        # Obter o título formatado do curso para encontrar os arquivos
        titulo_formatado = course['titulo'].replace(' ', '_')
        
        # Encontrar e excluir o arquivo CSV
        csv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CSV')
        csv_files = [f for f in os.listdir(csv_dir) if titulo_formatado in f]
        for csv_file in csv_files:
            os.remove(os.path.join(csv_dir, csv_file))
        
        # Encontrar e excluir o arquivo PDF
        pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PDF')
        pdf_files = [f for f in os.listdir(pdf_dir) if titulo_formatado in f]
        for pdf_file in pdf_files:
            os.remove(os.path.join(pdf_dir, pdf_file))
        
        flash('Curso excluído com sucesso!', 'success')
        return redirect(url_for('list_courses'))
        
    except Exception as e:
        flash(f'Erro ao excluir curso: {str(e)}', 'error')
        return redirect(url_for('list_courses'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """Rota para download de arquivos CSV e PDF"""
    if filename.endswith('.csv'):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CSV')
    elif filename.endswith('.pdf'):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PDF')
    else:
        flash('Tipo de arquivo não suportado', 'error')
        return redirect(url_for('index'))
    
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
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