# pdf_generator.py
# Módulo para geração de arquivos PDF a partir dos dados do curso

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf(course_data):
    """
    Gera um arquivo PDF com os dados do curso.
    
    Args:
        course_data (dict): Dicionário contendo os dados do curso.
        
    Returns:
        str: Caminho do arquivo PDF gerado.
    """
    # Criar diretório PDF se não existir
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'PDF')
    print(f"Diretório PDF: {pdf_dir}")
    if not os.path.exists(pdf_dir):
        print(f"Criando diretório PDF: {pdf_dir}")
        os.makedirs(pdf_dir)
    
    # Gerar nome do arquivo baseado na data atual e título do curso
    data_atual = datetime.now().strftime('%Y%m%d')
    titulo_formatado = course_data['titulo'].replace(' ', '_')
    filename = f"{data_atual}_{titulo_formatado}.pdf"
    filepath = os.path.join(pdf_dir, filename)
    print(f"Caminho completo do arquivo PDF: {filepath}")
    
    # Configurar documento PDF
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Título do documento
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.darkblue,
        spaceAfter=12
    )
    elements.append(Paragraph(f"Detalhes do Curso: {course_data['titulo']}", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Descrição do curso
    elements.append(Paragraph("<b>Descrição:</b>", styles["Heading3"]))
    elements.append(Paragraph(course_data['descricao'], styles["Normal"]))
    elements.append(Spacer(1, 0.25*inch))
    
    # Informações do curso em formato de tabela
    data = [
        ["Campo", "Valor"],
        ["ID", str(course_data['id'])],
        ["Título", course_data['titulo']],
        ["Início das Inscrições", course_data['inicio_inscricoes']],
        ["Fim das Inscrições", course_data['fim_inscricoes']],
        ["Órgão", course_data['orgao']],
        ["Tema", course_data['tema']],
        ["Modalidade", course_data['modalidade']],
        ["Carga Horária", course_data['carga_horaria']],
        ["Curso Gratuito", 'Sim' if course_data['curso_gratuito'] == 'sim' else 'Não'],
        ["Valor do Curso", course_data['valor_curso'] if 'valor_curso' in course_data and course_data['valor_curso'] else 'Gratuito'],
        ["Oferece Bolsa", 'Sim' if course_data.get('oferece_bolsa') == 'sim' else 'Não'],
        ["Valor da Bolsa", course_data['valor_bolsa'] if 'valor_bolsa' in course_data and course_data['valor_bolsa'] else 'Não aplicável'],
        ["Requisitos para a Obtenção da Bolsa", course_data['requisitos_bolsa'] if 'requisitos_bolsa' in course_data and course_data['requisitos_bolsa'] else 'Não aplicável'],
        ["Público Alvo", course_data['publico_alvo']],
        ["Oferece Certificado", 'Sim' if course_data['oferece_certificado'] == 'sim' else 'Não'],
        ["Pré-requisitos para Certificado", course_data['pre_requisitos'] if course_data['oferece_certificado'] == 'sim' else 'Não aplicável'],
        ["Informações Complementares para Inscrição", course_data['info_complementares']],
        ["Data de Criação", course_data['created_at']]
    ]
    
    # Criar tabela
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    
    # Rodapé
    elements.append(Spacer(1, 0.5*inch))
    footer_text = f"Documento gerado automaticamente em {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    elements.append(Paragraph(footer_text, styles["Italic"]))
    
    # Gerar PDF
    doc.build(elements)
    
    return filepath