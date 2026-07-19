from src.ui.components.ui_style_table import frima_estilo_aviso, frima_estilo
from reportlab.platypus import Table, Paragraph,  TableStyle
from reportlab.lib import colors

def tabla_frima_pdf_unica(nombre_firma: str, cargo_firma: str, permiso_operacion: int | None, qr_izq='', qr_der=""):
    estilo_f1 = frima_estilo()
    if permiso_operacion == 0:
        firma1 = nombre_firma
        firma_label = 'Alcalde Municipal'
    elif permiso_operacion == 1:
        firma1 = nombre_firma
        firma_label = 'Tesoreria Municipal'
    elif permiso_operacion == 2:
        firma1 = nombre_firma
        firma_label = 'Alcalde Municipal'
    else:
        firma1 = nombre_firma if nombre_firma else ""
        firma_label = cargo_firma

    valores_fila = [
        qr_izq,
        Paragraph("",),
        Paragraph(firma1, estilo_f1),
        Paragraph("",),
        qr_der,
    ]

    valores_fila_2 = [
        Paragraph("",),
        Paragraph("",),
        Paragraph(firma_label, estilo_f1),
        Paragraph("",),
        Paragraph("",),
    ]
    tabla_firma = Table(
        [valores_fila, valores_fila_2],
        colWidths=[50, 100, 200, 100, 50],  # ajusta según tus márgenes
    )

    tabla_firma.setStyle(TableStyle([
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (4, 0), (4, 1)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        # línea encima de la celda central
        ("LINEABOVE", (2, 0), (2, 0), 1, "black"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))

    return tabla_firma


def tabla_frima_admin_fima_recibido(nombre_firma: str, cargo_firma: str, nombre_recibe: str, firma_admin):
    estilo_f1 = frima_estilo_aviso()
    image_firma = [
                Paragraph("", estilo_f1),
                firma_admin,
                Paragraph("", estilo_f1),
                Paragraph("", estilo_f1),
                Paragraph("", estilo_f1),
            ]

    valores_fila = [

        Paragraph("",),
        Paragraph(nombre_firma, estilo_f1),
        Paragraph("",),
        Paragraph(nombre_recibe, estilo_f1),
        Paragraph("",),
    ]

    valores_fila_2 = [
        Paragraph("",),
        
        Paragraph(cargo_firma, estilo_f1),
        Paragraph("",),
        Paragraph("Recibido Por", estilo_f1),
        Paragraph("",),
    ]
    tabla_firma = Table(
                [image_firma,valores_fila,valores_fila_2],
                colWidths=[50, 200, 50, 200, 50],
            )

    tabla_firma.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (1, 1), (1, 1), 1, colors.black),
        ("LINEABOVE", (3, 1), (3, 1), 1, colors.black),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    return tabla_firma
