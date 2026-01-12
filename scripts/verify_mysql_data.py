#!/usr/bin/env python3
"""
Script de verificação de dados no MySQL
Verifica a integridade e consistência dos dados migrados
Autor: Sistema WebCiclo
Data: 2025-11-18
"""

import os
import pymysql
from dotenv import load_dotenv
import logging
from collections import defaultdict

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
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


def get_db_connection():
    """Cria conexão com o banco de dados"""
    return pymysql.connect(**DB_CONFIG)


def verify_data_integrity():
    """Verifica a integridade dos dados"""
    logger.info("=" * 80)
    logger.info("🔍 VERIFICAÇÃO DE INTEGRIDADE DOS DADOS")
    logger.info("=" * 80)
    
    connection = get_db_connection()
    issues = []
    
    try:
        with connection.cursor() as cursor:
            # 1. Verificar cursos sem turmas (Presencial/Híbrido)
            logger.info("\n📋 Verificando cursos presenciais sem turmas...")
            cursor.execute("""
                SELECT c.id, c.titulo, c.modalidade
                FROM cursos c
                LEFT JOIN turmas t ON c.id = t.curso_id
                WHERE c.modalidade IN ('Presencial', 'Híbrido')
                AND t.id IS NULL
            """)
            
            cursos_sem_turmas = cursor.fetchall()
            if cursos_sem_turmas:
                logger.warning(f"⚠️ {len(cursos_sem_turmas)} cursos presenciais sem turmas:")
                for curso in cursos_sem_turmas:
                    logger.warning(f"   • ID {curso['id']}: {curso['titulo']}")
                    issues.append(f"Curso {curso['id']} sem turmas")
            else:
                logger.info("✅ Todos os cursos presenciais têm turmas")
            
            # 2. Verificar cursos online sem plataforma
            logger.info("\n💻 Verificando cursos online sem plataforma...")
            cursor.execute("""
                SELECT c.id, c.titulo, c.modalidade
                FROM cursos c
                LEFT JOIN plataformas_online p ON c.id = p.curso_id
                WHERE c.modalidade IN ('Online', 'Híbrido')
                AND p.id IS NULL
            """)
            
            cursos_sem_plataforma = cursor.fetchall()
            if cursos_sem_plataforma:
                logger.warning(f"⚠️ {len(cursos_sem_plataforma)} cursos online sem plataforma:")
                for curso in cursos_sem_plataforma:
                    logger.warning(f"   • ID {curso['id']}: {curso['titulo']}")
                    issues.append(f"Curso {curso['id']} sem plataforma")
            else:
                logger.info("✅ Todos os cursos online têm plataforma")
            
            # 3. Verificar campos obrigatórios vazios
            logger.info("\n📝 Verificando campos obrigatórios...")
            cursor.execute("""
                SELECT id, titulo
                FROM cursos
                WHERE titulo IS NULL OR titulo = ''
                OR orgao IS NULL OR orgao = ''
                OR modalidade IS NULL OR modalidade = ''
            """)
            
            cursos_campos_vazios = cursor.fetchall()
            if cursos_campos_vazios:
                logger.warning(f"⚠️ {len(cursos_campos_vazios)} cursos com campos obrigatórios vazios:")
                for curso in cursos_campos_vazios:
                    logger.warning(f"   • ID {curso['id']}: {curso['titulo']}")
                    issues.append(f"Curso {curso['id']} com campos vazios")
            else:
                logger.info("✅ Todos os cursos têm campos obrigatórios preenchidos")
            
            # 4. Verificar datas inválidas
            logger.info("\n📅 Verificando datas...")
            cursor.execute("""
                SELECT id, titulo, inicio_inscricoes, fim_inscricoes
                FROM cursos
                WHERE inicio_inscricoes > fim_inscricoes
            """)
            
            cursos_datas_invalidas = cursor.fetchall()
            if cursos_datas_invalidas:
                logger.warning(f"⚠️ {len(cursos_datas_invalidas)} cursos com datas inválidas:")
                for curso in cursos_datas_invalidas:
                    logger.warning(f"   • ID {curso['id']}: {curso['titulo']}")
                    issues.append(f"Curso {curso['id']} com datas inválidas")
            else:
                logger.info("✅ Todas as datas estão corretas")
            
            # 5. Estatísticas por modalidade
            logger.info("\n📊 Estatísticas por modalidade:")
            cursor.execute("""
                SELECT modalidade, COUNT(*) as total
                FROM cursos
                GROUP BY modalidade
            """)
            
            for row in cursor.fetchall():
                logger.info(f"   • {row['modalidade']}: {row['total']} cursos")
            
            # 6. Estatísticas por órgão
            logger.info("\n🏛️ Top 5 órgãos com mais cursos:")
            cursor.execute("""
                SELECT orgao, COUNT(*) as total
                FROM cursos
                GROUP BY orgao
                ORDER BY total DESC
                LIMIT 5
            """)
            
            for row in cursor.fetchall():
                logger.info(f"   • {row['orgao']}: {row['total']} cursos")
            
            # 7. Verificar turmas sem dias da semana
            logger.info("\n📆 Verificando turmas sem dias da semana...")
            cursor.execute("""
                SELECT t.id, t.curso_id, c.titulo
                FROM turmas t
                JOIN cursos c ON t.curso_id = c.id
                LEFT JOIN turmas_dias_semana tds ON t.id = tds.turma_id
                WHERE tds.id IS NULL
            """)
            
            turmas_sem_dias = cursor.fetchall()
            if turmas_sem_dias:
                logger.warning(f"⚠️ {len(turmas_sem_dias)} turmas sem dias da semana definidos")
                issues.append(f"{len(turmas_sem_dias)} turmas sem dias")
            else:
                logger.info("✅ Todas as turmas têm dias da semana definidos")
            
            # Resumo
            logger.info("\n" + "=" * 80)
            if issues:
                logger.warning(f"⚠️ VERIFICAÇÃO CONCLUÍDA COM {len(issues)} PROBLEMAS")
                logger.warning("\nProblemas encontrados:")
                for issue in issues:
                    logger.warning(f"   • {issue}")
            else:
                logger.info("✅ VERIFICAÇÃO CONCLUÍDA - NENHUM PROBLEMA ENCONTRADO!")
            logger.info("=" * 80)
            
            return len(issues) == 0
            
    finally:
        connection.close()


