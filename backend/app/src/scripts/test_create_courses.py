#!/usr/bin/env python3
"""
Script para testar criação de cursos no banco de dados MySQL.
Cria 5 cursos de exemplo com diferentes modalidades.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.course_repository_mysql import CourseRepositoryMySQL
from src.services.course_service import CourseService


def create_test_courses():
    """Cria cursos de teste no banco de dados"""
    
    print("=" * 70)
    print("🎓 TESTE DE CRIAÇÃO DE CURSOS NO MYSQL")
    print("=" * 70)
    print()
    
    repository = CourseRepositoryMySQL()
    
    # Data base para os cursos
    hoje = datetime.now()
    inicio_inscricoes = hoje.strftime('%Y-%m-%d')
    fim_inscricoes = (hoje + timedelta(days=30)).strftime('%Y-%m-%d')
    inicio_aulas = (hoje + timedelta(days=45)).strftime('%Y-%m-%d')
    fim_aulas = (hoje + timedelta(days=90)).strftime('%Y-%m-%d')
    
    # Lista de cursos de teste
    cursos_teste = [
        # 1. CURSO PRESENCIAL - Múltiplas turmas
        {
            'tipo_acao': 'Curso',
            'titulo': 'Curso de Desenvolvimento Web Full Stack',
            'titulo_original': 'Curso de Desenvolvimento Web Full Stack',
            'descricao': 'Aprenda a desenvolver aplicações web completas usando tecnologias modernas como React, Node.js e MySQL.',
            'descricao_original': 'Aprenda a desenvolver aplicações web completas usando tecnologias modernas.',
            'inicio_inscricoes': inicio_inscricoes,
            'fim_inscricoes': fim_inscricoes,
            'orgao': 'Secretaria Municipal de Ciência, Tecnologia e Inovação - SMCT',
            'tema': 'Tecnologia',
            'carga_horaria': '120 horas',
            'modalidade': 'Presencial',
            'acessibilidade': 'acessivel',
            'recursos_acessibilidade': 'Rampas de acesso, intérprete de libras, material em braille',
            'publico_alvo': 'Jovens e adultos interessados em programação',
            'curso_gratuito': 'sim',
            'oferece_certificado': 'sim',
            'pre_requisitos': 'Conhecimentos básicos de informática',
            'oferece_bolsa': 'nao',
            'info_complementares': 'Curso com certificado reconhecido',
            'info_adicionais': 'Material didático incluso',
            'parceiro_externo': 'nao',
            'status': 'ativo',
            # Turmas presenciais
            'enderecos_unidades': [
                'Rua da Assembleia, 10 - Centro',
                'Av. Rio Branco, 156 - Centro',
                'Rua Primeiro de Março, 66 - Centro'
            ],
            'bairros_unidades': ['Centro', 'Centro', 'Centro'],
            'complementos_unidades': ['Sala 201', 'Sala 305', 'Sala 102'],
            'vagas_unidades': [30, 25, 35],
            'inicio_aulas_unidades': [inicio_aulas, inicio_aulas, inicio_aulas],
            'fim_aulas_unidades': [fim_aulas, fim_aulas, fim_aulas],
            'horario_inicio_unidades': ['09:00', '14:00', '18:00'],
            'horario_fim_unidades': ['12:00', '17:00', '21:00'],
            'dias_aula_unidades': [
                ['Segunda-feira', 'Quarta-feira', 'Sexta-feira'],
                ['Terça-feira', 'Quinta-feira'],
                ['Segunda-feira', 'Quarta-feira']
            ]
        },
        
        # 2. CURSO ONLINE - Aulas assíncronas
        {
            'tipo_acao': 'Curso',
            'titulo': 'Marketing Digital para Pequenos Negócios',
            'titulo_original': 'Marketing Digital para Pequenos Negócios',
            'descricao': 'Domine as estratégias de marketing digital para alavancar seu negócio nas redes sociais e Google.',
            'descricao_original': 'Estratégias de marketing digital para pequenos empreendedores.',
            'inicio_inscricoes': inicio_inscricoes,
            'fim_inscricoes': fim_inscricoes,
            'orgao': 'Secretaria Municipal de Desenvolvimento Econômico – SMDE',
            'tema': 'Empreendedorismo',
            'carga_horaria': '40 horas',
            'modalidade': 'Online',
            'acessibilidade': 'nao_acessivel',
            'publico_alvo': 'Empreendedores e microempresários',
            'curso_gratuito': 'sim',
            'oferece_certificado': 'sim',
            'pre_requisitos': 'Ter um negócio ou projeto empreendedor',
            'oferece_bolsa': 'nao',
            'info_complementares': 'Curso 100% online e gratuito',
            'parceiro_externo': 'sim',
            'parceiro_nome': 'SEBRAE Rio',
            'parceiro_link': 'https://www.sebrae-rj.com.br',
            'status': 'ativo',
            # Plataforma online
            'plataforma_digital': 'Google Classroom',
            'link_acesso': 'https://classroom.google.com/curso-marketing',
            'vagas_online': 100,
            'aulas_assincronas': 'sim'
        },
        
        # 3. CURSO ONLINE - Aulas síncronas
        {
            'tipo_acao': 'Oficina',
            'titulo': 'Oficina de Fotografia Digital',
            'titulo_original': 'Oficina de Fotografia Digital',
            'descricao': 'Aprenda técnicas profissionais de fotografia digital, composição, iluminação e edição de imagens.',
            'descricao_original': 'Técnicas de fotografia digital para iniciantes.',
            'inicio_inscricoes': inicio_inscricoes,
            'fim_inscricoes': fim_inscricoes,
            'orgao': 'Secretaria Municipal de Cultura - SMC',
            'tema': 'Arte e Cultura',
            'carga_horaria': '20 horas',
            'modalidade': 'Online',
            'acessibilidade': 'acessivel',
            'recursos_acessibilidade': 'Legendas ao vivo, intérprete de libras',
            'publico_alvo': 'Interessados em fotografia',
            'curso_gratuito': 'nao',
            'valor_curso_inteira': 150.00,
            'valor_curso_meia': 75.00,
            'requisitos_meia': 'Estudantes, idosos, PCD',
            'oferece_certificado': 'sim',
            'oferece_bolsa': 'sim',
            'valor_bolsa': 150.00,
            'requisitos_bolsa': 'Renda familiar até 2 salários mínimos',
            'info_complementares': 'Material de apoio digital incluso',
            'parceiro_externo': 'nao',
            'status': 'ativo',
            # Plataforma online com aulas síncronas
            'plataforma_digital': 'Zoom',
            'link_acesso': 'https://zoom.us/j/fotografia2025',
            'vagas_online': 50,
            'aulas_assincronas': 'nao',
            'inicio_aulas_online': inicio_aulas,
            'fim_aulas_online': fim_aulas,
            'horario_inicio_online': '19:00',
            'horario_fim_online': '21:00',
            'dias_aula_online': ['Terça-feira', 'Quinta-feira']
        },
        
        # 4. CURSO HÍBRIDO
        {
            'tipo_acao': 'Curso',
            'titulo': 'Gestão de Projetos com Metodologias Ágeis',
            'titulo_original': 'Gestão de Projetos com Metodologias Ágeis',
            'descricao': 'Aprenda Scrum, Kanban e outras metodologias ágeis para gerenciar projetos de forma eficiente.',
            'descricao_original': 'Metodologias ágeis para gestão de projetos.',
            'inicio_inscricoes': inicio_inscricoes,
            'fim_inscricoes': fim_inscricoes,
            'orgao': 'Secretaria Municipal de Trabalho e Renda - SMTE',
            'tema': 'Gestão',
            'carga_horaria': '60 horas',
            'modalidade': 'Híbrido',
            'acessibilidade': 'acessivel',
            'recursos_acessibilidade': 'Acessibilidade física e digital',
            'publico_alvo': 'Profissionais e estudantes de gestão',
            'curso_gratuito': 'sim',
            'oferece_certificado': 'sim',
            'pre_requisitos': 'Experiência profissional ou acadêmica',
            'oferece_bolsa': 'nao',
            'info_complementares': 'Certificado reconhecido pelo PMI',
            'parceiro_externo': 'sim',
            'parceiro_nome': 'Fundação Getúlio Vargas',
            'parceiro_link': 'https://www.fgv.br',
            'status': 'ativo',
            # Turmas presenciais
            'enderecos_unidades': [
                'Av. Presidente Vargas, 502 - Centro',
                'Rua Buenos Aires, 68 - Centro'
            ],
            'bairros_unidades': ['Centro', 'Centro'],
            'complementos_unidades': ['Auditório 1', 'Sala 401'],
            'vagas_unidades': [40, 30],
            'inicio_aulas_unidades': [inicio_aulas, inicio_aulas],
            'fim_aulas_unidades': [fim_aulas, fim_aulas],
            'horario_inicio_unidades': ['09:00', '14:00'],
            'horario_fim_unidades': ['13:00', '18:00'],
            'dias_aula_unidades': [
                ['Segunda-feira', 'Quarta-feira'],
                ['Terça-feira', 'Quinta-feira']
            ],
            # Plataforma online
            'plataforma_digital': 'Microsoft Teams',
            'link_acesso': 'https://teams.microsoft.com/gestao-projetos',
            'vagas_online': 60,
            'aulas_assincronas': 'nao',
            'inicio_aulas_online': inicio_aulas,
            'fim_aulas_online': fim_aulas,
            'horario_inicio_online': '19:00',
            'horario_fim_online': '22:00',
            'dias_aula_online': ['Sexta-feira']
        },
        
        # 5. PALESTRA PRESENCIAL - Uma única turma
        {
            'tipo_acao': 'Palestra',
            'titulo': 'Inovação e Transformação Digital no Setor Público',
            'titulo_original': 'Inovação e Transformação Digital no Setor Público',
            'descricao': 'Palestra sobre as tendências de transformação digital e inovação aplicadas ao setor público.',
            'descricao_original': 'Transformação digital no setor público.',
            'inicio_inscricoes': inicio_inscricoes,
            'fim_inscricoes': (hoje + timedelta(days=15)).strftime('%Y-%m-%d'),
            'orgao': 'Secretaria Municipal de Ciência, Tecnologia e Inovação - SMCT',
            'tema': 'Tecnologia',
            'carga_horaria': '3 horas',
            'modalidade': 'Presencial',
            'acessibilidade': 'acessivel',
            'recursos_acessibilidade': 'Rampas, elevador, intérprete de libras',
            'publico_alvo': 'Servidores públicos e gestores',
            'curso_gratuito': 'sim',
            'oferece_certificado': 'sim',
            'oferece_bolsa': 'nao',
            'info_complementares': 'Coffee break incluso',
            'parceiro_externo': 'nao',
            'status': 'ativo',
            # Uma única turma
            'enderecos_unidades': ['Rua Afonso Cavalcanti, 455 - Cidade Nova'],
            'bairros_unidades': ['Cidade Nova'],
            'complementos_unidades': ['Auditório Principal'],
            'vagas_unidades': [200],
            'inicio_aulas_unidades': [(hoje + timedelta(days=20)).strftime('%Y-%m-%d')],
            'fim_aulas_unidades': [(hoje + timedelta(days=20)).strftime('%Y-%m-%d')],
            'horario_inicio_unidades': ['14:00'],
            'horario_fim_unidades': ['17:00'],
            'dias_aula_unidades': [['Sexta-feira']]
        }
    ]
    
    # Criar cursos
    created_count = 0
    failed_count = 0
    user_id = 1  # ID do usuário admin
    
    for i, curso in enumerate(cursos_teste, 1):
        print(f"📚 Criando curso {i}/5: {curso['titulo']}")
        print(f"   Modalidade: {curso['modalidade']}")
        print(f"   Órgão: {curso['orgao']}")
        
        try:
            course_id = repository.create_course(curso, user_id)
            
            if course_id:
                print(f"   ✅ Criado com sucesso! ID: {course_id}")
                
                # Mostrar detalhes
                if curso['modalidade'] in ['Presencial', 'Híbrido']:
                    num_turmas = len(curso.get('enderecos_unidades', []))
                    print(f"   📍 Turmas presenciais: {num_turmas}")
                
                if curso['modalidade'] in ['Online', 'Híbrido']:
                    plataforma = curso.get('plataforma_digital', 'N/A')
                    vagas = curso.get('vagas_online', 0)
                    print(f"   💻 Plataforma: {plataforma} ({vagas} vagas)")
                
                created_count += 1
            else:
                print(f"   ❌ Erro ao criar curso")
                failed_count += 1
        
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            failed_count += 1
        
        print()
    
    print("=" * 70)
    print("📊 RESUMO")
    print("=" * 70)
    print(f"   ✅ Criados: {created_count}")
    print(f"   ❌ Falhas: {failed_count}")
    print(f"   📝 Total: {len(cursos_teste)}")
    print("=" * 70)
    
    return failed_count == 0


def list_created_courses():
    """Lista os cursos criados"""
    print()
    print("=" * 70)
    print("📋 CURSOS CADASTRADOS NO BANCO")
    print("=" * 70)
    print()
    
    repository = CourseRepositoryMySQL()
    courses = repository.find_all()
    
    if courses:
        for curso in courses:
            print(f"ID: {curso['id']}")
            print(f"   Título: {curso['titulo']}")
            print(f"   Modalidade: {curso['modalidade']}")
            print(f"   Órgão: {curso['orgao']}")
            print(f"   Status: {curso['status']}")
            print(f"   Criado em: {curso.get('created_at', 'N/A')}")
            print()
        
        print(f"Total: {len(courses)} curso(s)")
    else:
        print("⚠️  Nenhum curso encontrado no banco de dados.")
    
    print("=" * 70)


def main():
    """Função principal"""
    print()
    print("Escolha uma opção:")
    print("1. Criar cursos de teste")
    print("2. Listar cursos cadastrados")
    print("3. Criar cursos E listar")
    print()
    
    choice = input("Opção (1, 2 ou 3): ").strip()
    print()
    
    try:
        if choice == '1':
            success = create_test_courses()
        elif choice == '2':
            list_created_courses()
            success = True
        elif choice == '3':
            success = create_test_courses()
            if success:
                list_created_courses()
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
