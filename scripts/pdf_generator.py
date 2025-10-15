# pdf_generator.py
# Módulo para geração de arquivos PDF a partir dos dados do curso

import os
import textwrap
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.utils import simpleSplit
import re

def format_date_to_brazilian(date_str):
    """
    Converte datas para o formato brasileiro DD/MM/AAAA.
    
    Args:
        date_str (str): Data em qualquer formato (YYYY-MM-DD, YYYY/MM/DD, DD/MM/YYYY, etc.)
        
    Returns:
        str: Data no formato DD/MM/AAAA ou 'N/A' se inválida
    """
    if not date_str or date_str == 'N/A' or date_str.strip() == '':
        return 'N/A'
    
    date_str = str(date_str).strip()
    
    # Remover caracteres extras como | no final
    date_str = date_str.rstrip('|').strip()
    
    try:
        # Padrões de data que podem aparecer
        patterns = [
            (r'^(\d{4})-(\d{1,2})-(\d{1,2})$', r'\3/\2/\1'),  # YYYY-MM-DD -> DD/MM/YYYY
            (r'^(\d{4})/(\d{1,2})/(\d{1,2})$', r'\3/\2/\1'),  # YYYY/MM/DD -> DD/MM/YYYY
            (r'^(\d{1,2})/(\d{1,2})/(\d{4})$', r'\1/\2/\3'),   # DD/MM/YYYY -> DD/MM/YYYY (já correto)
            (r'^(\d{1,2})-(\d{1,2})-(\d{4})$', r'\1/\2/\3'),   # DD-MM-YYYY -> DD/MM/YYYY
        ]
        
        for pattern, replacement in patterns:
            match = re.match(pattern, date_str)
            if match:
                formatted_date = re.sub(pattern, replacement, date_str)
                # Validar se a data é válida
                day, month, year = formatted_date.split('/')
                day, month, year = int(day), int(month), int(year)
                
                # Verificação básica de validade
                if 1 <= day <= 31 and 1 <= month <= 12 and year >= 1900:
                    return f"{day:02d}/{month:02d}/{year}"
                
        # Se não conseguiu converter, retorna o valor original limpo
        return date_str
        
    except (ValueError, IndexError):
        return date_str

def wrap_text(text, max_width_chars=60):
    """
    Quebra texto longo em múltiplas linhas para melhor legibilidade.
    
    Args:
        text (str): Texto a ser quebrado
        max_width_chars (int): Número máximo de caracteres por linha
        
    Returns:
        str: Texto quebrado em múltiplas linhas
    """
    if not text or text == 'N/A':
        return text
    
    # Limpar quebras de linha existentes e espaços extras
    text = str(text).replace('\n', ' ').replace('\r', ' ').strip()
    
    # Quebrar texto em linhas menores
    wrapped_lines = textwrap.wrap(text, width=max_width_chars, break_long_words=True)
    return '\n'.join(wrapped_lines)

def clean_field_value(value, is_date=False):
    """
    Limpa e formata valores dos campos para exibição no PDF.
    
    Args:
        value: Valor do campo
        is_date (bool): Se True, converte para formato brasileiro DD/MM/AAAA
        
    Returns:
        str: Valor limpo e formatado
    """
    if not value or value == 'N/A' or value == '':
        return 'N/A'
    
    # Converter para string e limpar
    value_str = str(value).strip()
    
    # Se for uma data, converter para formato brasileiro
    if is_date:
        return format_date_to_brazilian(value_str)
    
    # Remover caracteres problemáticos para PDF
    value_str = value_str.replace('\r', ' ').replace('\n', ' ')
    
    # Limpar espaços múltiplos
    while '  ' in value_str:
        value_str = value_str.replace('  ', ' ')
    
    return value_str

