#!/usr/bin/env python3
"""
Script de migração de dados CSV para MySQL
Migra todos os cursos dos arquivos CSV para o banco de dados MySQL
Autor: Sistema WebCiclo
Data: 2025-11-18
"""

import os
import sys
import csv
import pymysql
from datetime import datetime
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'cursoscarioca'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Diretório com os arquivos CSV
CSV_DIR = 'CSV'


def get_db_connection():
    """Cria conexão com o banco de dados"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        logger.info("✅ Conexão com banco de dados estabelecida")
        return connection
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao banco: {e}")
        raise


def convert_date_format(date_str):
    """
    Converte data de DD/MM/YYYY ou YYYY/MM/DD para YYYY-MM-DD
    """
    if not date_str or date_str.strip() == '':
        return None
    
    try:
        # Tentar formato YYYY/MM/DD
        if '/' in date_str and len(date_str.split('/')[0]) == 4:
            parts = date_str.split('/')
            return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
        
        # Tentar formato DD/MM/YYYY
        if '/' in date_str:
            parts = date_str.split('/')
            return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
        
        # Tentar formato YYYY-MM-DD (já está correto)
        if '-' in date_str and len(date_str.split('-')[0]) == 4:
            return date_str
        
        # Tentar formato DD-MM-YYYY
        if '-' in date_str:
            parts = date_str.split('-')
            return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
        
        return None
    except Exception as e:
        logger.warning(f"⚠️ Erro ao converter data '{date_str}': {e}")
        return None


def parse_csv_row(row):
    """
    Processa uma linha do CSV e retorna dados estruturados
    """
    # Dados básicos do curso
    course_data = {
        'tipo_acao': row.get('tipo_acao', 'Curso').strip(),
        'titulo': row.get('titulo', '').strip(),
        'titulo_original': row.get('titulo', '').strip(),
        'descricao': row.get('descricao', '').strip() or row.get('descricao_original', '').strip(),
        'descricao_original': row.get('descricao_original', '').strip(),
        'capa_curso': row.get('capa_curso', '').strip(),
        'inicio_inscricoes': convert_date_format(row.get('inicio_inscricoes', '')),
        'fim_inscricoes': convert_date_format(row.get('fim_inscricoes', '')),
        'orgao': row.get('orgao', '').strip(),
        'tema': row.get('tema', '').strip(),
        'carga_horaria': row.get('carga_horaria', '').strip(),
        'modalidade': row.get('modalidade', '').strip(),
        'acessibilidade': row.get('acessibilidade', 'nao_acessivel').strip(),
        'recursos_acessibilidade': row.get('recursos_acessibilidade', '').strip(),
        'publico_alvo': row.get('publico_alvo', '').strip(),
        'curso_gratuito': row.get('curso_gratuito', 'sim').strip(),
        'valor_curso_inteira': row.get('valor_curso_inteira', '').strip() or None,
        'valor_curso_meia': row.get('valor_curso_meia', '').strip() or None,
        'requisitos_meia': row.get('requisitos_meia', '').strip(),
        'oferece_certificado': row.get('oferece_certificado', 'nao').strip(),
        'pre_requisitos': row.get('pre_requisitos', '').strip(),
        'oferece_bolsa': row.get('oferece_bolsa', 'nao').strip(),
        'valor_bolsa': row.get('valor_bolsa', '').strip() or None,
        'requisitos_bolsa': row.get('requisitos_bolsa', '').strip(),
        'info_complementares': row.get('info_complementares', '').strip(),
        'info_adicionais': row.get('info_adicionais', '').strip(),
        'parceiro_externo': row.get('parceiro_externo', 'nao').strip(),
        'parceiro_nome': row.get('parceiro_nome', '').strip(),
        'parceiro_link': row.get('parceiro_link', '').strip(),
        'parceiro_logo': row.get('parceiro_logo', '').strip(),
        'status': 'ativo'
    }
    
    # Processar turmas presenciais (dados separados por |)
    turmas = []
    if course_data['modalidade'] in ['Presencial', 'Híbrido']:
        enderecos = row.get('endereco_unidade', '').split('|') if row.get('endereco_unidade') else []
        bairros = row.get('bairro_unidade', '').split('|') if row.get('bairro_unidade') else []
        vagas = row.get('vagas_unidade', '').split('|') if row.get('vagas_unidade') else []
        inicio_aulas = row.get('inicio_aulas_data', '').split('|') if row.get('inicio_aulas_data') else []
        fim_aulas = row.get('fim_aulas_data', '').split('|') if row.get('fim_aulas_data') else []
        horario_inicio = row.get('horario_inicio', '').split('|') if row.get('horario_inicio') else []
        horario_fim = row.get('horario_fim', '').split('|') if row.get('horario_fim') else []
        dias_aula = row.get('dias_aula', '').split('|') if row.get('dias_aula') else []
        
        max_turmas = max(len(enderecos), len(bairros), len(vagas))
        
        for i in range(max_turmas):
            turma = {
                'numero_turma': i + 1,
                'endereco_unidade': enderecos[i].strip() if i < len(enderecos) else '',
                'bairro_unidade': bairros[i].strip() if i < len(bairros) else '',
                'vagas_totais': int(vagas[i].strip()) if i < len(vagas) and vagas[i].strip().isdigit() else 0,
                'inicio_aulas': convert_date_format(inicio_aulas[i].strip()) if i < len(inicio_aulas) else None,
                'fim_aulas': convert_date_format(fim_aulas[i].strip()) if i < len(fim_aulas) else None,
                'horario_inicio': horario_inicio[i].strip() if i < len(horario_inicio) else None,
                'horario_fim': horario_fim[i].strip() if i < len(horario_fim) else None,
                'dias_semana': dias_aula[i].strip().split(',') if i < len(dias_aula) and dias_aula[i].strip() else []
            }
            turmas.append(turma)
    
    # Processar plataforma online
    plataforma_online = None
    if course_data['modalidade'] in ['Online', 'Híbrido']:
        plataforma_online = {
            'plataforma_digital': row.get('plataforma_digital', '').strip(),
            'link_acesso': row.get('link_acesso', '').strip(),
            'vagas_totais': 0,  # Pode ser ajustado se houver no CSV
            'aulas_assincronas': row.get('aulas_assincronas', 'sim').strip(),
            'inicio_aulas': None,
            'fim_aulas': None,
            'horario_inicio': None,
            'horario_fim': None
        }
    
    return course_data, turmas, plataforma_online


def insert_course(connection, course_data, turmas, plataforma_online, user_id=1):
    """
    Insere um curso no banco de dados com suas turmas e plataforma
    """
    try:
        with connection.cursor() as cursor:
            # Inserir curso
            sql_curso = """
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
            
            values_curso = (
                course_data['tipo_acao'],
                course_data['titulo'],
                course_data['titulo_original'],
                course_data['descricao'],
                course_data['descricao_original'],
                course_data['capa_curso'],
                course_data['inicio_inscricoes'],
                course_data['fim_inscricoes'],
                course_data['orgao'],
                course_data['tema'],
                course_data['carga_horaria'],
                course_data['modalidade'],
                course_data['acessibilidade'],
                course_data['recursos_acessibilidade'],
                course_data['publico_alvo'],
                course_data['curso_gratuito'],
                course_data['valor_curso_inteira'],
                course_data['valor_curso_meia'],
                course_data['requisitos_meia'],
                course_data['oferece_certificado'],
                course_data['pre_requisitos'],
                course_data['oferece_bolsa'],
                course_data['valor_bolsa'],
                course_data['requisitos_bolsa'],
                course_data['info_complementares'],
                course_data['info_adicionais'],
                course_data['parceiro_externo'],
                course_data['parceiro_nome'],
                course_data['parceiro_link'],
                course_data['parceiro_logo'],
                course_data['status'],
                user_id
            )
            
            cursor.execute(sql_curso, values_curso)
            course_id = cursor.lastrowid
            
            # Inserir turmas
            for turma in turmas:
                sql_turma = """
                    INSERT INTO turmas (
                        curso_id, numero_turma, endereco_unidade, bairro_unidade,
                        vagas_totais, vagas_ocupadas, inicio_aulas, fim_aulas,
                        horario_inicio, horario_fim, status, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, 0, %s, %s, %s, %s, 'ativa', NOW(), NOW()
                    )
                """
                
                cursor.execute(sql_turma, (
                    course_id,
                    turma['numero_turma'],
                    turma['endereco_unidade'],
                    turma['bairro_unidade'],
                    turma['vagas_totais'],
                    turma['inicio_aulas'],
                    turma['fim_aulas'],
                    turma['horario_inicio'],
                    turma['horario_fim']
                ))
                
                turma_id = cursor.lastrowid
                
                # Inserir dias da semana
                for dia in turma['dias_semana']:
                    dia = dia.strip()
                    if dia:
                        sql_dia = """
                            INSERT INTO turmas_dias_semana (turma_id, dia_semana)
                            VALUES (%s, %s)
                        """
                        cursor.execute(sql_dia, (turma_id, dia))
            
            # Inserir plataforma online
            if plataforma_online:
                sql_plataforma = """
                    INSERT INTO plataformas_online (
                        curso_id, plataforma_digital, link_acesso, vagas_totais,
                        vagas_ocupadas, aulas_assincronas, inicio_aulas, fim_aulas,
                        horario_inicio, horario_fim, status, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, 0, %s, %s, %s, %s, %s, 'ativa', NOW(), NOW()
                    )
                """
                
                cursor.execute(sql_plataforma, (
                    course_id,
                    plataforma_online['plataforma_digital'],
                    plataforma_online['link_acesso'],
                    plataforma_online['vagas_totais'],
                    plataforma_online['aulas_assincronas'],
                    plataforma_online['inicio_aulas'],
                    plataforma_online['fim_aulas'],
                    plataforma_online['horario_inicio'],
                    plataforma_online['horario_fim']
                ))
            
            connection.commit()
            return course_id
            
    except Exception as e:
        connection.rollback()
        logger.error(f"❌ Erro ao inserir curso: {e}")
        raise


