from src.ui.components.ui_style_table import frima_estilo_aviso, frima_estilo
from reportlab.platypus import Table, Paragraph,  TableStyle
from reportlab.lib import colors

#ESTILOS TABLAS
ESTILOS_TABLA_APREMIO_DOS = TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (1, 1), (1, 1), 1, colors.black),
        ("LINEABOVE", (3, 1), (3, 1), 1, colors.black),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ])

ESTILOS_TABLA_APREMIO_TRES = TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (0, 1), (0, 1), 1, colors.black),
        ("LINEABOVE", (2, 1), (2, 1), 1, colors.black),
        ("LINEABOVE", (4, 1), (4, 1), 1, colors.black),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ])
ESTILOS_TABLA_FIRMA_ADMIN = TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (1, 1), (1, 1), 1, colors.black),
        ("LINEABOVE", (3, 1), (3, 1), 1, colors.black),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ])
ESTILOS_F1 = frima_estilo_aviso()

ESTILOS_TABLA_UNICA_RPT = TableStyle([
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
    ])

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
        "",
        Paragraph(firma1, estilo_f1),
        "",
        qr_der,
    ]

    valores_fila_2 = [
        "",
        "",
        Paragraph(firma_label, estilo_f1),
        "",
        "",
    ]
    tabla_firma = Table(
        [valores_fila, valores_fila_2],
        colWidths=[50, 100, 200, 100, 50],  # ajusta según tus márgenes
    )

    tabla_firma.setStyle(ESTILOS_TABLA_UNICA_RPT)

    return tabla_firma


def tabla_frima_admin_fima_recibido(nombre_firma: str, cargo_firma: str, nombre_recibe: str, firma_admin):
    image_firma = [
                "",
                firma_admin,
                "",
                "",
                "",
            ]

    valores_fila = [
        "",
        Paragraph(nombre_firma, ESTILOS_F1),
        "",
        Paragraph(nombre_recibe, ESTILOS_F1),
        "",
    ]
    valores_fila_2 = [
        "",
        Paragraph(cargo_firma, ESTILOS_F1),
        "",
        Paragraph("Recibido Por", ESTILOS_F1),
        "",
    ]
    tabla_firma = Table(
                [image_firma,valores_fila,valores_fila_2],
                colWidths=[50, 200, 50, 200, 50],
            )

    tabla_firma.setStyle(ESTILOS_TABLA_FIRMA_ADMIN)

    return tabla_firma


def firma_apremio_tres(nombre_1: str, cargo_1: str, nombre_2: str, cargo_2, img_firma_1, img_firma_2, nombre_3 = "Recibodo Por", cargo_3="Contribuyente"):
    
    image_firma = [
        img_firma_1,
        "",
        img_firma_2,
        "",
        "",
    ]
    valores_fila = [
        Paragraph(nombre_1, ESTILOS_F1),
        "",
        Paragraph(nombre_2, ESTILOS_F1),
        "",
        Paragraph(nombre_3, ESTILOS_F1),
    ]

    valores_fila_2 = [
        Paragraph(cargo_1, ESTILOS_F1),
        "",
        Paragraph(cargo_2, ESTILOS_F1),
        "",
        Paragraph(cargo_3, ESTILOS_F1),
    ]
    tabla_firma = Table(
                [image_firma,valores_fila,valores_fila_2],
                colWidths=[150, 50, 150, 50, 150],
            )

    tabla_firma.setStyle(ESTILOS_TABLA_APREMIO_TRES)

    return tabla_firma


def firma_apremio_dos(nombre_1: str, cargo_1: str, img_firma_1, nombre_2 = "Recibodo Por", cargo_2="Contribuyente"):
    
    image_firma = [
        "",
        img_firma_1,
        "",
        "",
        "",
    ]
    valores_fila = [
        "",
        Paragraph(nombre_1, ESTILOS_F1),
        "",
        Paragraph(nombre_2, ESTILOS_F1),
       "",
    ]

    #valores_fila_2 = [
    #    "",
    #    Paragraph(cargo_1, ESTILOS_F1),
    #    "",
    #    Paragraph(cargo_2, ESTILOS_F1),
    #    "",
    #]
    tabla_firma = Table(
                [image_firma,valores_fila],
                colWidths=[50, 200, 50, 200, 50],
            )

    tabla_firma.setStyle(ESTILOS_TABLA_APREMIO_DOS)

    return tabla_firma