def create_info_table(data, col_widths=None):
    """
    Cria uma tabela formatada com informações do curso.
    
    Args:
        data (list): Lista de listas com [campo, valor]
        col_widths (list): Larguras das colunas
        
    Returns:
        Table: Tabela formatada
    """
    if not data:
        return None
    
    # Larguras padrão se não especificadas
    if not col_widths:
        col_widths = [2.2*inch, 4.3*inch]
    
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # Quebra de palavra para CJK e outros idiomas
    ]))
    
    return table

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
    course_id = course_data.get('id', 'unknown')
    filename = f"{data_atual}_{course_id}_{titulo_formatado}.pdf"
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
        fontName='Helvetica',
        alignment=TA_JUSTIFY,
        leading=12  # Espaçamento entre linhas
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
    
    # Descrição do curso - NOVA FUNCIONALIDADE: Mostrar original e processada pelo Gemini
    if course_data.get('descricao_original') or course_data.get('descricao'):
        elements.append(Paragraph("<b>DESCRIÇÕES DO CURSO</b>", section_style))
        
        # Descrição original (inserida pelo usuário)
        if course_data.get('descricao_original'):
            elements.append(Paragraph("<b>Descrição Original:</b>", ParagraphStyle(
                'SubSection',
                parent=styles['Heading3'],
                fontSize=12,
                textColor=colors.darkblue,
                spaceAfter=8,
                spaceBefore=5,
                fontName='Helvetica-Bold'
            )))
            descricao_original_text = wrap_text(clean_field_value(course_data['descricao_original']), 70)
            elements.append(Paragraph(descricao_original_text, field_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # Descrição processada pelo Gemini (se diferente da original)
        if course_data.get('descricao') and course_data.get('descricao') != course_data.get('descricao_original'):
            elements.append(Paragraph("<b>Descrição Aprimorada (Gemini AI):</b>", ParagraphStyle(
                'SubSection',
                parent=styles['Heading3'],
                fontSize=12,
                textColor=colors.darkgreen,
                spaceAfter=8,
                spaceBefore=5,
                fontName='Helvetica-Bold'
            )))
            descricao_gemini_text = wrap_text(clean_field_value(course_data['descricao']), 70)
            elements.append(Paragraph(descricao_gemini_text, field_style))
            elements.append(Spacer(1, 0.15*inch))
        
        elements.append(Spacer(1, 0.1*inch))
    
    # Informações básicas
    elements.append(Paragraph("<b>INFORMAÇÕES BÁSICAS</b>", section_style))
    
    basic_info = [
        ["ID do Curso", clean_field_value(course_data.get('id'))],
        ["Título", wrap_text(clean_field_value(course_data.get('titulo')), 50)],
        ["Órgão Responsável", wrap_text(clean_field_value(course_data.get('orgao')), 50)],
        ["Tema", clean_field_value(course_data.get('tema'))],
        ["Modalidade", clean_field_value(course_data.get('modalidade'))],
        ["Data de Criação", clean_field_value(course_data.get('created_at'))]
    ]
    
    # Adicionar informações específicas da modalidade
    if course_data.get('modalidade') == 'Online':
        if course_data.get('plataforma_digital'):
            basic_info.append(["Plataforma Digital", wrap_text(clean_field_value(course_data['plataforma_digital']), 50)])
        if course_data.get('aulas_assincronas'):
            aulas_tipo = "Assíncronas" if course_data['aulas_assincronas'] == 'sim' else "Síncronas"
            basic_info.append(["Tipo de Aulas", aulas_tipo])
    
    # Criar tabela de informações básicas
    basic_table = create_info_table(basic_info)
    elements.append(basic_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Informações de período
    elements.append(Paragraph("<b>PERÍODOS E HORÁRIOS</b>", section_style))
    
    period_info = [
        ["Início das Inscrições", clean_field_value(course_data.get('inicio_inscricoes'), is_date=True)],
        ["Fim das Inscrições", clean_field_value(course_data.get('fim_inscricoes'), is_date=True)]
    ]
    
    # Adicionar informações de aulas se disponíveis
    if course_data.get('inicio_aulas_data'):
        period_info.append(["Início das Aulas", clean_field_value(course_data['inicio_aulas_data'], is_date=True)])
    if course_data.get('fim_aulas_data'):
        period_info.append(["Fim das Aulas", clean_field_value(course_data['fim_aulas_data'], is_date=True)])
    if course_data.get('horario_inicio'):
        period_info.append(["Horário de Início", clean_field_value(course_data['horario_inicio'])])
    if course_data.get('horario_fim'):
        period_info.append(["Horário de Fim", clean_field_value(course_data['horario_fim'])])
    if course_data.get('dias_aula'):
        period_info.append(["Dias da Aula", clean_field_value(course_data['dias_aula'])])
    
    period_table = create_info_table(period_info)
    elements.append(period_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Informações acadêmicas
    elements.append(Paragraph("<b>INFORMAÇÕES ACADÊMICAS</b>", section_style))
    
    academic_info = []
    
    if course_data.get('carga_horaria'):
        academic_info.append(["Carga Horária", clean_field_value(course_data['carga_horaria'])])
    
    if course_data.get('vagas_unidade'):
        academic_info.append(["Vagas Disponíveis", clean_field_value(course_data['vagas_unidade'])])
    
    if course_data.get('publico_alvo'):
        academic_info.append(["Público Alvo", wrap_text(clean_field_value(course_data['publico_alvo']), 50)])
    
    if course_data.get('oferece_certificado'):
        certificado = "Sim" if course_data['oferece_certificado'] == 'sim' else "Não"
        academic_info.append(["Oferece Certificado", certificado])
        
        if course_data.get('pre_requisitos') and course_data['oferece_certificado'] == 'sim':
            academic_info.append(["Pré-requisitos para Certificado", wrap_text(clean_field_value(course_data['pre_requisitos']), 50)])
    
    if course_data.get('acessibilidade'):
        academic_info.append(["Acessibilidade", clean_field_value(course_data['acessibilidade'])])
    
    if course_data.get('recursos_acessibilidade'):
        # Tratar recursos de acessibilidade com quebra de linha adequada
        recursos = clean_field_value(course_data['recursos_acessibilidade'])
        academic_info.append(["Recursos de Acessibilidade", wrap_text(recursos, 45)])
    
    if academic_info:
        academic_table = create_info_table(academic_info)
        elements.append(academic_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Informações financeiras
    elements.append(Paragraph("<b>INFORMAÇÕES FINANCEIRAS</b>", section_style))
    
    financial_info = []
    
    if course_data.get('curso_gratuito'):
        gratuito = "Sim" if course_data['curso_gratuito'] == 'sim' else "Não"
        financial_info.append(["Curso Gratuito", gratuito])
    
    if course_data.get('valor_curso') and course_data.get('curso_gratuito') != 'sim':
        financial_info.append(["Valor do Curso", clean_field_value(course_data['valor_curso'])])
    
    if course_data.get('valor_curso_inteira'):
        financial_info.append(["Valor Inteira", clean_field_value(course_data['valor_curso_inteira'])])
    
    if course_data.get('valor_curso_meia'):
        financial_info.append(["Valor Meia", clean_field_value(course_data['valor_curso_meia'])])
    
    if course_data.get('requisitos_meia'):
        financial_info.append(["Requisitos para Meia", wrap_text(clean_field_value(course_data['requisitos_meia']), 50)])
    
    if course_data.get('oferece_bolsa'):
        bolsa = "Sim" if course_data['oferece_bolsa'] == 'sim' else "Não"
        financial_info.append(["Oferece Bolsa", bolsa])
    
    if course_data.get('valor_bolsa') and course_data.get('oferece_bolsa') == 'sim':
        financial_info.append(["Valor da Bolsa", clean_field_value(course_data['valor_bolsa'])])
    
    if course_data.get('requisitos_bolsa') and course_data.get('oferece_bolsa') == 'sim':
        financial_info.append(["Requisitos para Bolsa", wrap_text(clean_field_value(course_data['requisitos_bolsa']), 50)])
    
    if financial_info:
        financial_table = create_info_table(financial_info)
        elements.append(financial_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Informações de localização (para cursos presenciais/híbridos)
    if course_data.get('modalidade') in ['Presencial', 'Híbrido'] and course_data.get('endereco_unidade'):
        elements.append(Paragraph("<b>INFORMAÇÕES DE LOCALIZAÇÃO</b>", section_style))
        
        location_info = []
        
        if course_data.get('endereco_unidade'):
            location_info.append(["Endereço", wrap_text(clean_field_value(course_data['endereco_unidade']), 50)])
        
        if course_data.get('bairro_unidade'):
            location_info.append(["Bairro", clean_field_value(course_data['bairro_unidade'])])
        
        if course_data.get('vagas_unidade'):
            location_info.append(["Vagas por Unidade", clean_field_value(course_data['vagas_unidade'])])
        
        if location_info:
            location_table = create_info_table(location_info)
            elements.append(location_table)
            elements.append(Spacer(1, 0.2*inch))
    
    # Informações de parceiros externos
    if course_data.get('parceiro_externo') == 'sim':
        elements.append(Paragraph("<b>PARCEIRO EXTERNO</b>", section_style))
        
        partner_info = []
        
        if course_data.get('parceiro_nome'):
            partner_info.append(["Nome do Parceiro", wrap_text(clean_field_value(course_data['parceiro_nome']), 50)])
        
        if course_data.get('parceiro_link'):
            partner_info.append(["Link do Parceiro", wrap_text(clean_field_value(course_data['parceiro_link']), 50)])
        
        if partner_info:
            partner_table = create_info_table(partner_info)
            elements.append(partner_table)
            elements.append(Spacer(1, 0.2*inch))
    
    # Informações complementares
    if course_data.get('info_complementares'):
        elements.append(Paragraph("<b>INFORMAÇÕES COMPLEMENTARES</b>", section_style))
        info_text = wrap_text(clean_field_value(course_data['info_complementares']), 70)
        elements.append(Paragraph(info_text, field_style))
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