def migrate_csv_files():
    """
    Migra todos os arquivos CSV para o banco de dados
    """
    logger.info("=" * 80)
    logger.info("🚀 INICIANDO MIGRAÇÃO CSV → MySQL")
    logger.info("=" * 80)
    
    # Verificar se diretório CSV existe
    if not os.path.exists(CSV_DIR):
        logger.error(f"❌ Diretório '{CSV_DIR}' não encontrado!")
        return False
    
    # Listar arquivos CSV
    csv_files = [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]
    
    if not csv_files:
        logger.warning(f"⚠️ Nenhum arquivo CSV encontrado em '{CSV_DIR}'")
        return False
    
    logger.info(f"📁 Encontrados {len(csv_files)} arquivos CSV")
    logger.info("-" * 80)
    
    # Conectar ao banco
    connection = get_db_connection()
    
    # Estatísticas
    total_migrated = 0
    total_errors = 0
    
    try:
        for csv_file in sorted(csv_files):
            csv_path = os.path.join(CSV_DIR, csv_file)
            logger.info(f"📄 Processando: {csv_file}")
            
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    
                    for row in reader:
                        try:
                            # Processar dados
                            course_data, turmas, plataforma_online = parse_csv_row(row)
                            
                            # Inserir no banco
                            course_id = insert_course(connection, course_data, turmas, plataforma_online)
                            
                            total_migrated += 1
                            logger.info(f"   ✅ Curso '{course_data['titulo']}' migrado (ID: {course_id})")
                            
                        except Exception as e:
                            total_errors += 1
                            logger.error(f"   ❌ Erro ao processar linha: {e}")
                            continue
                
            except Exception as e:
                logger.error(f"   ❌ Erro ao ler arquivo {csv_file}: {e}")
                total_errors += 1
                continue
        
        logger.info("-" * 80)
        logger.info("📊 ESTATÍSTICAS DA MIGRAÇÃO")
        logger.info(f"   • Cursos migrados: {total_migrated}")
        logger.info(f"   • Erros: {total_errors}")
        logger.info(f"   • Taxa de sucesso: {(total_migrated / (total_migrated + total_errors) * 100):.1f}%")
        logger.info("=" * 80)
        
        return True
        
    finally:
        connection.close()
        logger.info("🔌 Conexão com banco de dados fechada")


