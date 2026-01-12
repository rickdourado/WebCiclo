from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_from_directory,
)
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import os
import functools
import logging

# Importar configurações e serviços
from config import Config, config
from services.course_service import CourseService
from services.validation_service import ValidationError
from services.course_status_service import CourseStatusService
from services.auth_service import AuthService

# Importar formulários
from forms import LoginForm, CourseForm, CourseStatusForm, DeleteCourseForm

# Configurar aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar proteção CSRF
csrf = CSRFProtect(app)


# Filtros Jinja2 customizados para lidar com tipos do MySQL
@app.template_filter("safe_str")
def safe_str_filter(value):
    """Converte qualquer valor para string de forma segura"""
    if value is None:
        return ""
    return str(value)


@app.template_filter("format_date")
def format_date_filter(value):
    """Formata data para DD/MM/YYYY sem horas, aceitando múltiplos formatos de entrada"""
    if not value:
        return ""

    # Converter para string se não for
    date_str = str(value)

    # Se já tem espaço (timestamp), usar apenas a parte da data
    if " " in date_str:
        date_str = date_str.split(" ")[0]

    # Se está no formato YYYY-MM-DD
    if "-" in date_str and len(date_str.split("-")[0]) == 4:
        parts = date_str.split("-")
        if len(parts) == 3:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"

    # Se está no formato DD/MM/YYYY
    if "/" in date_str:
        parts = date_str.split("/")
        if len(parts) == 3:
            # Se o primeiro tem 4 dígitos (YYYY/MM/DD), converter
            if len(parts[0]) == 4:
                return f"{parts[2]}/{parts[1]}/{parts[0]}"
            # Senão, já está em DD/MM/YYYY
            else:
                return date_str

    # Se não conseguiu converter, retornar original
    return date_str


@app.template_filter("format_currency")
def format_currency_filter(value):
    """Formata valores monetários"""
    if not value:
        return ""
    value_str = str(value)
    if value_str.startswith("R$"):
        return value_str
    return f"R$ {value_str}"


@app.template_filter("safe_split")
def safe_split_filter(value, separator="|"):
    """Split seguro que retorna lista vazia se valor não for string"""
    if not value:
        return []
    if not isinstance(value, str):
        value = str(value)
    return value.split(separator)


# Handler para erros CSRF
@app.errorhandler(400)
def csrf_error(e):
    """Handler personalizado para erros CSRF"""
    # Verificar se é realmente um erro CSRF e não um erro de validação
    error_description = str(e.description) if hasattr(e, "description") else str(e)
    if "CSRF" in error_description or "csrf" in error_description.lower():
        logger.warning(f"🔒 Erro CSRF detectado: {e}")
        flash(
            "Erro de segurança: Token CSRF inválido ou expirado. Tente novamente.",
            "error",
        )
        return redirect(request.referrer or url_for("index"))
    # Se não for erro CSRF, deixar o Flask tratar normalmente
    return e


# Middleware de segurança
@app.after_request
def add_security_headers(response):
    """Adiciona headers de segurança às respostas"""
    # Proteção contra XSS
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Política de segurança de conteúdo básica
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https://cdnjs.cloudflare.com; "
        "connect-src 'self';"
    )

    # Referrer policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


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
auth_service = AuthService()

# Configuração do template folder
app.template_folder = "templates"
app.static_folder = "static"


# Simulação de banco de dados para cursos
COURSES_DB = []

