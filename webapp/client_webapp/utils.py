import os
import logging

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from PIL import Image as PILImage
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


def create_analysis_pdf(container_name, log_level, ai_response, logo_path=None) -> bytes:
    """
    Crea un documento PDF con logo centrato e informazioni di analisi.

    Args:
        container_name (str): Nome del container
        log_level (str): Livello di log
        ai_response (str): Risposta dell'AI
        logo_path (str): Percorso del logo (opzionale)

    Returns:
        bytes: i bytes del PDF creato
    """
    output_bytes = BytesIO()
    doc = SimpleDocTemplate(
        output_bytes,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
        title=f"{container_name} - Analisi log",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#2C3E50'),
        alignment=TA_CENTER,
        spaceAfter=30
    )

    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#34495E'),
        spaceBefore=20,
        spaceAfter=10
    )

    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#2C3E50'),
        spaceAfter=15,
        alignment=TA_LEFT
    )

    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#7F8C8D'),
        spaceAfter=10
    )

    report_content = []

    if logo_path and os.path.exists(logo_path):
        try:
            # Verifica e ridimensiona il logo se necessario
            img = PILImage.open(logo_path)
            width, height = img.size

            # Calcola le dimensioni per mantenere l'aspect ratio
            max_width = 3 * inch
            max_height = 2 * inch

            if width > max_width or height > max_height:
                ratio = min(max_width / width, max_height / height)
                new_width = width * ratio
                new_height = height * ratio
            else:
                new_width = width
                new_height = height

            logo = Image(logo_path, width=new_width, height=new_height)
            logo.hAlign = 'CENTER'
            report_content.append(logo)
            report_content.append(Spacer(1, 30))

        except Exception as e:
            logger.error(f"Errore nel caricamento del logo: {e}")
            logger.exception(e, exc_info=True)

    report_content.append(Paragraph("Risultati Analisi AI", title_style))
    report_content.append(Spacer(1, 20))

    italian_tz = ZoneInfo('Europe/Rome')
    current_time = datetime.now(italian_tz).strftime("%d/%m/%Y alle %H:%M:%S")
    report_content.append(Paragraph(f"<i>Report generato il {current_time}</i>", info_style))
    report_content.append(Spacer(1, 30))

    report_content.append(Paragraph("Nome Container", section_title_style))
    report_content.append(Paragraph(f"<b>{container_name}</b>", content_style))

    report_content.append(Paragraph("Livello di Log", section_title_style))

    log_colors = {
        'DEBUG': '#3498DB',
        'INFO': '#2ECC71',
        'WARNING': '#F39C12',
        'ERROR': '#E74C3C',
        'CRITICAL': '#8E44AD'
    }

    log_color = log_colors.get(log_level.upper(), '#2C3E50')
    report_content.append(Paragraph(f"<b><font color='{log_color}'>{log_level.upper()}</font></b>", content_style))


    report_content.append(Paragraph("Risposta AI", section_title_style))

    ai_response_formatted = ai_response.replace('\n', '<br/>')
    report_content.append(Paragraph(ai_response_formatted, content_style))

    report_content.append(Spacer(1, 50))
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#95A5A6'),
        alignment=TA_CENTER
    )
    report_content.append(Paragraph("--- Fine del Report ---", footer_style))

    doc.build(report_content)

    return output_bytes.getvalue()