def verify_migration():
    """
    Verifica se a migração foi bem-sucedida
    """
    logger.info("")
    logger.info("=" * 80)
    logger.info("🔍 VERIFICANDO DADOS MIGRADOS")
    logger.info("=" * 80)
    
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # Contar cursos
            cursor.execute("SELECT COUNT(*) as total FROM cursos")
            total_cursos = cursor.fetchone()['total']
            logger.info(f"📚 Total de cursos: {total_cursos}")
            
            # Contar turmas
            cursor.execute("SELECT COUNT(*) as total FROM turmas")
            total_turmas = cursor.fetchone()['total']
            logger.info(f"🏫 Total de turmas: {total_turmas}")
            
            # Contar plataformas online
            cursor.execute("SELECT COUNT(*) as total FROM plataformas_online")
            total_plataformas = cursor.fetchone()['total']
            logger.info(f"💻 Total de plataformas online: {total_plataformas}")
            
            # Listar alguns cursos
            logger.info("")
            logger.info("📋 Primeiros 5 cursos migrados:")
            cursor.execute("""
                SELECT id, titulo, modalidade, orgao, created_at 
                FROM cursos 
                ORDER BY id 
                LIMIT 5
            """)
            
            for curso in cursor.fetchall():
                logger.info(f"   • ID {curso['id']}: {curso['titulo']} ({curso['modalidade']})")
            
            logger.info("=" * 80)
            logger.info("✅ Verificação concluída!")
            
    finally:
        connection.close()


def main():
    """Função principal"""
    try:
        # Executar migração
        success = migrate_csv_files()
        
        if success:
            # Verificar dados
            verify_migration()
            
            logger.info("")
            logger.info("🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            logger.info("")
            logger.info("📝 Próximos passos:")
            logger.info("   1. Verifique os dados no banco de dados")
            logger.info("   2. Teste a aplicação web")
            logger.info("   3. Delete este script após confirmar que está tudo OK")
            logger.info("")
            
            return 0
        else:
            logger.error("❌ Migração falhou!")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