def show_sample_data():
    """Mostra dados de exemplo"""
    logger.info("\n" + "=" * 80)
    logger.info("📋 DADOS DE EXEMPLO")
    logger.info("=" * 80)
    
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # Buscar um curso completo com turmas
            cursor.execute("""
                SELECT * FROM cursos
                WHERE modalidade = 'Presencial'
                LIMIT 1
            """)
            
            curso = cursor.fetchone()
            if curso:
                logger.info(f"\n📚 Curso: {curso['titulo']}")
                logger.info(f"   • ID: {curso['id']}")
                logger.info(f"   • Modalidade: {curso['modalidade']}")
                logger.info(f"   • Órgão: {curso['orgao']}")
                logger.info(f"   • Inscrições: {curso['inicio_inscricoes']} a {curso['fim_inscricoes']}")
                logger.info(f"   • Gratuito: {curso['curso_gratuito']}")
                
                # Buscar turmas
                cursor.execute("""
                    SELECT * FROM turmas
                    WHERE curso_id = %s
                """, (curso['id'],))
                
                turmas = cursor.fetchall()
                logger.info(f"\n🏫 Turmas ({len(turmas)}):")
                for turma in turmas:
                    logger.info(f"   • Turma {turma['numero_turma']}")
                    logger.info(f"     - Endereço: {turma['endereco_unidade']}")
                    logger.info(f"     - Bairro: {turma['bairro_unidade']}")
                    logger.info(f"     - Vagas: {turma['vagas_totais']}")
                    logger.info(f"     - Horário: {turma['horario_inicio']} às {turma['horario_fim']}")
                    
                    # Buscar dias da semana
                    cursor.execute("""
                        SELECT dia_semana FROM turmas_dias_semana
                        WHERE turma_id = %s
                    """, (turma['id'],))
                    
                    dias = [d['dia_semana'] for d in cursor.fetchall()]
                    logger.info(f"     - Dias: {', '.join(dias)}")
            
            logger.info("\n" + "=" * 80)
            
    finally:
        connection.close()


def main():
    """Função principal"""
    try:
        # Verificar integridade
        is_valid = verify_data_integrity()
        
        # Mostrar dados de exemplo
        show_sample_data()
        
        if is_valid:
            logger.info("\n✅ Todos os dados estão OK!")
            return 0
        else:
            logger.warning("\n⚠️ Alguns problemas foram encontrados. Revise os logs acima.")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
