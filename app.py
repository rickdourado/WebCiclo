from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os

# Importar módulos para geração de arquivos
from csv_generator import generate_csv
from pdf_generator import generate_pdf

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
        
        course_data = {
            'id': len(COURSES_DB) + 1,
            'titulo': request.form.get('titulo'),
            'descricao': request.form.get('descricao'),
            'inicio_inscricoes': f'{inicio_data} {inicio_hora}' if inicio_data and inicio_hora else '',
            'fim_inscricoes': f'{fim_data} {fim_hora}' if fim_data and fim_hora else '',
            'orgao': request.form.get('orgao'),
            'tema': request.form.get('tema'),
            'modalidade': request.form.get('modalidade'),
            'carga_horaria': request.form.get('carga_horaria'),
            'publico_alvo': request.form.get('publico_alvo'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Adicionar ao "banco de dados"
        COURSES_DB.append(course_data)
        
        # Gerar arquivos CSV e PDF
        try:
            csv_path = generate_csv(course_data)
            pdf_path = generate_pdf(course_data)
            flash(f'Arquivos gerados: CSV e PDF', 'info')
        except Exception as file_error:
            flash(f'Erro ao gerar arquivos: {str(file_error)}', 'warning')
        
        flash('Curso criado com sucesso!', 'success')
        return redirect(url_for('course_success', course_id=course_data['id']))
        
    except Exception as e:
        flash(f'Erro ao criar curso: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/course/<int:course_id>')
def course_success(course_id):
    """Página de sucesso após criação do curso"""
    course = next((c for c in COURSES_DB if c['id'] == course_id), None)
    if not course:
        flash('Curso não encontrado', 'error')
        return redirect(url_for('index'))
    
    # Verificar se existem arquivos gerados para este curso
    csv_files = [f for f in os.listdir('CSV') if f.startswith(f"curso_{course_id}_")]
    pdf_files = [f for f in os.listdir('PDF') if f.startswith(f"curso_{course_id}_")]
    
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
    return render_template('course_list.html', courses=COURSES_DB)

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