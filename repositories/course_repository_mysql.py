"""
Repositório para gerenciamento de cursos no banco de dados MySQL.
Responsável por todas as operações de persistência relacionadas a cursos.
"""

import pymysql
import logging
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class CourseRepositoryMySQL:
    """Repositório para operações de cursos no banco de dados MySQL"""
    
    def __init__(self):
        """Inicializa o repositório com configurações do banco"""
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'cursoscarioca'),
            'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
            'cursorclass': pymysql.cursors.DictCursor
        }
    
    def _get_connection(self):
        """Cria e retorna uma conexão com o banco de dados"""
        try:
            connection = pymysql.connect(**self.db_config)
            return connection
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao banco de dados: {e}")
            raise
    
    def create_course(self, course_data: Dict[str, Any], user_id: int) -> Optional[int]:
        """
        Cria um novo curso no banco de dados
        
        Args:
            course_data: Dados do curso
            user_id: ID do usuário que está criando o curso
            
        Returns:
            ID do curso criado ou None em caso de erro
        """
        connection = None
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                # Inserir dados na tabela cursos
                sql = """
                    INSERT INTO cursos (
                        tipo_acao, titulo, titulo_original, descricao, descricao_original,
                        capa_curso, inicio_inscricoes, fim_inscricoes, orgao, tema,
                        carga_horaria, modalidade, acessibilidade, recursos_acessibilidade,
                        publico_alvo, curso_gratuito, valor_curso_inteira, valor_curso_meia,
                        requisitos_meia, oferece_certificado, pre_requisitos, oferece_bolsa,
                        valor_bolsa, requisitos_bolsa, info_complementares, info_adicionais,
                        parceiro_externo, parceiro_nome, parceiro_link, parceiro_logo,
                        status, created_by, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, NOW(), NOW()
                    )
                """
                
                values = (
                    course_data.get('tipo_acao', 'Curso'),
                    course_data.get('titulo'),
                    course_data.get('titulo_original'),
                    course_data.get('descricao'),
                    course_data.get('descricao_original'),
                    course_data.get('capa_curso'),
                    course_data.get('inicio_inscricoes'),
                    course_data.get('fim_inscricoes'),
                    course_data.get('orgao'),
                    course_data.get('tema'),
                    course_data.get('carga_horaria'),
                    course_data.get('modalidade'),
                    course_data.get('acessibilidade', 'nao_acessivel'),
                    course_data.get('recursos_acessibilidade'),
                    course_data.get('publico_alvo'),
                    course_data.get('curso_gratuito', 'sim'),
                    course_data.get('valor_curso_inteira'),
                    course_data.get('valor_curso_meia'),
                    course_data.get('requisitos_meia'),
                    course_data.get('oferece_certificado', 'nao'),
                    course_data.get('pre_requisitos'),
                    course_data.get('oferece_bolsa', 'nao'),
                    course_data.get('valor_bolsa'),
                    course_data.get('requisitos_bolsa'),
                    course_data.get('info_complementares'),
                    course_data.get('info_adicionais'),
                    course_data.get('parceiro_externo', 'nao'),
                    course_data.get('parceiro_nome'),
                    course_data.get('parceiro_link'),
                    course_data.get('parceiro_logo'),
                    course_data.get('status', 'ativo'),
                    user_id
                )
                
                cursor.execute(sql, values)
                course_id = cursor.lastrowid
                
                # Inserir turmas presenciais se modalidade for Presencial ou Híbrido
                if course_data.get('modalidade') in ['Presencial', 'Híbrido']:
                    self._insert_turmas(cursor, course_id, course_data)
                
                # Inserir plataforma online se modalidade for Online ou Híbrido
                if course_data.get('modalidade') in ['Online', 'Híbrido']:
                    self._insert_plataforma_online(cursor, course_id, course_data)
                
                connection.commit()
                logger.info(f"✅ Curso criado com sucesso: ID {course_id}")
                return course_id
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar curso: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if connection:
                connection.close()
    
    def _insert_turmas(self, cursor, course_id: int, course_data: Dict[str, Any]):
        """
        Insere turmas presenciais para um curso
        
        Args:
            cursor: Cursor do banco de dados
            course_id: ID do curso
            course_data: Dados do curso contendo arrays de turmas
        """
        # Obter arrays de dados das turmas
        enderecos = course_data.get('enderecos_unidades', [])
        bairros = course_data.get('bairros_unidades', [])
        complementos = course_data.get('complementos_unidades', [])
        vagas = course_data.get('vagas_unidades', [])
        inicio_aulas = course_data.get('inicio_aulas_unidades', [])
        fim_aulas = course_data.get('fim_aulas_unidades', [])
        horario_inicio = course_data.get('horario_inicio_unidades', [])
        horario_fim = course_data.get('horario_fim_unidades', [])
        dias_aula = course_data.get('dias_aula_unidades', [])
        
        # Inserir cada turma
        for i in range(len(enderecos)):
            sql_turma = """
                INSERT INTO turmas (
                    curso_id, numero_turma, endereco_unidade, bairro_unidade,
                    complemento, vagas_totais, vagas_ocupadas, inicio_aulas,
                    fim_aulas, horario_inicio, horario_fim, status,
                    created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, 0, %s, %s, %s, %s, 'ativa', NOW(), NOW()
                )
            """
            
            values_turma = (
                course_id,
                i + 1,  # numero_turma sequencial
                enderecos[i] if i < len(enderecos) else None,
                bairros[i] if i < len(bairros) else None,
                complementos[i] if i < len(complementos) else None,
                int(vagas[i]) if i < len(vagas) and vagas[i] else 0,
                inicio_aulas[i] if i < len(inicio_aulas) else None,
                fim_aulas[i] if i < len(fim_aulas) else None,
                horario_inicio[i] if i < len(horario_inicio) else None,
                horario_fim[i] if i < len(horario_fim) else None
            )
            
            cursor.execute(sql_turma, values_turma)
            turma_id = cursor.lastrowid
            
            # Inserir dias da semana para esta turma
            if i < len(dias_aula) and dias_aula[i]:
                try:
                    dias_list = dias_aula[i].split(',') if isinstance(dias_aula[i], str) else dias_aula[i]
                    for dia in dias_list:
                        dia = dia.strip()
                        if dia:
                            sql_dia = """
                                INSERT INTO turmas_dias_semana (turma_id, dia_semana)
                                VALUES (%s, %s)
                            """
                            try:
                                cursor.execute(sql_dia, (turma_id, dia))
                            except Exception as e:
                                # Logar valor problemático e re-raise para o rollback
                                logger.error(f"❌ Erro ao inserir dia '{dia}' para turma {turma_id}: {e}")
                                raise
                except Exception:
                    logger.error(f"❌ Formato inválido para dias_da_turma index={i}: {dias_aula[i]}")
                    raise
            
            logger.info(f"✅ Turma {i+1} criada para curso {course_id}")
    
    def _insert_plataforma_online(self, cursor, course_id: int, course_data: Dict[str, Any]):
        """
        Insere plataforma online para um curso
        
        Args:
            cursor: Cursor do banco de dados
            course_id: ID do curso
            course_data: Dados do curso contendo informações da plataforma
        """
        sql_plataforma = """
            INSERT INTO plataformas_online (
                curso_id, plataforma_digital, link_acesso, vagas_totais,
                vagas_ocupadas, aulas_assincronas, inicio_aulas, fim_aulas,
                horario_inicio, horario_fim, status, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, 0, %s, %s, %s, %s, %s, 'ativa', NOW(), NOW()
            )
        """
        
        aulas_assincronas = course_data.get('aulas_assincronas', 'sim')
        
        values_plataforma = (
            course_id,
            course_data.get('plataforma_digital'),
            course_data.get('link_acesso'),
            int(course_data.get('vagas_online', 0)) if course_data.get('vagas_online') else 0,
            aulas_assincronas,
            course_data.get('inicio_aulas_online') if aulas_assincronas == 'nao' else None,
            course_data.get('fim_aulas_online') if aulas_assincronas == 'nao' else None,
            course_data.get('horario_inicio_online') if aulas_assincronas == 'nao' else None,
            course_data.get('horario_fim_online') if aulas_assincronas == 'nao' else None
        )
        
        cursor.execute(sql_plataforma, values_plataforma)
        plataforma_id = cursor.lastrowid
        
        # TODO: Inserir dias da semana se aulas síncronas
        # Tabela plataformas_dias_semana não existe ainda no banco
        # if aulas_assincronas == 'nao' and course_data.get('dias_aula_online'):
        #     dias_list = course_data.get('dias_aula_online', [])
        #     if isinstance(dias_list, str):
        #         dias_list = dias_list.split(',')
        #     
        #     for dia in dias_list:
        #         dia = dia.strip()
        #         if dia:
        #             sql_dia = """
        #                 INSERT INTO plataformas_dias_semana (plataforma_id, dia_semana)
        #                 VALUES (%s, %s)
        #             """
        #             cursor.execute(sql_dia, (plataforma_id, dia))
        
        logger.info(f"✅ Plataforma online criada para curso {course_id}")
    
    def find_by_id(self, course_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca um curso pelo ID com todas as suas turmas e plataformas
        
        Args:
            course_id: ID do curso
            
        Returns:
            Dicionário com dados do curso ou None se não encontrado
        """
        connection = None
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                # Buscar dados do curso
                sql = "SELECT * FROM cursos WHERE id = %s"
                cursor.execute(sql, (course_id,))
                course = cursor.fetchone()
                
                if not course:
                    return None
                
                # Buscar turmas presenciais
                course['turmas'] = self._get_turmas_by_course_id(cursor, course_id)
                
                # Buscar plataforma online
                course['plataforma_online'] = self._get_plataforma_by_course_id(cursor, course_id)
                
                return course
                
        except Exception as e:
            logger.error(f"❌ Erro ao buscar curso {course_id}: {e}")
            return None
        finally:
            if connection:
                connection.close()
    
    def update_course(self, course_id: int, course_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Atualiza um curso existente no banco de dados
        
        Args:
            course_id: ID do curso
            course_data: Novos dados do curso
            
        Returns:
            Dicionário com dados do curso atualizado ou None em caso de erro
        """
        connection = None
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                # Construir SQL UPDATE dinamicamente baseado nos campos fornecidos
                fields_to_update = []
                values = []
                
                # Campos que podem ser atualizados
                updateable_fields = [
                    'tipo_acao', 'titulo', 'titulo_original', 'descricao', 'descricao_original',
                    'capa_curso', 'inicio_inscricoes', 'fim_inscricoes', 'orgao', 'tema',
                    'carga_horaria', 'modalidade', 'acessibilidade', 'recursos_acessibilidade',
                    'publico_alvo', 'curso_gratuito', 'valor_curso_inteira', 'valor_curso_meia',
                    'requisitos_meia', 'oferece_certificado', 'pre_requisitos', 'oferece_bolsa',
                    'valor_bolsa', 'requisitos_bolsa', 'info_complementares', 'info_adicionais',
                    'parceiro_externo', 'parceiro_nome', 'parceiro_link', 'parceiro_logo', 'status'
                ]
                
                # Montar lista de campos a atualizar
                decimal_fields = ['valor_curso_inteira', 'valor_curso_meia', 'valor_bolsa', 'carga_horaria']
                
                for field in updateable_fields:
                    if field in course_data:
                        fields_to_update.append(f"{field} = %s")
                        value = course_data.get(field)
                        
                        # Normalizar valores vazios para None em campos decimais
                        if field in decimal_fields and (value == '' or value == 'None'):
                            value = None
                        
                        values.append(value)
                
                if not fields_to_update:
                    logger.warning(f"⚠️ Nenhum campo para atualizar no curso {course_id}")
                    return self.find_by_id(course_id)
                
                # Adicionar updated_at e course_id
                fields_to_update.append("updated_at = NOW()")
                values.append(course_id)
                
                sql = f"UPDATE cursos SET {', '.join(fields_to_update)} WHERE id = %s"
                cursor.execute(sql, values)
                
                if cursor.rowcount == 0:
                    logger.warning(f"⚠️ Nenhum curso encontrado com ID {course_id}")
                    return None
                
                connection.commit()
                logger.info(f"✅ Curso {course_id} atualizado com sucesso")
                
                # Se houver dados de turmas, atualizar turmas também
                if 'enderecos_unidades' in course_data and course_data.get('enderecos_unidades'):
                    # Deletar turmas antigas
                    sql_delete_dias = "DELETE FROM turmas_dias_semana WHERE turma_id IN (SELECT id FROM turmas WHERE curso_id = %s)"
                    cursor.execute(sql_delete_dias, (course_id,))
                    
                    sql_delete_turmas = "DELETE FROM turmas WHERE curso_id = %s"
                    cursor.execute(sql_delete_turmas, (course_id,))
                    
                    connection.commit()
                    logger.info(f"✅ Turmas antigas do curso {course_id} deletadas")
                    
                    # Inserir novas turmas
                    self._insert_turmas(cursor, course_id, course_data)
                    connection.commit()
                    logger.info(f"✅ Novas turmas do curso {course_id} inseridas")
                
                # Retornar curso atualizado
                return self.find_by_id(course_id)
                
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar curso {course_id}: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if connection:
                connection.close()
    
    def _get_turmas_by_course_id(self, cursor, course_id: int) -> List[Dict[str, Any]]:
        """Busca todas as turmas de um curso"""
        sql = "SELECT * FROM turmas WHERE curso_id = %s ORDER BY numero_turma"
        cursor.execute(sql, (course_id,))
        turmas = cursor.fetchall()
        
        # Para cada turma, buscar dias da semana
        for turma in turmas:
            sql_dias = "SELECT dia_semana FROM turmas_dias_semana WHERE turma_id = %s"
            cursor.execute(sql_dias, (turma['id'],))
            dias = cursor.fetchall()
            turma['dias_semana'] = [dia['dia_semana'] for dia in dias]
        
        return turmas
    
    def _get_plataforma_by_course_id(self, cursor, course_id: int) -> Optional[Dict[str, Any]]:
        """Busca a plataforma online de um curso"""
        sql = "SELECT * FROM plataformas_online WHERE curso_id = %s"
        cursor.execute(sql, (course_id,))
        plataforma = cursor.fetchone()
        
        if plataforma:
            # TODO: Buscar dias da semana quando tabela existir
            # Tabela plataformas_dias_semana não existe ainda no banco
            # sql_dias = "SELECT dia_semana FROM plataformas_dias_semana WHERE plataforma_id = %s"
            # cursor.execute(sql_dias, (plataforma['id'],))
            # dias = cursor.fetchall()
            # plataforma['dias_semana'] = [dia['dia_semana'] for dia in dias]
            plataforma['dias_semana'] = []  # Temporário até criar a tabela
        
        return plataforma
    
    def find_all(self):
        """
        Lista todos os cursos
        
        Returns:
            Lista de cursos
        """
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM cursos 
                    WHERE status = 'ativo'
                    ORDER BY created_at DESC
                """)
                courses = cursor.fetchall()
                
                logger.info(f"✅ {len(courses)} cursos encontrados")
                return courses
                
        except Exception as e:
            logger.error(f"❌ Erro ao listar cursos: {str(e)}")
            return []
        finally:
            if connection:
                connection.close()
    
    def delete_course(self, course_id: int) -> bool:
        """
        Exclui um curso do banco de dados
        
        Args:
            course_id: ID do curso a ser excluído
            
        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        connection = None
        try:
            logger.info(f"🔍 Iniciando exclusão do curso {course_id}")
            connection = self._get_connection()
            logger.info(f"✅ Conexão estabelecida")
            
            with connection.cursor() as cursor:
                # Verificar se o curso existe
                logger.info(f"🔍 Verificando se curso {course_id} existe...")
                cursor.execute("SELECT id FROM cursos WHERE id = %s", (course_id,))
                if not cursor.fetchone():
                    logger.warning(f"⚠️ Curso {course_id} não encontrado")
                    return False
                
                logger.info(f"✅ Curso {course_id} encontrado, executando DELETE...")
                
                # Deletar o curso (CASCADE irá deletar turmas, dias_semana e plataformas automaticamente)
                cursor.execute("DELETE FROM cursos WHERE id = %s", (course_id,))
                rows_affected = cursor.rowcount
                logger.info(f"📊 Linhas afetadas pelo DELETE: {rows_affected}")
                
                logger.info(f"💾 Executando COMMIT...")
                connection.commit()
                logger.info(f"✅ COMMIT executado com sucesso")
                
                logger.info(f"✅ Curso {course_id} excluído com sucesso do banco de dados")
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro ao excluir curso {course_id}: {str(e)}")
            logger.error(f"❌ Tipo do erro: {type(e).__name__}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            if connection:
                logger.info("🔄 Executando ROLLBACK...")
                connection.rollback()
            return False
        finally:
            if connection:
                logger.info("🔌 Fechando conexão")
                connection.close()
    
    def mark_as_inserted(self, course_id: int) -> bool:
        """
        Marca um curso como inserido no sistema
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se marcado com sucesso
        """
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE cursos SET is_inserted = 'sim' WHERE id = %s",
                    (course_id,)
                )
                connection.commit()
                
                if cursor.rowcount > 0:
                    logger.info(f"✅ Curso {course_id} marcado como inserido")
                    return True
                else:
                    logger.warning(f"⚠️ Curso {course_id} não encontrado")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Erro ao marcar curso {course_id} como inserido: {str(e)}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection:
                connection.close()
    
    def unmark_as_inserted(self, course_id: int) -> bool:
        """
        Desmarca um curso como inserido no sistema
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se desmarcado com sucesso
        """
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE cursos SET is_inserted = 'nao' WHERE id = %s",
                    (course_id,)
                )
                connection.commit()
                
                if cursor.rowcount > 0:
                    logger.info(f"✅ Curso {course_id} desmarcado como inserido")
                    return True
                else:
                    logger.warning(f"⚠️ Curso {course_id} não encontrado")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Erro ao desmarcar curso {course_id}: {str(e)}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection:
                connection.close()
    
    def is_course_inserted(self, course_id: int) -> bool:
        """
        Verifica se um curso está marcado como inserido
        
        Args:
            course_id: ID do curso
            
        Returns:
            bool: True se o curso está marcado como inserido
        """
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT is_inserted FROM cursos WHERE id = %s",
                    (course_id,)
                )
                result = cursor.fetchone()
                
                if result:
                    return result['is_inserted'] == 'sim'
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao verificar status do curso {course_id}: {str(e)}")
            return False
        finally:
            if connection:
                connection.close()
    
    def get_inserted_courses(self) -> set:
        """
        Retorna o conjunto de IDs dos cursos marcados como inseridos
        
        Returns:
            set: Conjunto de IDs dos cursos inseridos
        """
        try:
            connection = self._get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM cursos WHERE is_inserted = 'sim'"
                )
                results = cursor.fetchall()
                
                return {row['id'] for row in results}
                
        except Exception as e:
            logger.error(f"❌ Erro ao buscar cursos inseridos: {str(e)}")
            return set()
        finally:
            if connection:
                connection.close()

