# services/course_service.py
# Serviço de negócio para cursos

from typing import Dict, List, Optional, Tuple
from repositories.course_repository import CourseRepository
from repositories.course_repository_mysql import CourseRepositoryMySQL
from services.validation_service import CourseValidator, ValidationError
from services.ai_service import AIService
from services.file_service import FileService
from flask import session
import logging

logger = logging.getLogger(__name__)


class CourseService:
    """Serviço de negócio para operações com cursos"""

    def __init__(self):
        # Usar repositório MySQL como principal
        self.repository_mysql = CourseRepositoryMySQL()
        # Manter repositório CSV/PDF para backup
        self.repository_csv = CourseRepository()
        self.validator = CourseValidator()
        self.ai_service = AIService()
        self.file_service = FileService()

    def create_course(
        self, form_data: Dict, files: Dict = None, user_id: int = None
    ) -> Tuple[bool, Dict, List[str]]:
        """
        Cria um novo curso

        Args:
            form_data: Dados do formulário
            files: Arquivos enviados (logos, etc.)

        Returns:
            Tuple[bool, Dict, List[str]]: (sucesso, dados_curso, erros)
        """
        try:
            # CORREÇÃO: Limpar campos inválidos baseado na modalidade antes da validação
            form_data = self._clean_form_data_by_modality(form_data)

            # Validar dados
            is_valid, errors, warnings = self.validator.validate_course_data(form_data)
            if not is_valid:
                return False, {}, errors

            # Processar dados do formulário para MySQL
            course_data = self._process_form_data_for_mysql(form_data)

            # Processar arquivos se fornecidos
            if files:
                self._process_uploaded_files(course_data, files)

            # Melhorar descrição com IA
            course_data = self._enhance_description(course_data)

            # Obter user_id da sessão ou usar valor fornecido (útil para testes)
            if user_id is None:
                user_id = session.get(
                    "user_id", 1
                )  # Default para 1 se não houver sessão

            # Salvar curso no MySQL
            course_id = self.repository_mysql.create_course(course_data, user_id)

            if not course_id:
                return False, {}, ["Erro ao salvar curso no banco de dados"]

            # Buscar curso completo criado
            saved_course = self.repository_mysql.find_by_id(course_id)

            # Também salvar em CSV/PDF para backup (opcional)
            try:
                course_data_csv = self._prepare_course_for_csv(saved_course)
                csv_pdf_data = self.repository_csv.save_course(course_data_csv)

                # Atualizar os nomes dos arquivos no banco MySQL
                if csv_pdf_data.get("csv_file") or csv_pdf_data.get("pdf_file"):
                    self.repository_mysql.update_course_files(
                        course_id,
                        csv_pdf_data.get("csv_file"),
                        csv_pdf_data.get("pdf_file"),
                    )
                    saved_course = self.repository_mysql.find_by_id(course_id)

                logger.info(f"✅ Backup CSV/PDF criado para curso {course_id}")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao criar backup CSV/PDF: {e}")
                warnings.append("Curso salvo, mas backup CSV/PDF falhou")

            return True, saved_course, warnings

        except Exception as e:
            logger.error(f"❌ Erro ao criar curso: {e}")
            import traceback

            logger.error(traceback.format_exc())
            return False, {}, [f"Erro interno: {str(e)}"]

    def update_course(
        self, course_id: int, form_data: Dict, files: Dict = None
    ) -> Tuple[bool, Dict, List[str]]:
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
            existing_course = self.repository_mysql.find_by_id(course_id)
            if not existing_course:
                return False, {}, ["Curso não encontrado"]

            # CORREÇÃO: Limpar campos inválidos baseado na modalidade antes da validação
            form_data = self._clean_form_data_by_modality(form_data)

            # Validar dados
            is_valid, errors, warnings = self.validator.validate_course_data(form_data)
            if not is_valid:
                return False, {}, errors

            # Para edição, usar processamento MySQL para obter dados de turmas estruturados
            course_data = self._process_form_data_for_mysql(form_data)

            # Processar arquivos se fornecidos
            if files:
                self._process_uploaded_files(course_data, files)
            else:
                # Manter arquivos existentes
                course_data["parceiro_logo"] = existing_course.get("parceiro_logo", "")

            # NOVA FUNCIONALIDADE: Na edição, não alterar a descrição já processada pelo Gemini
            # Manter sempre a descrição original e a processada pelo Gemini separadamente
            course_data["descricao"] = existing_course.get(
                "descricao", course_data.get("descricao_original")
            )

            # Atualizar curso
            updated_course = self.repository_mysql.update_course(course_id, course_data)

            return True, updated_course, warnings

        except Exception as e:
            return False, {}, [f"Erro interno: {str(e)}"]

    def get_course(self, course_id: int) -> Optional[Dict]:
        """Busca um curso pelo ID e formata para template"""
        # Tentar buscar no MySQL primeiro
        course = self.repository_mysql.find_by_id(course_id)
        if course:
            # Formatar para template
            return self._format_course_for_template(course)

        # Fallback para CSV se não encontrar no MySQL
        logger.warning(f"Curso {course_id} não encontrado no MySQL, tentando CSV")
        return self.repository_csv.find_by_id(course_id)

    def list_courses(
        self, search_query: str = None, modality: str = None, orgao: str = None
    ) -> List[Dict]:
        """
        Lista cursos com filtros opcionais

        Args:
            search_query: Texto de busca
            modality: Modalidade do curso
            orgao: Órgão responsável

        Returns:
            List[Dict]: Lista de cursos filtrados e formatados para os templates
        """
        # Usar MySQL como fonte principal
        courses = self.repository_mysql.find_all()

        # Formatar cursos para o formato esperado pelos templates
        formatted_courses = []
        for course in courses:
            formatted_course = self._format_course_for_template(course)
            formatted_courses.append(formatted_course)

        # Aplicar filtros se necessário
        if search_query:
            query_lower = search_query.lower()
            formatted_courses = [
                c
                for c in formatted_courses
                if query_lower in str(c.get("titulo", "")).lower()
                or query_lower in str(c.get("descricao", "")).lower()
                or query_lower in str(c.get("tema", "")).lower()
            ]

        if modality:
            formatted_courses = [
                c for c in formatted_courses if c.get("modalidade") == modality
            ]

        if orgao:
            formatted_courses = [
                c for c in formatted_courses if c.get("orgao") == orgao
            ]

        return formatted_courses

    def _normalize_mysql_types(self, data: Dict) -> Dict:
        """
        Normaliza tipos de dados do MySQL para tipos esperados pelos templates
        Converte datetime, Decimal, timedelta, etc. para strings
        """
        from decimal import Decimal

        normalized = {}
        for key, value in data.items():
            if value is None:
                normalized[key] = ""
            elif isinstance(value, Decimal):
                # Converter Decimal para string formatada
                normalized[key] = str(value)
            elif hasattr(value, "strftime"):
                # datetime ou date objects
                if hasattr(value, "hour"):
                    # datetime com hora
                    normalized[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    # apenas date
                    normalized[key] = value.strftime("%Y-%m-%d")
            elif hasattr(value, "total_seconds"):
                # timedelta object
                total_seconds = int(value.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                normalized[key] = f"{hours:02d}:{minutes:02d}"
            else:
                normalized[key] = value

        return normalized

    def _format_course_for_template(self, course: Dict) -> Dict:
        """
        Formata dados do curso do MySQL para o formato esperado pelos templates

        Args:
            course: Dados do curso do MySQL

        Returns:
            Dict: Curso formatado para template
        """
        try:
            # Buscar curso completo com turmas e plataforma
            course_id = course.get("id")
            logger.info(f"🔄 Formatando curso {course_id} para template")
            full_course = self.repository_mysql.find_by_id(course_id)

            if not full_course:
                logger.warning(f"⚠️ Curso {course_id} não encontrado ao formatar")
                return course

            # Normalizar tipos do MySQL para tipos esperados pelos templates
            full_course = self._normalize_mysql_types(full_course)

            # Formatar datas para exibição (DD/MM/YYYY)
            if full_course.get("inicio_inscricoes"):
                logger.info(
                    f"📅 Convertendo inicio_inscricoes: {full_course['inicio_inscricoes']}"
                )
                full_course["inicio_inscricoes"] = self._convert_date_from_mysql(
                    full_course["inicio_inscricoes"]
                )
            if full_course.get("fim_inscricoes"):
                logger.info(
                    f"📅 Convertendo fim_inscricoes: {full_course['fim_inscricoes']}"
                )
                full_course["fim_inscricoes"] = self._convert_date_from_mysql(
                    full_course["fim_inscricoes"]
                )
        except Exception as e:
            logger.error(f"❌ Erro ao formatar curso {course.get('id')}: {e}")
            logger.error(f"Tipo de erro: {type(e).__name__}")
            import traceback

            logger.error(traceback.format_exc())

            # Em caso de erro, normalizar tipos e garantir campos básicos
            full_course = self._normalize_mysql_types(course.copy())

            # Garantir que campos pipe-separated existam como strings vazias
            for field in [
                "endereco_unidade",
                "bairro_unidade",
                "vagas_unidade",
                "inicio_aulas_data",
                "fim_aulas_data",
                "horario_inicio",
                "horario_fim",
                "dias_aula",
            ]:
                if field not in full_course or full_course[field] is None:
                    full_course[field] = ""
                elif not isinstance(full_course[field], str):
                    full_course[field] = str(full_course[field])

            return full_course

        try:
            # Processar turmas presenciais
            if full_course.get("turmas"):
                turmas = full_course["turmas"]

                # Normalizar tipos de cada turma
                turmas = [self._normalize_mysql_types(t) for t in turmas]

                # Criar strings pipe-separated para compatibilidade com templates antigos
                full_course["endereco_unidade"] = "|".join(
                    [t.get("endereco_unidade", "") or "" for t in turmas]
                )
                full_course["bairro_unidade"] = "|".join(
                    [t.get("bairro_unidade", "") or "" for t in turmas]
                )
                full_course["vagas_unidade"] = "|".join(
                    [str(t.get("vagas_totais", 0)) for t in turmas]
                )

                # Converter datas de objetos datetime para strings
                inicio_aulas_list = []
                fim_aulas_list = []
                for t in turmas:
                    if t.get("inicio_aulas"):
                        # Converter datetime.date para string YYYY-MM-DD
                        inicio_date = t["inicio_aulas"]
                        if hasattr(inicio_date, "strftime"):
                            inicio_aulas_list.append(inicio_date.strftime("%Y-%m-%d"))
                        else:
                            inicio_aulas_list.append(str(inicio_date))

                    if t.get("fim_aulas"):
                        # Converter datetime.date para string YYYY-MM-DD
                        fim_date = t["fim_aulas"]
                        if hasattr(fim_date, "strftime"):
                            fim_aulas_list.append(fim_date.strftime("%Y-%m-%d"))
                        else:
                            fim_aulas_list.append(str(fim_date))

                full_course["inicio_aulas_data"] = "|".join(inicio_aulas_list)
                full_course["fim_aulas_data"] = "|".join(fim_aulas_list)

                # Converter horários de objetos timedelta para strings
                horario_inicio_list = []
                horario_fim_list = []
                for t in turmas:
                    if t.get("horario_inicio"):
                        horario = t["horario_inicio"]
                        if hasattr(horario, "strftime"):
                            horario_inicio_list.append(horario.strftime("%H:%M"))
                        elif isinstance(horario, str):
                            horario_inicio_list.append(horario)
                        else:
                            # timedelta object
                            total_seconds = int(horario.total_seconds())
                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            horario_inicio_list.append(f"{hours:02d}:{minutes:02d}")

                    if t.get("horario_fim"):
                        horario = t["horario_fim"]
                        if hasattr(horario, "strftime"):
                            horario_fim_list.append(horario.strftime("%H:%M"))
                        elif isinstance(horario, str):
                            horario_fim_list.append(horario)
                        else:
                            # timedelta object
                            total_seconds = int(horario.total_seconds())
                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            horario_fim_list.append(f"{hours:02d}:{minutes:02d}")

                full_course["horario_inicio"] = "|".join(horario_inicio_list)
                full_course["horario_fim"] = "|".join(horario_fim_list)

                # Dias da semana
                dias_list = []
                for turma in turmas:
                    if turma.get("dias_semana"):
                        dias_list.append(",".join(turma["dias_semana"]))
                full_course["dias_aula"] = "|".join(dias_list)

            # Processar plataforma online
            if full_course.get("plataforma_online"):
                plataforma = self._normalize_mysql_types(
                    full_course["plataforma_online"]
                )
                full_course["plataforma_digital"] = plataforma.get(
                    "plataforma_digital", ""
                )
                full_course["link_acesso"] = plataforma.get("link_acesso", "")
                full_course["aulas_assincronas"] = plataforma.get(
                    "aulas_assincronas", "sim"
                )

                if plataforma.get("dias_semana"):
                    full_course["dias_aula_online"] = ",".join(
                        plataforma["dias_semana"]
                    )

        except Exception as e:
            logger.error(
                f"❌ Erro ao processar turmas/plataforma do curso {course_id}: {e}"
            )
            logger.error(f"Tipo de erro: {type(e).__name__}")
            import traceback

            logger.error(traceback.format_exc())

            # Garantir que campos pipe-separated existam como strings vazias
            for field in [
                "endereco_unidade",
                "bairro_unidade",
                "vagas_unidade",
                "inicio_aulas_data",
                "fim_aulas_data",
                "horario_inicio",
                "horario_fim",
                "dias_aula",
            ]:
                if field not in full_course or full_course[field] is None:
                    full_course[field] = ""
                elif not isinstance(full_course[field], str):
                    full_course[field] = str(full_course[field])

        return full_course

    def delete_course(self, course_id: int) -> Tuple[bool, str]:
        """
        Exclui um curso

        Args:
            course_id: ID do curso

        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            success = self.repository_mysql.delete_course(course_id)
            if success:
                return True, "Curso excluído com sucesso"
            else:
                return False, "Curso não encontrado"
        except Exception as e:
            return False, f"Erro ao excluir curso: {str(e)}"

    def _clean_form_data_by_modality(self, form_data):
        """
        Limpa campos do formulário que não são aplicáveis à modalidade selecionada

        Args:
            form_data: Dados do formulário (ImmutableMultiDict ou dict)

        Returns:
            MultiDict limpo com apenas campos relevantes
        """
        from werkzeug.datastructures import MultiDict

        modalidade = form_data.get("modalidade", "")

        # Criar novo MultiDict para armazenar dados limpos
        cleaned_data = MultiDict()

        # Copiar todos os dados primeiro
        if hasattr(form_data, "items"):
            for key in form_data.keys():
                values = (
                    form_data.getlist(key)
                    if hasattr(form_data, "getlist")
                    else [form_data.get(key)]
                )
                for value in values:
                    cleaned_data.add(key, value)

        # Campos a limpar baseado na modalidade
        if modalidade == "Online":
            # Para cursos online, limpar campos presenciais
            campos_presenciais = [
                "endereco_unidade[]",
                "bairro_unidade[]",
                "complemento[]",
            ]

            for campo in campos_presenciais:
                if campo in cleaned_data:
                    # Remover valores não vazios desses campos
                    valores = cleaned_data.getlist(campo)
                    cleaned_data.setlist(campo, [""] * len(valores) if valores else [])
                    logger.info(
                        f"🧹 Limpando campo presencial para curso online: {campo}"
                    )

        elif modalidade in ["Presencial", "Híbrido"]:
            # Para cursos presenciais/híbridos, limpar campos online específicos
            # (mas manter alguns campos que podem ser usados em híbrido)
            pass  # Não limpar nada por enquanto para presencial/híbrido

        return cleaned_data

    def _process_form_data_for_mysql(self, form_data: Dict) -> Dict:
        """Processa dados do formulário para salvar no MySQL"""
        modalidade = form_data.get("modalidade", "")

        # Dados básicos do curso
        course_data = {
            "tipo_acao": form_data.get("tipo_acao", "Curso").strip(),
            "titulo": form_data.get("titulo", "").strip(),
            "descricao_original": form_data.get("descricao", "").strip(),
            "titulo_original": form_data.get("titulo", "").strip(),  # Para histórico
            "inicio_inscricoes": self._convert_date_to_mysql(
                form_data.get("inicio_inscricoes_data")
            ),
            "fim_inscricoes": self._convert_date_to_mysql(
                form_data.get("fim_inscricoes_data")
            ),
            "orgao": form_data.get("orgao", ""),
            "tema": form_data.get("tema", ""),
            "carga_horaria": form_data.get("carga_horaria", ""),
            "modalidade": modalidade,
            "publico_alvo": form_data.get("publico_alvo", ""),
            "acessibilidade": form_data.get("acessibilidade", "nao_acessivel"),
            "recursos_acessibilidade": form_data.get("recursos_acessibilidade", "")
            if form_data.get("acessibilidade") in ["acessivel", "exclusivo"]
            else "",
            "curso_gratuito": form_data.get("curso_gratuito", "sim"),
            "valor_curso_inteira": form_data.get("valor_curso_inteira")
            if form_data.get("curso_gratuito") == "nao"
            else None,
            "valor_curso_meia": form_data.get("valor_curso_meia")
            if form_data.get("curso_gratuito") == "nao"
            else None,
            "requisitos_meia": form_data.get("requisitos_meia")
            if form_data.get("curso_gratuito") == "nao"
            else "",
            "oferece_certificado": form_data.get("oferece_certificado", "nao"),
            "pre_requisitos": form_data.get("pre_requisitos")
            if form_data.get("oferece_certificado") == "sim"
            else "",
            "oferece_bolsa": form_data.get("oferece_bolsa", "nao"),
            "valor_bolsa": form_data.get("valor_bolsa")
            if form_data.get("oferece_bolsa") == "sim"
            else None,
            "requisitos_bolsa": form_data.get("requisitos_bolsa")
            if form_data.get("oferece_bolsa") == "sim"
            else "",
            "info_complementares": form_data.get("info_complementares", ""),
            "info_adicionais": form_data.get("info_adicionais_opcao", "nao"),
            "parceiro_externo": form_data.get("parceiro_externo", "nao"),
            "parceiro_nome": form_data.get("parceiro_nome")
            if form_data.get("parceiro_externo") == "sim"
            else "",
            "parceiro_link": form_data.get("parceiro_link")
            if form_data.get("parceiro_externo") == "sim"
            else "",
            "parceiro_logo": "",
            "capa_curso": "",
        }

        # Processar dados específicos por modalidade
        if modalidade in ["Presencial", "Híbrido"]:
            # Arrays de turmas presenciais
            course_data["enderecos_unidades"] = (
                form_data.getlist("endereco_unidade[]")
                if hasattr(form_data, "getlist")
                else []
            )
            course_data["bairros_unidades"] = (
                form_data.getlist("bairro_unidade[]")
                if hasattr(form_data, "getlist")
                else []
            )
            course_data["complementos_unidades"] = (
                form_data.getlist("complemento[]")
                if hasattr(form_data, "getlist")
                else []
            )
            course_data["vagas_unidades"] = (
                form_data.getlist("vagas_unidade[]")
                if hasattr(form_data, "getlist")
                else []
            )
            course_data["inicio_aulas_unidades"] = (
                [
                    self._convert_date_to_mysql(d)
                    for d in form_data.getlist("inicio_aulas_data[]")
                ]
                if hasattr(form_data, "getlist")
                else []
            )
            course_data["fim_aulas_unidades"] = (
                [
                    self._convert_date_to_mysql(d)
                    for d in form_data.getlist("fim_aulas_data[]")
                ]
                if hasattr(form_data, "getlist")
                else []
            )
            course_data["horario_inicio_unidades"] = (
                form_data.getlist("horario_inicio[]")
                if hasattr(form_data, "getlist")
                else []
            )
            course_data["horario_fim_unidades"] = (
                form_data.getlist("horario_fim[]")
                if hasattr(form_data, "getlist")
                else []
            )

            # Dias da semana por turma
            dias_aula_list = []
            num_turmas = len(course_data["enderecos_unidades"])

            logger.info(f"📅 Processando dias da semana para {num_turmas} turmas")

            if hasattr(form_data, "getlist"):
                # Tentar obter dias específicos por turma (dias_aula_presencial_0[], dias_aula_presencial_1[], etc)
                dias_por_turma = []
                for i in range(num_turmas):
                    dias_especificos = form_data.getlist(f"dias_aula_presencial_{i}[]")
                    logger.info(
                        f"  Turma {i}: dias_aula_presencial_{i}[] = {dias_especificos}"
                    )
                    if dias_especificos:
                        dias_por_turma.append(
                            ",".join([str(d) for d in dias_especificos if d])
                        )
                    else:
                        dias_por_turma.append("")

                # Se conseguimos dias específicos por turma, usar isso
                if any(dias_por_turma):
                    dias_aula_list = dias_por_turma
                    logger.info(
                        f"✅ Usando dias específicos por turma: {dias_aula_list}"
                    )
                else:
                    # Fallback: tentar obter dias genéricos (todos os checkboxes com nome dias_aula_presencial[])
                    dias_presencial = form_data.getlist("dias_aula_presencial[]")
                    logger.info(f"⚠️ Fallback para dias genéricos: {dias_presencial}")

                    if not dias_presencial:
                        dias_aula_list = ["" for _ in range(num_turmas)]
                        logger.warning(
                            f"❌ Nenhum dia encontrado! Lista vazia para {num_turmas} turmas"
                        )
                    else:
                        # Aplicar os mesmos dias a todas as turmas (comportamento padrão)
                        joined = ",".join([str(x) for x in dias_presencial if x])
                        dias_aula_list = [joined for _ in range(num_turmas)]
                        logger.info(
                            f"✅ Aplicando mesmos dias a todas as turmas: {joined}"
                        )
            else:
                dias_aula_list = ["" for _ in range(num_turmas)]
                logger.warning(f"❌ form_data não tem getlist, lista vazia")

            course_data["dias_aula_unidades"] = dias_aula_list
            logger.info(f"📊 Resultado final dias_aula_unidades: {dias_aula_list}")

        if modalidade in ["Online", "Híbrido"]:
            # Dados da plataforma online
            course_data["plataforma_digital"] = form_data.get("plataforma_digital", "")
            course_data["link_acesso"] = form_data.get("link_acesso", "")
            course_data["vagas_online"] = form_data.get("vagas_online", 0)
            course_data["aulas_assincronas"] = form_data.get("aulas_assincronas", "sim")

            if course_data["aulas_assincronas"] == "nao":
                course_data["inicio_aulas_online"] = self._convert_date_to_mysql(
                    form_data.get("inicio_aulas_online")
                )
                course_data["fim_aulas_online"] = self._convert_date_to_mysql(
                    form_data.get("fim_aulas_online")
                )
                course_data["horario_inicio_online"] = form_data.get(
                    "horario_inicio_online"
                )
                course_data["horario_fim_online"] = form_data.get("horario_fim_online")
                course_data["dias_aula_online"] = (
                    form_data.getlist("dias_aula_online[]")
                    if hasattr(form_data, "getlist")
                    else []
                )

        return course_data

    def _convert_date_to_mysql(self, date_string: str) -> Optional[str]:
        """Converte data para formato MySQL (YYYY-MM-DD)"""
        if not date_string:
            return None

        # Se já está no formato YYYY-MM-DD
        if "-" in date_string and len(date_string.split("-")[0]) == 4:
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

        return date_string

    def _prepare_course_for_csv(self, course_data: Dict) -> Dict:
        """Prepara dados do curso do MySQL para formato CSV/PDF"""
        # Converter de volta para formato esperado pelo gerador CSV/PDF
        csv_data = course_data.copy()

        # Converter datas de volta para formato DD/MM/YYYY
        if csv_data.get("inicio_inscricoes"):
            csv_data["inicio_inscricoes"] = self._convert_date_from_mysql(
                csv_data["inicio_inscricoes"]
            )
        if csv_data.get("fim_inscricoes"):
            csv_data["fim_inscricoes"] = self._convert_date_from_mysql(
                csv_data["fim_inscricoes"]
            )

        # Processar turmas para formato CSV (pipe-separated)
        if csv_data.get("turmas"):
            turmas = csv_data["turmas"]
            csv_data["endereco_unidade"] = "|".join(
                [t.get("endereco_unidade", "") for t in turmas]
            )
            csv_data["bairro_unidade"] = "|".join(
                [t.get("bairro_unidade", "") for t in turmas]
            )
            csv_data["vagas_unidade"] = "|".join(
                [str(t.get("vagas_totais", 0)) for t in turmas]
            )
            csv_data["inicio_aulas_data"] = "|".join(
                [
                    self._convert_date_from_mysql(t.get("inicio_aulas"))
                    for t in turmas
                    if t.get("inicio_aulas")
                ]
            )
            csv_data["fim_aulas_data"] = "|".join(
                [
                    self._convert_date_from_mysql(t.get("fim_aulas"))
                    for t in turmas
                    if t.get("fim_aulas")
                ]
            )
            csv_data["horario_inicio"] = "|".join(
                [str(t.get("horario_inicio", "")) for t in turmas]
            )
            csv_data["horario_fim"] = "|".join(
                [str(t.get("horario_fim", "")) for t in turmas]
            )
            csv_data["dias_aula"] = "|".join(
                [",".join(t.get("dias_semana", [])) for t in turmas]
            )

        return csv_data

    def _convert_date_from_mysql(self, date_obj) -> str:
        """Converte data do MySQL para formato DD/MM/YYYY"""
        if not date_obj:
            return ""

        # Se é objeto datetime, converter diretamente
        if hasattr(date_obj, "strftime"):
            try:
                return date_obj.strftime("%d/%m/%Y")
            except:
                pass

        # Se é string no formato YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS
        if isinstance(date_obj, str):
            try:
                # Remover horas se existir
                date_str = date_obj.split(" ")[0] if " " in date_obj else date_obj
                parts = date_str.split("-")
                if len(parts) == 3:
                    ano, mes, dia = parts
                    return f"{dia}/{mes}/{ano}"
            except:
                pass

        # Se não conseguiu converter, retornar original
        return str(date_obj)

    def _process_form_data(self, form_data: Dict) -> Dict:
        """Processa e transforma dados do formulário"""
        # Converter datas
        inicio_data = form_data.get("inicio_inscricoes_data")
        fim_data = form_data.get("fim_inscricoes_data")
        modalidade = form_data.get("modalidade", "")

        # Processar campos de array baseado na modalidade
        course_data = {
            "tipo_acao": form_data.get("tipo_acao", "").strip(),
            "titulo": form_data.get("titulo", "").strip(),
            "descricao_original": form_data.get("descricao", "").strip(),
            "inicio_inscricoes": f"{inicio_data.replace('-', '/')}"
            if inicio_data
            else "",
            "fim_inscricoes": f"{fim_data.replace('-', '/')}" if fim_data else "",
            "orgao": form_data.get("orgao", ""),
            "tema": form_data.get("tema", ""),
            "modalidade": modalidade,
        }

        # Campos específicos por modalidade
        if modalidade == "Online":
            # Verificar se aulas são síncronas (assíncronas = "não")
            aulas_assincronas = form_data.get("aulas_assincronas", "")
            aulas_sincronas = aulas_assincronas == "nao"

            # Campos específicos para Online
            course_data.update(
                {
                    "plataforma_digital": form_data.get("plataforma_digital", ""),
                    "carga_horaria": form_data.get("carga_horaria", ""),
                    "aulas_assincronas": aulas_assincronas,
                    "dias_aula": "|".join(
                        list(dict.fromkeys(form_data.getlist("dias_aula_online[]")))
                    )
                    if hasattr(form_data, "getlist")
                    else form_data.get("dias_aula_online[]", ""),
                    # Para cursos online, vagas_unidade deve vir do formulário
                    "vagas_unidade": "|".join(
                        [
                            v.strip()
                            for v in form_data.getlist("vagas_unidade[]")
                            if v.strip()
                        ]
                    )
                    if hasattr(form_data, "getlist")
                    else form_data.get("vagas_unidade[]", "").strip(),
                    # Campos de Presencial/Híbrido devem estar vazios para Online
                    "endereco_unidade": "",
                    "bairro_unidade": "",
                }
            )

            # Datas de aula baseadas no tipo de aula
            if aulas_sincronas:
                # Para aulas síncronas, incluir datas de início e fim
                course_data.update(
                    {
                        "inicio_aulas_data": "|".join(
                            [
                                d
                                for d in form_data.getlist("inicio_aulas_data[]")
                                if d.strip()
                            ]
                        )
                        if hasattr(form_data, "getlist")
                        else form_data.get("inicio_aulas_data[]", ""),
                        "fim_aulas_data": "|".join(
                            [
                                d
                                for d in form_data.getlist("fim_aulas_data[]")
                                if d.strip()
                            ]
                        )
                        if hasattr(form_data, "getlist")
                        else form_data.get("fim_aulas_data[]", ""),
                    }
                )
            else:
                # Para aulas assíncronas, datas devem estar vazias
                course_data.update({"inicio_aulas_data": "", "fim_aulas_data": ""})

            # Horários baseados no tipo de aula
            if aulas_sincronas:
                # Para aulas síncronas, incluir horários
                course_data.update(
                    {
                        "horario_inicio": "|".join(
                            [
                                h
                                for h in form_data.getlist("horario_inicio[]")
                                if h.strip()
                            ]
                        )
                        if hasattr(form_data, "getlist")
                        else form_data.get("horario_inicio[]", ""),
                        "horario_fim": "|".join(
                            [h for h in form_data.getlist("horario_fim[]") if h.strip()]
                        )
                        if hasattr(form_data, "getlist")
                        else form_data.get("horario_fim[]", ""),
                    }
                )
            else:
                # Para aulas assíncronas, horários devem estar vazios
                course_data.update({"horario_inicio": "", "horario_fim": ""})
        else:
            # Campos específicos para Presencial/Híbrido
            course_data.update(
                {
                    "endereco_unidade": "|".join(
                        form_data.getlist("endereco_unidade[]")
                    )
                    if hasattr(form_data, "getlist")
                    else form_data.get("endereco_unidade[]", ""),
                    "bairro_unidade": "|".join(form_data.getlist("bairro_unidade[]"))
                    if hasattr(form_data, "getlist")
                    else form_data.get("bairro_unidade[]", ""),
                    "vagas_unidade": "|".join(
                        [
                            v.strip()
                            for v in form_data.getlist("vagas_unidade[]")
                            if v.strip()
                        ]
                    )
                    if hasattr(form_data, "getlist")
                    else form_data.get("vagas_unidade[]", "").strip(),
                    "inicio_aulas_data": "|".join(
                        form_data.getlist("inicio_aulas_data[]")
                    )
                    if hasattr(form_data, "getlist")
                    else form_data.get("inicio_aulas_data[]", ""),
                    "fim_aulas_data": "|".join(form_data.getlist("fim_aulas_data[]"))
                    if hasattr(form_data, "getlist")
                    else form_data.get("fim_aulas_data[]", ""),
                    "horario_inicio": "|".join(
                        [h for h in form_data.getlist("horario_inicio[]") if h.strip()]
                    )
                    if hasattr(form_data, "getlist")
                    else form_data.get("horario_inicio[]", ""),
                    "horario_fim": "|".join(
                        [h for h in form_data.getlist("horario_fim[]") if h.strip()]
                    )
                    if hasattr(form_data, "getlist")
                    else form_data.get("horario_fim[]", ""),
                    "dias_aula": "|".join(
                        list(dict.fromkeys(form_data.getlist("dias_aula_presencial[]")))
                    )
                    if hasattr(form_data, "getlist")
                    else form_data.get("dias_aula_presencial[]", ""),
                    "carga_horaria": form_data.get("carga_horaria", ""),
                    # Campos de Online devem estar vazios para Presencial/Híbrido
                    "plataforma_digital": "",
                    "aulas_assincronas": "",
                }
            )

        # Campos comuns a todas as modalidades
        course_data.update(
            {
                "curso_gratuito": form_data.get("curso_gratuito", ""),
                "valor_curso": form_data.get("valor_curso")
                if form_data.get("curso_gratuito") == "nao"
                else "",
                "valor_curso_inteira": form_data.get("valor_curso_inteira")
                if form_data.get("curso_gratuito") == "nao"
                else "",
                "valor_curso_meia": form_data.get("valor_curso_meia")
                if form_data.get("curso_gratuito") == "nao"
                else "",
                "requisitos_meia": form_data.get("requisitos_meia")
                if form_data.get("curso_gratuito") == "nao"
                else "",
                "oferece_bolsa": form_data.get("oferece_bolsa", ""),
                "valor_bolsa": form_data.get("valor_bolsa")
                if form_data.get("oferece_bolsa") == "sim"
                else "",
                "requisitos_bolsa": form_data.get("requisitos_bolsa")
                if form_data.get("oferece_bolsa") == "sim"
                else "",
                "publico_alvo": form_data.get("publico_alvo", ""),
                "acessibilidade": form_data.get("acessibilidade", ""),
                "recursos_acessibilidade": form_data.get("recursos_acessibilidade")
                if form_data.get("acessibilidade") in ["acessivel", "exclusivo"]
                else "",
                "oferece_certificado": form_data.get("oferece_certificado", ""),
                "pre_requisitos": form_data.get("pre_requisitos")
                if form_data.get("oferece_certificado") == "sim"
                else "",
                "info_complementares": form_data.get("info_complementares", ""),
                "parceiro_externo": form_data.get("parceiro_externo", ""),
                "parceiro_nome": form_data.get("parceiro_nome")
                if form_data.get("parceiro_externo") == "sim"
                else "",
                "parceiro_link": form_data.get("parceiro_link")
                if form_data.get("parceiro_externo") == "sim"
                else "",
                "parceiro_logo": "",
                "capa_curso": "",
            }
        )

        return course_data

    def _process_uploaded_files(self, course_data: Dict, files: Dict):
        """Processa arquivos enviados"""
        # Processar logo do parceiro
        if course_data.get("parceiro_externo") == "sim":
            partner_name = course_data.get("parceiro_nome", "")
            logo_file = files.get("parceiro_logo")

            if logo_file and partner_name:
                logo_filename = self.file_service.save_partner_logo(
                    logo_file, partner_name
                )
                if logo_filename:
                    course_data["parceiro_logo"] = logo_filename

        # Processar capa do curso (com redimensionamento)
        cover_file = files.get("capa_curso")
        if cover_file:
            course_title = course_data.get("titulo", "")
            if course_title:
                # Salvar e redimensionar imagem
                cover_filename = self.file_service.save_course_cover(
                    cover_file, course_title
                )

                if cover_filename:
                    course_data["capa_curso"] = cover_filename
                    print(f"✅ Capa do curso salva: {cover_filename}")
                else:
                    print(f"❌ Erro ao salvar capa do curso")

    def _enhance_description(self, course_data: Dict) -> Dict:
        """Melhora a descrição usando IA"""
        try:
            original_description = course_data.get("descricao_original", "")
            if original_description:
                enhanced_description = self.ai_service.enhance_description(
                    original_description
                )
                course_data["descricao"] = enhanced_description
            else:
                course_data["descricao"] = original_description
        except Exception as e:
            print(f"Erro ao melhorar descrição: {str(e)}")
            course_data["descricao"] = course_data.get("descricao_original", "")

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
            return self.repository_mysql.find_by_id(course_id)
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
            "id",
            "titulo",
            "descricao_original",
            "descricao",
            "created_at",
            "csv_file",
            "pdf_file",
            "capa_curso",  # Logo pode ser mantido se quiserem
        ]

        # Criar cópia dos dados
        duplicate_data = course_data.copy()

        # Limpar campos que não devem ser copiados
        for field in fields_to_clear:
            duplicate_data[field] = ""

        # Adicionar prefixo ao título para indicar que é uma cópia
        original_title = course_data.get("titulo", "")
        if original_title:
            duplicate_data["titulo_original"] = f"Cópia de: {original_title}"

        # CORREÇÃO: Converter datas de inscrição para formato HTML (YYYY-MM-DD)
        if duplicate_data.get("inicio_inscricoes"):
            duplicate_data["inicio_inscricoes_data"] = (
                self._convert_date_to_html_format(duplicate_data["inicio_inscricoes"])
            )
        if duplicate_data.get("fim_inscricoes"):
            duplicate_data["fim_inscricoes_data"] = self._convert_date_to_html_format(
                duplicate_data["fim_inscricoes"]
            )

        # Processar dados de múltiplas unidades (igual ao template de edição)
        modalidade = duplicate_data.get("modalidade", "").lower()
        if modalidade == "presencial" or modalidade == "híbrido":
            # Processar dados de múltiplas unidades separados por |
            enderecos = (
                duplicate_data.get("endereco_unidade", "").split("|")
                if duplicate_data.get("endereco_unidade")
                else [""]
            )
            bairros = (
                duplicate_data.get("bairro_unidade", "").split("|")
                if duplicate_data.get("bairro_unidade")
                else [""]
            )
            vagas = (
                duplicate_data.get("vagas_unidade", "").split("|")
                if duplicate_data.get("vagas_unidade")
                else [""]
            )
            inicio_aulas = (
                duplicate_data.get("inicio_aulas_data", "").split("|")
                if duplicate_data.get("inicio_aulas_data")
                else [""]
            )
            fim_aulas = (
                duplicate_data.get("fim_aulas_data", "").split("|")
                if duplicate_data.get("fim_aulas_data")
                else [""]
            )
            horario_inicio = (
                duplicate_data.get("horario_inicio", "").split("|")
                if duplicate_data.get("horario_inicio")
                else [""]
            )
            horario_fim = (
                duplicate_data.get("horario_fim", "").split("|")
                if duplicate_data.get("horario_fim")
                else [""]
            )
            dias_aula = (
                duplicate_data.get("dias_aula", "").split("|")
                if duplicate_data.get("dias_aula")
                else [""]
            )

            # Arrays para múltiplas unidades (usado pelo template)
            duplicate_data["enderecos_unidades"] = enderecos
            duplicate_data["bairros_unidades"] = bairros
            duplicate_data["vagas_unidades"] = vagas
            duplicate_data["inicio_aulas_unidades"] = inicio_aulas
            duplicate_data["fim_aulas_unidades"] = fim_aulas
            duplicate_data["horario_inicio_unidades"] = horario_inicio
            duplicate_data["horario_fim_unidades"] = horario_fim
            duplicate_data["dias_aula_unidades"] = dias_aula

            # Converter datas para formato HTML (YYYY-MM-DD)
            inicio_aulas_converted = []
            fim_aulas_converted = []

            for data in inicio_aulas:
                if data:
                    converted = self._convert_date_to_html_format(data)
                    inicio_aulas_converted.append(converted)
                else:
                    inicio_aulas_converted.append("")

            for data in fim_aulas:
                if data:
                    converted = self._convert_date_to_html_format(data)
                    fim_aulas_converted.append(converted)
                else:
                    fim_aulas_converted.append("")

            # Atualizar arrays com datas convertidas
            duplicate_data["inicio_aulas_unidades"] = inicio_aulas_converted
            duplicate_data["fim_aulas_unidades"] = fim_aulas_converted

            print(f"🔄 Preparando {len(enderecos)} unidades para duplicação:")
            for i, endereco in enumerate(enderecos):
                print(
                    f"   Unidade {i + 1}: {endereco} - {bairros[i] if i < len(bairros) else ''}"
                )
                print(
                    f"      Início: {inicio_aulas_converted[i] if i < len(inicio_aulas_converted) else ''}"
                )
                print(
                    f"      Fim: {fim_aulas_converted[i] if i < len(fim_aulas_converted) else ''}"
                )

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