# Lista de órgãos carregada do arquivo Listadecursos.txt
ORGAOS = [
    "Secretaria Municipal da Casa Civil - CVL",
    "Secretaria Municipal de Coordenação Governamental - SMCG",
    "Secretaria Municipal de Fazenda - SMF",
    "Secretaria Municipal de Integridade, Transparência e Proteção de Dados - SMIT",
    "Secretaria Municipal de Desenvolvimento Urbano e Licenciamento - SMDU",
    "Secretaria Municipal de Desenvolvimento Econômico – SMDE",
    "Secretaria Municipal de Infraestrutura - SMI",
    "Secretaria Municipal de Transportes - SMTR",
    "Secretaria Municipal de Conservação - SECONSERVA",
    "Secretaria Municipal de Educação - SME",
    "Secretaria Municipal de Assistência Social - SMAS",
    "Secretaria Municipal de Saúde - SMS",
    "Secretaria Municipalk de Administração - SMA",
    "Secretaria Municipal de Trabalho e Renda - SMTE",
    "Secretaria Municipal de Cultura - SMC",
    "Secretaria Municipal da Pessoa com Deficiência - SMPD",
    "Secretaria Municipal do Ambiente e Clima - SMAC",
    "Secretaria de Esportes - SMEL",
    "Secretaria Municipal de Habitação - SMH",
    "Secretaria Municipal de Ciência, Tecnologia e Inovação - SMCT",
    "Secretaria Mun. do Envelhecimento Saudável e Qualidade de Vida - SEMESQV",
    "Secretaria Municipal de Ordem Pública - SEOP",
    "Secretaria Municipal de Proteção e Defesa dos Animais - SMPDA",
    "Secretaria Municipal de Turismo - SMTUR-RIO",
    "Secretaria Especial de Proteção e Defesa do Consumidor - SEDECON",
    "Secretaria Especial de Políticas para Mulheres e  Cuidados - SPM-RIO",
    "Secretaria Especial da Juventude Carioca - JUV-RIO",
    "Secretaria Especial de Ação Comunitária - SEAC-RIO",
    "Secretaria Especial de Cidadania e Família - SECID",
    "Secretaria Especial de Integração Metropolitana - SEIM",
    "Secretaria Especial de Economia Solidária - SES-RIO",
    "Secretaria Especial de Direitos HUmanos e Igualdade Racial - SEDHIR",
    "Secretaria Especial de Inclusão - SINC-RIO",
    "Arquivo Geral da Cidade do Rio de Janeiro - C/ARQ",
    "Controladoria Geral do Município - CGM-RIO",
    "Procuradoria Geral do Município - PGM",
    "Instituto de Previdência e Assistência - PREVI-RIO",
    "Instituto Fundação João Goulart - CVL/FJG",
    "Instituto Municipal de Urbanismo Pereira Passos - IPP",
    "Instituto Municipal de Vigilância Sanitária, Vigilância de Zoonoses e de Inspeção Agropecuária - S/IVISA-RIO",
    "Guarda Municipal do Rio de Janeiro - GM-RIO",
    "Fundação Instituto de Geotécnica do Município do Rio de Janeiro – GEO-RIO",
    "Fundação Instituto das Águas do Município do Rio de Janeiro - RIO-ÁGUAS",
    "Fundação Parques e Jardins - FPJ",
    "Fundação Planetário da Cidade do Rio de Janeiro - PLANETÁRIO",
    "Fundação Jardim Zoológico da Cidade do Rio de Janeiro - RIO-ZOO",
    "Fundação Cidade das Artes - CIDADE DAS ARTES",
    "Empresa Municipal de Multimeios S.A. - MULTIRIO",
    "Distribuidora de Filmes S.A. - RIOFILME",
    "Empresa Municipal de Informática - IPLANRIO",
    "Empresa Municipal de Artes Gráficas - IMPRENSA DA CIDADE",
    "Companhia Carioca de Parcerias e Investimentos - CCPAR",
    "Empresa Municipal de Urbanização - RIO-URBE",
    "Empresa de Turismo do Município do Rio de Janeiro - RIOTUR",
    "Empresa Pública de Saúde do Rio de Janeiro – RIOSAÚDE",
    "Companhia Municipal de Energia e Iluminação - RIOLUZ",
    "Companhia Municipal de Limpeza Urbana – COMLURB",
    "Companhia de Engenharia de Tráfego do RJ - CET-RIO",
    "Companhia Municipal de Transportes Coletivos - CMTC-RIO",
    "Riocentro S.A. - Centro de Feiras, Exposições e Congressos do Rio de Janeiro - RIOCENTRO",
    "Agência de Fomento do Município do Rio de Janeiro S.A. - INVEST.RIO",
    "Empresa de Eventos do Município do Rio de Janeiro - RIOEVENTOS",
    "Instituto Rio Patrimônio da Humanidade - IRPH",
]


@app.route("/")
def index():
    """Página inicial com formulário de criação de curso"""
    # Limpar apenas mensagens de sucesso ao acessar a página inicial
    # Isso evita que mensagens de sucesso apareçam quando o usuário volta da página de sucesso
    # Mas mantém mensagens de erro de validação para serem exibidas
    if "_flashes" in session:
        flashes = session["_flashes"]
        # Manter apenas mensagens de erro e warning, remover sucesso
        session["_flashes"] = [
            flash for flash in flashes if flash[0] in ["error", "warning"]
        ]

    # Data atual para preenchimento automático dos campos de data
    from datetime import datetime

    today_date = datetime.now().strftime("%Y-%m-%d")

    return render_template("index.html", orgaos=ORGAOS, today_date=today_date)


