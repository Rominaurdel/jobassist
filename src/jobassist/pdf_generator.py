"""
Génération de PDF avec ReportLab
"""

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    ReportLab = True
except ImportError:
    ReportLab = None

from .utils import clean_markdown


def generate_pdf(text: str, output_path: str):
    """Génère un PDF à partir du texte nettoyé"""
    if not ReportLab:
        raise ImportError("reportlab not installed. Run: pip install -r requirements.txt")
    
    # Nettoyer le texte
    clean_text = clean_markdown(text)
    
    # Créer le document PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    # Styles
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        leading=18,
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Construire le contenu
    story = []
    lines = clean_text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Ligne vide
        if not line:
            story.append(Spacer(1, 6))
            i += 1
            continue
        
        # Détecter les titres de section
        is_title = False
        if len(line) < 50:
            if line.isupper() or (i + 1 < len(lines) and not lines[i + 1].strip()):
                is_title = True
            elif not line.endswith('.') and not line.endswith(',') and not line.endswith(':'):
                if len(line.split()) < 8:  # Moins de 8 mots
                    is_title = True
        
        # Échapper les caractères HTML spéciaux pour ReportLab
        line_escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        if is_title:
            story.append(Paragraph(line_escaped, title_style))
        else:
            story.append(Paragraph(line_escaped, normal_style))
        
        i += 1
    
    # Générer le PDF
    doc.build(story)
