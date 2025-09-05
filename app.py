from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os

# Importar módulos para geração de arquivos
from scripts.csv_generator import generate_csv
from scripts.pdf_generator import generate_pdf
from scripts.csv_reader import read_csv_files, get_course_by_id
from scripts.id_manager import get_next_id, get_current_id

app = Flask(__name__)
# Configuração para produção no PythonAnywhere
app.secret_key = os.environ.get('SECRET_KEY', 'ciclo_carioca_v4_pythonanywhere_2025')

# Configuração do template folder
app.template_folder = 'templates'
app.static_folder = 'static'

# Simulação de banco de dados para cursos
COURSES_DB = []

# Dados de exemplo para órgãos
ORGAOS = [
    'Secretaria Municipal de Educação (SME)',
    'Secretaria Municipal de Saúde (SMS)',
    'Secretaria Municipal de Ciência e Tecnologia (SMCT)',
    'Secretaria Municipal de Trabalho e Emprego (SMTE)',
    'Secretaria Municipal de Desenvolvimento Urbano (SMDU)',
    'Secretaria Municipal de Meio Ambiente (SMAC)',
    'Secretaria Municipal de Cultura (SMC)',
    'Secretaria Municipal de Assistência Social (SMAS)',
    'Secretaria Municipal de Fazenda (SMF)',
    'Secretaria Municipal de Transportes (SMTR)',
    'Instituto de Vigilância Sanitária (IVISA)',
    'Empresa Municipal de Vigilância (EMV)',
    'Fundação Planetário da Cidade do Rio de Janeiro',
    'Instituto Pereira Passos (IPP)',
    'Empresa Municipal de Informática (IPLANRIO)'
]

@app.route('/')
def index():
    """Página inicial com formulário de criação de curso"""
    # Limpar mensagens flash ao acessar a página inicial
    # Isso evita que mensagens antigas apareçam no PythonAnywhere
    if 'pythonanywhere' in request.host:
        session.pop('_flashes', None)
    
    return render_template('course_form.html', 
                         orgaos=ORGAOS)

@app.route('/create_course', methods=['POST'])
def create_course():
    """Processar criação de novo curso"""
    try:
        # Capturar dados do formulário
        inicio_data = request.form.get('inicio_inscricoes_data')
        inicio_hora = request.form.get('inicio_inscricoes_hora')
        fim_data = request.form.get('fim_inscricoes_data')
        fim_hora = request.form.get('fim_inscricoes_hora')
        
        # Obter próximo ID disponível
        next_id = get_next_id()
        
        course_data = {
            'id': next_id,
            'titulo': request.form.get('titulo'),
            'descricao': request.form.get('descricao'),
            'inicio_inscricoes': f'{inicio_data.replace("-", "/")} {inicio_hora}' if inicio_data and inicio_hora else '',
            'fim_inscricoes': f'{fim_data.replace("-", "/")} {fim_hora}' if fim_data and fim_hora else '',
            'orgao': request.form.get('orgao'),
            'tema': request.form.get('tema'),
            'modalidade': request.form.get('modalidade'),
            'carga_horaria': request.form.get('carga_horaria'),
            'publico_alvo': request.form.get('publico_alvo'),
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
        
        flash('Curso criado com sucesso!', 'success')
        return redirect(url_for('course_success', course_id=course_data['id']))
        
    except Exception as e:
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
        
    csv_files = [f for f in os.listdir(csv_dir) if f.startswith(f"curso_{course_id}_")]
    pdf_files = [f for f in os.listdir(pdf_dir) if f.startswith(f"curso_{course_id}_")]
    
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
    return render_template('course_list.html', courses=courses)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎓 WebApp v4 - Ciclo Carioca (PythonAnywhere)")
    print("📋 Formulário de Criação de Cursos")
    print("🌐 Rodando em modo de produção")
    print("="*50 + "\n")
    
    # Configuração para desenvolvimento local
    app.run(debug=False, host='0.0.0.0', port=5001)

# Configuração para PythonAnywhere
# Esta aplicação será importada pelo arquivo WSGI
application = app

# Middleware para verificar e limpar mensagens flash no PythonAnywhere
@app.before_request
def check_pythonanywhere():
    """Verificar se estamos no PythonAnywhere e limpar mensagens flash"""
    if request.host and 'pythonanywhere' in request.host:
        # Limpar mensagens flash em todas as requisições no PythonAnywhere
        if '_flashes' in session:
            session.pop('_flashes', None)