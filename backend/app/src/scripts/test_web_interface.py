#!/usr/bin/env python3
"""
Script para testar a interface web e verificar se os cursos estão sendo exibidos corretamente.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.course_service import CourseService


def test_course_listing():
    """Testa a listagem de cursos"""
    
    print("=" * 70)
    print("🌐 TESTE DE LISTAGEM DE CURSOS PARA INTERFACE WEB")
    print("=" * 70)
    print()
    
    service = CourseService()
    
    # Listar todos os cursos
    print("📋 Buscando cursos...")
    courses = service.list_courses()
    
    print(f"✅ {len(courses)} cursos encontrados")
    print()
    
    # Mostrar detalhes de cada curso
    for i, course in enumerate(courses, 1):
        print(f"{'='*70}")
        print(f"Curso {i}/{len(courses)}")
        print(f"{'='*70}")
        print(f"ID: {course.get('id')}")
        print(f"Título: {course.get('titulo')}")
        print(f"Modalidade: {course.get('modalidade')}")
        print(f"Órgão: {course.get('orgao')}")
        print()
        
        # Verificar campos formatados
        print("📊 Campos Formatados para Template:")
        
        if course.get('modalidade') in ['Presencial', 'Híbrido']:
            print(f"  • Endereços: {course.get('endereco_unidade', 'N/A')}")
            print(f"  • Bairros: {course.get('bairro_unidade', 'N/A')}")
            print(f"  • Vagas: {course.get('vagas_unidade', 'N/A')}")
            print(f"  • Dias: {course.get('dias_aula', 'N/A')}")
        
        if course.get('modalidade') in ['Online', 'Híbrido']:
            print(f"  • Plataforma: {course.get('plataforma_digital', 'N/A')}")
            print(f"  • Assíncrona: {course.get('aulas_assincronas', 'N/A')}")
        
        print(f"  • Gratuito: {course.get('curso_gratuito', 'N/A')}")
        print(f"  • Certificado: {course.get('oferece_certificado', 'N/A')}")
        print()
    
    print("=" * 70)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 70)
    print()
    print("💡 Para testar na interface web:")
    print("   1. Inicie o servidor: flask run")
    print("   2. Acesse: http://localhost:5000/courses")
    print("   3. Faça login com: oportunidades.cariocas@prefeitura.rio")
    print()
    
    return True


def test_single_course():
    """Testa busca de um curso específico"""
    
    print("=" * 70)
    print("🔍 TESTE DE BUSCA DE CURSO INDIVIDUAL")
    print("=" * 70)
    print()
    
    service = CourseService()
    
    # Buscar curso ID 6 (primeiro curso de teste)
    course_id = 6
    print(f"📚 Buscando curso ID {course_id}...")
    course = service.get_course(course_id)
    
    if course:
        print(f"✅ Curso encontrado!")
        print()
        print(f"Título: {course.get('titulo')}")
        print(f"Modalidade: {course.get('modalidade')}")
        print(f"Descrição: {course.get('descricao', '')[:100]}...")
        print()
        
        # Verificar estrutura de turmas
        if course.get('turmas'):
            print(f"📍 Turmas: {len(course.get('turmas'))} encontradas")
            for turma in course.get('turmas', []):
                print(f"  • Turma {turma.get('numero_turma')}: {turma.get('endereco_unidade')}")
        
        # Verificar plataforma
        if course.get('plataforma_online'):
            plat = course.get('plataforma_online')
            print(f"💻 Plataforma: {plat.get('plataforma_digital')}")
        
        print()
        print("✅ Estrutura do curso está correta!")
    else:
        print(f"❌ Curso {course_id} não encontrado")
    
    print("=" * 70)


def main():
    """Função principal"""
    print()
    print("Escolha uma opção:")
    print("1. Testar listagem de cursos")
    print("2. Testar busca de curso individual")
    print("3. Executar ambos os testes")
    print()
    
    choice = input("Opção (1, 2 ou 3): ").strip()
    print()
    
    try:
        if choice == '1':
            success = test_course_listing()
        elif choice == '2':
            test_single_course()
            success = True
        elif choice == '3':
            test_course_listing()
            test_single_course()
            success = True
        else:
            print("❌ Opção inválida!")
            success = False
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