@app.route("/create_course", methods=["POST"])
def create_course():
    """Cria um novo curso usando o serviço de cursos com proteção CSRF"""
    try:
        # Validar CSRF token
        csrf.protect()

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
        success, course_data, messages = course_service.create_course(
            request.form, request.files
        )

        if success:
            logger.info(f"Curso criado com sucesso: ID {course_data['id']}")

            # Exibir avisos se houver
            for warning in messages:
                flash(warning, "warning")

            flash("Curso criado com sucesso!", "success")
            return redirect(url_for("course_success", course_id=course_data["id"]))
        else:
            # Exibir erros de validação
            logger.warning(f"Falha na criação do curso: {messages}")
            for error in messages:
                flash(error, "error")
                logger.warning(f"Erro de validação: {error}")

            # Log detalhado para debug
            logger.info("Dados do formulário que falharam na validação:")
            for key, value in request.form.items():
                logger.info(f"  {key}: {value}")

            return redirect(url_for("index"))

    except Exception as e:
        logger.error(f"Erro interno ao criar curso: {str(e)}")
        logger.error(f"Tipo do erro: {type(e).__name__}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        flash(f"Erro interno ao criar curso: {str(e)}", "error")
        return redirect(url_for("index"))


@app.route("/course/<int:course_id>")
def course_success(course_id):
    """Página de sucesso após criação do curso"""
    try:
        logger.info(f"🎉 Acessando página de sucesso para curso ID: {course_id}")
        course = course_service.get_course(course_id)
        if not course:
            logger.warning(f"❌ Curso {course_id} não encontrado na página de sucesso")
            flash("Curso não encontrado", "error")
            return redirect(url_for("index"))

        # Obter arquivos gerados
        csv_file = course.get("csv_file")
        pdf_file = course.get("pdf_file")

        logger.info(
            f"✅ Renderizando página de sucesso para: {course.get('titulo', 'Curso sem título')}"
        )
        logger.info(f"📄 Arquivos: CSV={csv_file}, PDF={pdf_file}")

        return render_template(
            "course_success.html", course=course, csv_file=csv_file, pdf_file=pdf_file
        )
    except Exception as e:
        logger.error(f"Erro ao buscar curso {course_id}: {str(e)}")
        flash("Erro ao carregar curso", "error")
        return redirect(url_for("index"))


@app.route("/courses/public")
def public_courses():
    """Lista pública de cursos - apenas visualização e duplicação"""
    try:
        # Log para debug no PythonAnywhere
        if "pythonanywhere" in request.host:
            logger.info("Acessando lista pública de cursos via PythonAnywhere")

        # Usar o serviço para listar cursos
        courses = course_service.list_courses()

        return render_template("course_list_public.html", courses=courses)
    except Exception as e:
        logger.error(f"Erro ao listar cursos públicos: {str(e)}")
        flash("Erro ao carregar lista de cursos", "error")
        return redirect(url_for("index"))


# -----------------------------
# Decorator de autenticação
# -----------------------------


def login_required(view_func):
    """Decorator para proteger rotas que exigem login de admin"""

    @functools.wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Faça login para acessar esta página.", "warning")
            # Incluir parâmetro next para redirecionar após login
            return redirect(url_for("admin_login", next=request.url))
        return view_func(*args, **kwargs)

    return wrapped_view


@app.route("/courses")
@login_required
def list_courses():
    """Listar todos os cursos criados - área administrativa"""
    try:
        # Log para debug no PythonAnywhere
        if "pythonanywhere" in request.host:
            logger.info("Acessando lista de cursos via PythonAnywhere")

        # Usar o serviço para listar cursos
        courses = course_service.list_courses()

        # Obter status dos cursos inseridos
        inserted_courses = course_status_service.get_inserted_courses()

        # Adicionar status aos cursos
        for course in courses:
            # Converter ID do curso para int para comparação correta
            course_id = course.get("id")
            if isinstance(course_id, str) and course_id.isdigit():
                course_id = int(course_id)
            course["is_inserted"] = course_id in inserted_courses

        return render_template(
            "course_list.html", courses=courses, inserted_courses=inserted_courses
        )
    except Exception as e:
        logger.error(f"Erro ao listar cursos: {str(e)}")
        flash("Erro ao carregar lista de cursos", "error")
        return redirect(url_for("index"))


@app.route("/duplicate/<int:course_id>", methods=["GET", "POST"])
def duplicate_course(course_id):
    """Carrega formulário de duplicação ou processa a criação do curso duplicado"""
    try:
        if request.method == "POST":
            # Validar CSRF token
            csrf.protect()

            # Processar criação do curso duplicado
            logger.info(f"Processando duplicação do curso {course_id}")
            logger.info(f"Dados recebidos: {dict(request.form)}")

            # Log específico para campos críticos
            logger.info("=== DEBUG DUPLICAÇÃO ===")
            logger.info(f"modalidade: {request.form.get('modalidade')}")
            logger.info(f"aulas_assincronas: {request.form.get('aulas_assincronas')}")
            logger.info(f"horario_inicio[]: {request.form.getlist('horario_inicio[]')}")
            logger.info(f"horario_fim[]: {request.form.getlist('horario_fim[]')}")
            logger.info(
                f"endereco_unidade[]: {request.form.getlist('endereco_unidade[]')}"
            )
            logger.info(f"vagas_unidade[]: {request.form.getlist('vagas_unidade[]')}")

            # Log de dias da semana para debug
            logger.info("=== DIAS DA SEMANA ===")
            # Verificar todos os campos que começam com dias_aula
            for key in request.form.keys():
                if "dias_aula" in key:
                    logger.info(f"{key}: {request.form.getlist(key)}")
            logger.info("========================")

            # Usar o serviço de cursos para criar o curso duplicado
            success, course_data, messages = course_service.create_course(
                request.form, request.files
            )

            if success:
                logger.info(f"Curso duplicado com sucesso: ID {course_data['id']}")

                # Exibir avisos se houver
                for warning in messages:
                    flash(warning, "warning")

                flash("Curso duplicado com sucesso!", "success")
                return redirect(url_for("course_success", course_id=course_data["id"]))
            else:
                # Exibir erros de validação e manter na página de duplicação
                logger.warning(f"Falha na duplicação do curso: {messages}")
                for error in messages:
                    flash(error, "error")
                    logger.warning(f"Erro de validação: {error}")

                # Buscar dados originais do curso para duplicação
                original_course_data = course_service.get_course(course_id)
                if original_course_data:
                    # Preparar dados para duplicação
                    original_course_data = _prepare_course_for_edit_form(
                        original_course_data
                    )
                    duplicate_data = original_course_data.copy()

                    # Limpar campos que não devem ser copiados
                    fields_to_clear = [
                        "id",
                        "created_at",
                        "csv_file",
                        "pdf_file",
                        "capa_curso",
                    ]
                    for field in fields_to_clear:
                        duplicate_data[field] = ""

                    # Sobrescrever com dados do formulário para preservar o que o usuário digitou
                    for key, value in request.form.items():
                        if key.endswith("[]"):
                            duplicate_data[key.replace("[]", "")] = (
                                request.form.getlist(key)
                            )
                        else:
                            duplicate_data[key] = value

                    # Preparar título para duplicação se não foi alterado pelo usuário
                    if (
                        not duplicate_data.get("titulo")
                        or duplicate_data.get("titulo")
                        == f"Cópia de {original_course_data.get('titulo', '')}"
                    ):
                        original_title = original_course_data.get("titulo", "")
                        if original_title:
                            duplicate_data["titulo_original"] = (
                                f"Cópia de {original_title}"
                            )
                            duplicate_data["titulo"] = f"Cópia de {original_title}"
                            duplicate_data["descricao_original"] = (
                                original_course_data.get("descricao", "")
                            )

                        # Renderizar formulário com dados preservados e mensagens de erro
                        today_date = datetime.now().strftime("%Y-%m-%d")
                        # Preencher datas padrão se estiverem vazias para evitar envio de valores nulos
                        if not duplicate_data.get("inicio_inscricoes_data"):
                            duplicate_data["inicio_inscricoes_data"] = today_date
                        if not duplicate_data.get("fim_inscricoes_data"):
                            from datetime import timedelta

                            duplicate_data["fim_inscricoes_data"] = (
                                datetime.now() + timedelta(days=30)
                            ).strftime("%Y-%m-%d")

                        return render_template(
                            "course_duplicate.html",
                            orgaos=ORGAOS,
                            duplicate_data=duplicate_data,
                            original_course_id=course_id,
                            today_date=today_date,
                        )

                # Se não conseguir buscar dados originais, redirecionar
                return redirect(url_for("duplicate_course", course_id=course_id))

        # GET - Carregar formulário de duplicação
        # Buscar o curso a ser duplicado
        course_data = course_service.get_course(course_id)
        if not course_data:
            flash("Curso não encontrado para duplicação", "error")
            return redirect(url_for("public_courses"))

        # Preparar dados igual ao formulário de edição
        course_data = _prepare_course_for_edit_form(course_data)

        # Preparar dados para duplicação
        duplicate_data = course_data.copy()

        # Limpar campos que não devem ser copiados na duplicação
        fields_to_clear = ["id", "created_at", "csv_file", "pdf_file", "capa_curso"]

        for field in fields_to_clear:
            duplicate_data[field] = ""

        # Preparar título para duplicação
        original_title = course_data.get("titulo", "")
        if original_title:
            duplicate_data["titulo_original"] = f"Cópia de {original_title}"
            duplicate_data["titulo"] = (
                f"Cópia de {original_title}"  # Para preencher o campo
            )
            duplicate_data["descricao_original"] = course_data.get(
                "descricao", ""
            )  # Para exibir na interface

        # CORREÇÃO: Converter datas de volta para formato HTML (YYYY-MM-DD) para o input type="date"
        # O _prepare_course_for_edit_form converte para DD/MM/YYYY, mas o template precisa de YYYY-MM-DD
        if duplicate_data.get("inicio_inscricoes_data"):
            duplicate_data["inicio_inscricoes_data"] = _convert_date_to_html_format(
                duplicate_data["inicio_inscricoes_data"]
            )
        if duplicate_data.get("fim_inscricoes_data"):
            duplicate_data["fim_inscricoes_data"] = _convert_date_to_html_format(
                duplicate_data["fim_inscricoes_data"]
            )

        # Preencher datas padrão se estiverem vazias para evitar envio de valores nulos
        today_date = datetime.now().strftime("%Y-%m-%d")
        if not duplicate_data.get("inicio_inscricoes_data"):
            duplicate_data["inicio_inscricoes_data"] = today_date
        if not duplicate_data.get("fim_inscricoes_data"):
            from datetime import timedelta

            duplicate_data["fim_inscricoes_data"] = (
                datetime.now() + timedelta(days=30)
            ).strftime("%Y-%m-%d")

        # Renderizar formulário com dados pré-preenchidos
        return render_template(
            "course_duplicate.html",
            orgaos=ORGAOS,
            duplicate_data=duplicate_data,
            original_course_id=course_id,
            today_date=today_date,
        )
    except Exception as e:
        logger.error(f"Erro ao duplicar curso {course_id}: {str(e)}")
        flash("Erro ao carregar dados para duplicação", "error")
        return redirect(url_for("public_courses"))


# -----------------------------
# Rotas de autenticação admin
# -----------------------------


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Login administrativo com proteção CSRF e autenticação via banco de dados"""
    form = LoginForm()

    if form.validate_on_submit():
        email = form.username.data  # Campo username agora aceita email
        password = form.password.data

        # Usar o serviço de autenticação (agora retorna 3 valores)
        success, error_message, user_data = auth_service.authenticate_admin(
            email, password
        )

        if success and user_data:
            session["logged_in"] = True
            session["user_id"] = user_data["id"]
            session["user_email"] = user_data["email"]
            flash("Login realizado com sucesso!", "success")

            # Redirecionar para a página solicitada ou dashboard
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("admin_dashboard"))
        else:
            flash(error_message or "Credenciais inválidas", "error")

    return render_template("admin_login.html", form=form)


@app.route("/admin/logout")
def admin_logout():
    """Logout do usuário administrativo"""
    session.pop("logged_in", None)
    session.pop("user_id", None)
    session.pop("user_email", None)
    flash("Logout realizado com sucesso.", "info")
    return redirect(url_for("index"))


@app.route("/admin")
@login_required
def admin_dashboard():
    """Dashboard administrativo"""
    try:
        # Usar o serviço para listar cursos
        courses = course_service.list_courses()

        # Obter status dos cursos inseridos
        inserted_courses = course_status_service.get_inserted_courses()

        # Adicionar status aos cursos
        for course in courses:
            # Converter ID do curso para int para comparação correta
            course_id = course.get("id")
            if isinstance(course_id, str) and course_id.isdigit():
                course_id = int(course_id)
            course["is_inserted"] = course_id in inserted_courses

        return render_template(
            "course_list.html", courses=courses, inserted_courses=inserted_courses
        )
    except Exception as e:
        logger.error(f"Erro no dashboard admin: {str(e)}")
        import traceback

        logger.error(f"Traceback completo: {traceback.format_exc()}")
        flash("Erro ao carregar dashboard", "error")
        return redirect(url_for("index"))


# -----------------------------
# Fim da seção de autenticação admin
# -----------------------------


@app.route("/edit_course/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    """Editar um curso existente"""
    try:
        course = course_service.get_course(course_id)
        if not course:
            flash("Curso não encontrado", "error")
            return redirect(url_for("list_courses"))

        if request.method == "POST":
            # Validar CSRF token
            csrf.protect()

            # Usar o serviço para atualizar o curso
            success, updated_course, messages = course_service.update_course(
                course_id, request.form, request.files
            )

            if success:
                # Exibir avisos se houver
                for warning in messages:
                    flash(warning, "warning")

                flash("Curso atualizado com sucesso!", "success")
                return redirect(url_for("course_edit_success", course_id=course_id))
            else:
                # Exibir erros de validação e manter na página de edição
                for error in messages:
                    flash(error, "error")

                # Preparar dados do curso com os dados do formulário para preservar as alterações
                course = _prepare_course_for_edit_form(course)

                # Sobrescrever com dados do formulário para preservar o que o usuário digitou
                for key, value in request.form.items():
                    if key.endswith("[]"):
                        # Para campos de array, usar getlist
                        course[key.replace("[]", "")] = request.form.getlist(key)
                    else:
                        course[key] = value

                # Renderizar o formulário novamente com os dados preservados e mensagens de erro
                return render_template("course_edit.html", course=course, orgaos=ORGAOS)

        # Preparar dados para o formulário de edição
        course = _prepare_course_for_edit_form(course)
        return render_template("course_edit.html", course=course, orgaos=ORGAOS)

    except Exception as e:
        logger.error(f"Erro ao editar curso {course_id}: {str(e)}")
        flash(f"Erro ao editar curso: {str(e)}", "error")
        return redirect(url_for("list_courses"))


def _convert_date_to_html_format(date_string):
    """
    Converte data para formato HTML (YYYY-MM-DD) para input type="date"

    Args:
        date_string: Data em formato DD/MM/YYYY ou YYYY-MM-DD

    Returns:
        str: Data no formato YYYY-MM-DD
    """
    if not date_string:
        return ""

    # Se já está no formato correto (YYYY-MM-DD)
    import re

    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_string):
        return date_string

    # Se está no formato DD/MM/YYYY
    if "/" in date_string:
        try:
            parts = date_string.split("/")
            if len(parts) == 3:
                dia, mes, ano = parts
                return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
        except:
            pass

    # Se está no formato DD-MM-YYYY
    if "-" in date_string and len(date_string.split("-")[0]) <= 2:
        try:
            parts = date_string.split("-")
            if len(parts) == 3:
                dia, mes, ano = parts
                return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
        except:
            pass

    return date_string


def _prepare_course_for_edit_form(course):
    """Prepara dados do curso para o formulário de edição"""
    # Garantir que temos a descrição original para edição
    if not course.get("descricao_original") and course.get("descricao"):
        # Se não temos descricao_original, usar a descricao atual como original
        course["descricao_original"] = course["descricao"]

    # Converter datas para o formato HTML (YYYY-MM-DD)
    if "inicio_inscricoes" in course and course["inicio_inscricoes"]:
        try:
            # Se for um objeto datetime, converter diretamente
            if isinstance(course["inicio_inscricoes"], datetime):
                course["inicio_inscricoes_data"] = course["inicio_inscricoes"].strftime(
                    "%Y-%m-%d"
                )
            # Se for string, processar
            elif isinstance(course["inicio_inscricoes"], str):
                # Tentar primeiro com separador '-'
                if "-" in course["inicio_inscricoes"]:
                    parts = course["inicio_inscricoes"].split("-")
                # Tentar com separador '/' se não encontrar '-'
                else:
                    parts = course["inicio_inscricoes"].split("/")

                if len(parts) == 3:
                    # Se estiver no formato DD-MM-AAAA ou DD/MM/AAAA
                    if len(parts[2]) == 4:  # Ano tem 4 dígitos
                        course["inicio_inscricoes_data"] = (
                            f"{parts[2]}-{parts[1]}-{parts[0]}"
                        )
                    # Se estiver no formato AAAA-MM-DD ou AAAA/MM/DD
                    elif len(parts[0]) == 4:  # Ano tem 4 dígitos
                        course["inicio_inscricoes_data"] = (
                            f"{parts[0]}-{parts[1]}-{parts[2]}"
                        )
        except Exception as e:
            logger.warning(f"Erro ao converter data de início: {e}")
            course["inicio_inscricoes_data"] = ""
    else:
        course["inicio_inscricoes_data"] = ""

    if "fim_inscricoes" in course and course["fim_inscricoes"]:
        try:
            # Se for um objeto datetime, converter diretamente
            if isinstance(course["fim_inscricoes"], datetime):
                course["fim_inscricoes_data"] = course["fim_inscricoes"].strftime(
                    "%Y-%m-%d"
                )
            # Se for string, processar
            elif isinstance(course["fim_inscricoes"], str):
                # Tentar primeiro com separador '-'
                if "-" in course["fim_inscricoes"]:
                    parts = course["fim_inscricoes"].split("-")
                # Tentar com separador '/' se não encontrar '-'
                else:
                    parts = course["fim_inscricoes"].split("/")

                if len(parts) == 3:
                    # Se estiver no formato DD-MM-AAAA ou DD/MM/AAAA
                    if len(parts[2]) == 4:  # Ano tem 4 dígitos
                        course["fim_inscricoes_data"] = (
                            f"{parts[2]}-{parts[1]}-{parts[0]}"
                        )
                    # Se estiver no formato AAAA-MM-DD ou AAAA/MM/DD
                    elif len(parts[0]) == 4:  # Ano tem 4 dígitos
                        course["fim_inscricoes_data"] = (
                            f"{parts[0]}-{parts[1]}-{parts[2]}"
                        )
        except Exception as e:
            logger.warning(f"Erro ao converter data de fim: {e}")
            course["fim_inscricoes_data"] = ""
    else:
        course["fim_inscricoes_data"] = ""

    # Mapear campos de modalidade e unidades
    if (
        course.get("modalidade") == "Presencial"
        or course.get("modalidade") == "Híbrido"
    ):
        # Processar dados de múltiplas unidades separados por |
        # Verificar se é string antes de usar split
        endereco_val = course.get("endereco_unidade", "")
        enderecos = (
            endereco_val.split("|")
            if isinstance(endereco_val, str) and endereco_val
            else [""]
        )

        bairro_val = course.get("bairro_unidade", "")
        bairros = (
            bairro_val.split("|")
            if isinstance(bairro_val, str) and bairro_val
            else [""]
        )

        vagas_val = course.get("vagas_unidade", "")
        vagas = (
            vagas_val.split("|") if isinstance(vagas_val, str) and vagas_val else [""]
        )

        inicio_aulas_val = course.get("inicio_aulas_data", "")
        inicio_aulas_raw = (
            inicio_aulas_val.split("|")
            if isinstance(inicio_aulas_val, str) and inicio_aulas_val
            else [""]
        )
        # Limpar formato de data para remover hora se presente (YYYY-MM-DD HH:MM:SS -> YYYY-MM-DD)
        inicio_aulas = []
        for data in inicio_aulas_raw:
            if data and " " in data:
                # Remover parte do horário
                inicio_aulas.append(data.split(" ")[0])
            else:
                inicio_aulas.append(data)

        fim_aulas_val = course.get("fim_aulas_data", "")
        fim_aulas_raw = (
            fim_aulas_val.split("|")
            if isinstance(fim_aulas_val, str) and fim_aulas_val
            else [""]
        )
        # Limpar formato de data para remover hora se presente
        fim_aulas = []
        for data in fim_aulas_raw:
            if data and " " in data:
                # Remover parte do horário
                fim_aulas.append(data.split(" ")[0])
            else:
                fim_aulas.append(data)

        horario_inicio_val = course.get("horario_inicio", "")
        horario_inicio = (
            horario_inicio_val.split("|")
            if isinstance(horario_inicio_val, str) and horario_inicio_val
            else [""]
        )

        horario_fim_val = course.get("horario_fim", "")
        horario_fim = (
            horario_fim_val.split("|")
            if isinstance(horario_fim_val, str) and horario_fim_val
            else [""]
        )

        dias_aula_val = course.get("dias_aula", "")
        dias_aula = (
            dias_aula_val.split("|")
            if isinstance(dias_aula_val, str) and dias_aula_val
            else [""]
        )

        # Campos de unidade presencial (primeira unidade para compatibilidade)
        course["endereco_unidade"] = enderecos[0] if enderecos else ""
        course["bairro_unidade"] = bairros[0] if bairros else ""
        course["vagas_unidade"] = vagas[0] if vagas else ""
        course["inicio_aulas_data"] = inicio_aulas[0] if inicio_aulas else ""
        course["fim_aulas_data"] = fim_aulas[0] if fim_aulas else ""
        course["horario_inicio"] = horario_inicio[0] if horario_inicio else ""
        course["horario_fim"] = horario_fim[0] if horario_fim else ""
        course["dias_aula"] = dias_aula[0] if dias_aula else ""

        # Arrays para múltiplas unidades
        course["enderecos_unidades"] = enderecos
        course["bairros_unidades"] = bairros
        course["vagas_unidades"] = vagas
        course["inicio_aulas_unidades"] = inicio_aulas
        course["fim_aulas_unidades"] = fim_aulas
        course["horario_inicio_unidades"] = horario_inicio
        course["horario_fim_unidades"] = horario_fim
        course["dias_aula_unidades"] = dias_aula
    elif course.get("modalidade") == "Online":
        # Campos de plataforma online
        course["plataforma_digital"] = course.get("plataforma_digital", "")
        course["aulas_assincronas"] = course.get("aulas_assincronas", "sim")
        course["vagas_online"] = course.get("vagas_unidade", "")
        course["inicio_aulas_online"] = course.get("inicio_aulas_data", "")
        course["fim_aulas_online"] = course.get("fim_aulas_data", "")
        course["horario_inicio_online"] = course.get("horario_inicio", "")
        course["horario_fim_online"] = course.get("horario_fim", "")

    # Mapear campos de valores e certificado
    course["curso_gratuito"] = course.get("curso_gratuito", "sim")
    course["valor_curso_inteira"] = course.get("valor_curso_inteira", "")
    course["valor_curso_meia"] = course.get("valor_curso_meia", "")
    course["requisitos_meia"] = course.get("requisitos_meia", "")
    course["oferece_certificado"] = course.get("oferece_certificado", "nao")
    course["pre_requisitos"] = course.get("pre_requisitos", "")

    # Mapear campos de bolsa
    course["oferece_bolsa"] = course.get("oferece_bolsa", "nao")
    course["valor_bolsa"] = course.get("valor_bolsa", "")
    course["requisitos_bolsa"] = course.get("requisitos_bolsa", "")

    # Mapear campos de acessibilidade
    course["acessibilidade"] = course.get("acessibilidade", "nao_acessivel")
    course["recursos_acessibilidade"] = course.get("recursos_acessibilidade", "")

    # Mapear campos de parceiro externo
    course["parceiro_externo"] = course.get("parceiro_externo", "nao")
    course["parceiro_nome"] = course.get("parceiro_nome", "")
    course["parceiro_link"] = course.get("parceiro_link", "")
    course["parceiro_logo"] = course.get("parceiro_logo", "")

    # Mapear informações adicionais
    course["info_adicionais_opcao"] = "nao"  # Padrão para não mostrar campo adicional
    if course.get("info_complementares") and course.get("info_complementares").strip():
        course["info_adicionais_opcao"] = "sim"

    return course


@app.route("/course_edit_success/<int:course_id>")
@login_required
def course_edit_success(course_id):
    """Exibir página de sucesso após edição do curso"""
    try:
        course = course_service.get_course(course_id)
        if not course:
            flash("Curso não encontrado", "error")
            return redirect(url_for("list_courses"))
        return render_template("course_edit_success.html", course=course)
    except Exception as e:
        logger.error(f"Erro ao carregar curso editado {course_id}: {str(e)}")
        flash("Erro ao carregar curso", "error")
        return redirect(url_for("list_courses"))


@app.route("/delete_course/<int:course_id>", methods=["POST"])
@login_required
def delete_course(course_id):
    """Excluir um curso existente e seus arquivos com proteção CSRF"""
    form = DeleteCourseForm()

    if form.validate_on_submit():
        try:
            success, message = course_service.delete_course(course_id)

            if success:
                flash(message, "success")
            else:
                flash(message, "error")

        except Exception as e:
            logger.error(f"Erro ao excluir curso {course_id}: {str(e)}")
            flash(f"Erro ao excluir curso: {str(e)}", "error")
    else:
        flash("Erro de validação CSRF. Tente novamente.", "error")

    return redirect(url_for("list_courses"))


@app.route("/course_status/<int:course_id>", methods=["POST"])
@login_required
def toggle_course_status(course_id):
    """Marcar/desmarcar curso como inserido com proteção CSRF"""
    form = CourseStatusForm()

    if form.validate_on_submit():
        try:
            action = form.action.data

            if action == "mark_inserted":
                success = course_status_service.mark_as_inserted(course_id)
                if success:
                    flash("Curso marcado como inserido!", "success")
                else:
                    flash("Erro ao marcar curso como inserido", "error")
            elif action == "unmark_inserted":
                success = course_status_service.unmark_as_inserted(course_id)
                if success:
                    flash("Curso desmarcado como inserido!", "success")
                else:
                    flash("Erro ao desmarcar curso", "error")
            else:
                flash("Ação inválida", "error")

        except Exception as e:
            logger.error(f"Erro ao alterar status do curso {course_id}: {str(e)}")
            flash(f"Erro ao alterar status: {str(e)}", "error")
    else:
        flash("Erro de validação CSRF. Tente novamente.", "error")

    return redirect(url_for("list_courses"))


@app.route("/download/<filename>")
@login_required
def download_file(filename):
    """Rota para download de arquivos CSV e PDF"""
    try:
        if filename.endswith(".csv"):
            directory = Config.CSV_DIR
        elif filename.endswith(".pdf"):
            directory = Config.PDF_DIR
        else:
            flash("Tipo de arquivo não suportado", "error")
            return redirect(url_for("index"))

        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Erro ao baixar arquivo {filename}: {str(e)}")
        flash(f"Erro ao baixar arquivo: {str(e)}", "error")
        return redirect(url_for("index"))


# -----------------------------
# Seção de APIs removida - usando rotas com proteção CSRF


@app.route("/test-icons")
def test_icons():
    """Página de teste para verificar se os ícones Font Awesome estão funcionando"""
    return render_template("test_icons.html")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🎓 WebApp v4 - Ciclo Carioca (CicloCarioca.pythonanywhere.com)")
    print("📋 Formulário de Criação de Cursos")
    print("🌐 Rodando em modo de produção")
    print("=" * 50 + "\n")

    # Configuração para desenvolvimento local
    app.run(debug=False, host="0.0.0.0", port=5001)

# Configuração para CicloCarioca.pythonanywhere.com
# Esta aplicação será importada pelo arquivo WSGI
application = app


# Middleware para verificar se estamos no PythonAnywhere (sem limpar flash messages)
@app.before_request
def check_pythonanywhere():
    """Verificar se estamos no CicloCarioca.pythonanywhere.com"""
    if request.host and "pythonanywhere" in request.host:
        # Apenas log para debug - NÃO limpar flash messages
        logger.info(f"Acessando via PythonAnywhere: {request.host}")
        # Removido: session.pop('_flashes', None) - estava impedindo exibição de erros
