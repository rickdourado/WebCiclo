# pdf_generator.py
# Módulo para geração de arquivos PDF a partir dos dados do curso

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

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
    titulo_formatado = course_data['titulo'].replace(' ', '_').replace('/', '_').replace('\\', '_')
    filename = f"{data_atual}_{titulo_formatado}.pdf"
    filepath = os.path.join(pdf_dir, filename)
    print(f"Caminho completo do arquivo PDF: {filepath}")
    
    # Configurar documento PDF com margens adequadas
    doc = SimpleDocTemplate(
        filepath, 
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    elements = []
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.darkblue,
        spaceAfter=12,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    field_style = ParagraphStyle(
        'Field',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    # Cabeçalho do documento
    elements.append(Paragraph("WebCiclo.Carioca", title_style))
    elements.append(Paragraph("Sistema de Curadoria de Cursos", ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=20
    )))
    elements.append(Spacer(1, 0.3*inch))
    
    # Título do curso
    elements.append(Paragraph(f"<b>DETALHES DO CURSO</b>", section_style))
    elements.append(Paragraph(f"<b>{course_data['titulo']}</b>", ParagraphStyle(
        'CourseTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.black,
        spaceAfter=15,
        fontName='Helvetica-Bold'
    )))
    
    # Descrição do curso
    if course_data.get('descricao'):
        elements.append(Paragraph("<b>Descrição:</b>", section_style))
        elements.append(Paragraph(course_data['descricao'], field_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Informações básicas
    elements.append(Paragraph("<b>INFORMAÇÕES BÁSICAS</b>", section_style))
    
    basic_info = [
        ["ID do Curso", str(course_data.get('id', 'N/A'))],
        ["Título", course_data.get('titulo', 'N/A')],
        ["Órgão Responsável", course_data.get('orgao', 'N/A')],
        ["Tema", course_data.get('tema', 'N/A')],
        ["Modalidade", course_data.get('modalidade', 'N/A')],
        ["Data de Criação", course_data.get('created_at', 'N/A')]
    ]
    
    # Adicionar informações específicas da modalidade
    if course_data.get('modalidade') == 'Online':
        if course_data.get('plataforma_digital'):
            basic_info.append(["Plataforma Digital", course_data['plataforma_digital']])
        if course_data.get('aulas_assincronas'):
            aulas_tipo = "Assíncronas" if course_data['aulas_assincronas'] == 'sim' else "Síncronas"
            basic_info.append(["Tipo de Aulas", aulas_tipo])
    
    # Criar tabela de informações básicas
    basic_table = Table(basic_info, colWidths=[2.5*inch, 4*inch])
    basic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    elements.append(basic_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Informações de período
    elements.append(Paragraph("<b>PERÍODOS E HORÁRIOS</b>", section_style))
    
    period_info = [
        ["Início das Inscrições", course_data.get('inicio_inscricoes', 'N/A')],
        ["Fim das Inscrições", course_data.get('fim_inscricoes', 'N/A')]
    ]
    
    # Adicionar informações de aulas se disponíveis
    if course_data.get('inicio_aulas_data'):
        period_info.append(["Início das Aulas", course_data['inicio_aulas_data']])
    if course_data.get('fim_aulas_data'):
        period_info.append(["Fim das Aulas", course_data['fim_aulas_data']])
    if course_data.get('horario_inicio'):
        period_info.append(["Horário de Início", course_data['horario_inicio']])
    if course_data.get('horario_fim'):
        period_info.append(["Horário de Fim", course_data['horario_fim']])
    if course_data.get('dias_aula'):
        period_info.append(["Dias da Aula", course_data['dias_aula']])
    
    period_table = Table(period_info, colWidths=[2.5*inch, 4*inch])
    period_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    elements.append(period_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Informações acadêmicas
    elements.append(Paragraph("<b>INFORMAÇÕES ACADÊMICAS</b>", section_style))
    
    academic_info = []
    
    if course_data.get('carga_horaria'):
        academic_info.append(["Carga Horária", course_data['carga_horaria']])
    
    if course_data.get('vagas_unidade'):
        academic_info.append(["Vagas Disponíveis", course_data['vagas_unidade']])
    
    if course_data.get('publico_alvo'):
        academic_info.append(["Público Alvo", course_data['publico_alvo']])
    
    if course_data.get('oferece_certificado'):
        certificado = "Sim" if course_data['oferece_certificado'] == 'sim' else "Não"
        academic_info.append(["Oferece Certificado", certificado])
        
        if course_data.get('pre_requisitos') and course_data['oferece_certificado'] == 'sim':
            academic_info.append(["Pré-requisitos para Certificado", course_data['pre_requisitos']])
    
    if course_data.get('acessibilidade'):
        academic_info.append(["Acessibilidade", course_data['acessibilidade']])
    
    if course_data.get('recursos_acessibilidade'):
        academic_info.append(["Recursos de Acessibilidade", course_data['recursos_acessibilidade']])
    
    if academic_info:
        academic_table = Table(academic_info, colWidths=[2.5*inch, 4*inch])
        academic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(academic_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Informações financeiras
    elements.append(Paragraph("<b>INFORMAÇÕES FINANCEIRAS</b>", section_style))
    
    financial_info = []
    
    if course_data.get('curso_gratuito'):
        gratuito = "Sim" if course_data['curso_gratuito'] == 'sim' else "Não"
        financial_info.append(["Curso Gratuito", gratuito])
    
    if course_data.get('valor_curso') and course_data.get('curso_gratuito') != 'sim':
        financial_info.append(["Valor do Curso", course_data['valor_curso']])
    
    if course_data.get('valor_curso_inteira'):
        financial_info.append(["Valor Inteira", course_data['valor_curso_inteira']])
    
    if course_data.get('valor_curso_meia'):
        financial_info.append(["Valor Meia", course_data['valor_curso_meia']])
    
    if course_data.get('requisitos_meia'):
        financial_info.append(["Requisitos para Meia", course_data['requisitos_meia']])
    
    if course_data.get('oferece_bolsa'):
        bolsa = "Sim" if course_data['oferece_bolsa'] == 'sim' else "Não"
        financial_info.append(["Oferece Bolsa", bolsa])
    
    if course_data.get('valor_bolsa') and course_data.get('oferece_bolsa') == 'sim':
        financial_info.append(["Valor da Bolsa", course_data['valor_bolsa']])
    
    if course_data.get('requisitos_bolsa') and course_data.get('oferece_bolsa') == 'sim':
        financial_info.append(["Requisitos para Bolsa", course_data['requisitos_bolsa']])
    
    if financial_info:
        financial_table = Table(financial_info, colWidths=[2.5*inch, 4*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(financial_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Informações de localização (para cursos presenciais/híbridos)
    if course_data.get('modalidade') in ['Presencial', 'Híbrido'] and course_data.get('endereco_unidade'):
        elements.append(Paragraph("<b>INFORMAÇÕES DE LOCALIZAÇÃO</b>", section_style))
        
        location_info = []
        
        if course_data.get('endereco_unidade'):
            location_info.append(["Endereço", course_data['endereco_unidade']])
        
        if course_data.get('bairro_unidade'):
            location_info.append(["Bairro", course_data['bairro_unidade']])
        
        if course_data.get('vagas_unidade'):
            location_info.append(["Vagas por Unidade", course_data['vagas_unidade']])
        
        if location_info:
            location_table = Table(location_info, colWidths=[2.5*inch, 4*inch])
            location_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BACKGROUND', (1, 0), (1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            elements.append(location_table)
            elements.append(Spacer(1, 0.2*inch))
    
    # Informações de parceiros externos
    if course_data.get('parceiro_externo') == 'sim':
        elements.append(Paragraph("<b>PARCEIRO EXTERNO</b>", section_style))
        
        partner_info = []
        
        if course_data.get('parceiro_nome'):
            partner_info.append(["Nome do Parceiro", course_data['parceiro_nome']])
        
        if course_data.get('parceiro_link'):
            partner_info.append(["Link do Parceiro", course_data['parceiro_link']])
        
        if partner_info:
            partner_table = Table(partner_info, colWidths=[2.5*inch, 4*inch])
            partner_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BACKGROUND', (1, 0), (1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            elements.append(partner_table)
            elements.append(Spacer(1, 0.2*inch))
    
    # Informações complementares
    if course_data.get('info_complementares'):
        elements.append(Paragraph("<b>INFORMAÇÕES COMPLEMENTARES</b>", section_style))
        elements.append(Paragraph(course_data['info_complementares'], field_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Rodapé
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("─" * 50, ParagraphStyle(
        'Separator',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )))
    elements.append(Spacer(1, 0.1*inch))
    
    footer_text = f"Documento gerado automaticamente pelo WebCiclo.Carioca em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    elements.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Italic'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )))
    
    # Gerar PDF
    doc.build(elements)
    
    return filepath